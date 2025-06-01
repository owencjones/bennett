from argparse import Namespace
from enum import unique
from re import match
from typing import Optional

from requests import get as get_http
from rich.console import Console

from .exceptions import (
    OPToolException_API_connection_failed,
    OPToolException_BNF_Code_was_invalid,
)


def main(bnf_code: str, console: Console, weighted: bool) -> None:
    """
    Default entrypoint for the tool.

    Parameters
    __________
    bnf_code    string      A 15-Character string to identify a BNF item


    Returns
    _______

    None

    Raises
    ______

    OPToolException - An anticipated error occurred
    Exception - An unanticipated error occurred
    """

    validate_bnf_code(bnf_code)
    chemical, chemical_code = retrieve_single_drug_chemical(bnf_code)
    ordering_by_org = get_spending_by_org(chemical_code, weighted)
    output = produce_output(chemical, ordering_by_org)

    console.print(output)


def validate_bnf_code(bnf_str: str) -> None:
    """
    Validates a BNF Code input from the user

    Parameters
    __________
    bnf_str     string      The BNF code string to validate

    Raises
    ______
    OPToolException_BNF_Code_was_invalid - If the BNF code is invalid
    """

    assert isinstance(bnf_str, str), "Expected a string."

    if len(bnf_str) < 15:
        raise OPToolException_BNF_Code_was_invalid(
            "The tool currently only accepts full 15 character BNF codes, sorry!"
        )
    elif len(bnf_str) > 15:
        raise OPToolException_BNF_Code_was_invalid(
            "The code you entered was too long to be valid."
        )

    bnf_regex = r"[0-9]{6}[A-Z0-9\*]{9}"

    if not match(bnf_regex, bnf_str):
        raise OPToolException_BNF_Code_was_invalid(
            "Code doesn't appear to be a valid BNF code"
        )

    return


def retrieve_api_output(url: str) -> dict | list:
    """
    Accesses the API and uses the output and turns it into a limited set of info we need for the specs
    """
    output_http = get_http(url, timeout=5000, allow_redirects=True)

    if output_http.status_code == 404:
        raise OPToolException_API_connection_failed(
            "The code did not match any BNF item(s)"
        )

    if output_http.status_code not in [200, 201]:
        raise OPToolException_API_connection_failed(
            f"Attempting to connect to the API Failed.  We got a response code of {output_http.status_code}  You could try again, or contact technical support."
        )

    if (
        content_type := output_http.headers.get("Content-Type")
    ) is not None and content_type != "application/json":
        raise OPToolException_API_connection_failed(
            "We didn't get the type of data we were expecting from the API!"
        )

    data = output_http.json()

    return data


#############
# Stage One #
#############
def retrieve_single_drug_chemical(bnf_code: str) -> tuple[str, str]:
    chemical_name_from_code = bnf_code[0:9]
    url = f"https://openprescribing.net/api/1.0/bnf_code/?format=json&q={chemical_name_from_code}"

    output = retrieve_api_output(url)

    chemical_names = [
        item.get("name") for item in output if item.get("type") == "chemical"
    ]

    if len(chemical_names) > 1:
        raise OPToolException_BNF_Code_was_invalid(
            "The BNF Code returned {len(chemical_names)} names for base chemical, which should be possible...  Please report this"
        )

    return chemical_names[0], chemical_name_from_code


#############
# Stage Two #
#############


def get_spending_by_org(
    chemical_code: str, weighted: Optional[bool] = False
) -> dict[str, tuple[str, int]]:
    url = f"https://openprescribing.net/api/1.0/spending_by_org/?format=json&org_type=icb&code={chemical_code}"

    api_output = retrieve_api_output(url)
    if not api_output or not isinstance(api_output, list):
        raise OPToolException_API_connection_failed(
            "No data was returned for the chemical code provided.  Please check the code and try again."
        )

    unique_icbs = get_unique_items_by_key(api_output, "row_name")
    unique_months = sorted(get_unique_items_by_key(api_output, "date"), reverse=True)

    icb_with_highest_ordering_per_month = {}
    icb_to_quantity = {}

    if weighted:
        icb_month_to_headcount = generate_weighting_by_icb_headcount(chemical_code)
    else:
        icb_month_to_headcount = {}

    for month in unique_months:
        for icb in unique_icbs:
            if weighted:
                total_for_month = sum(
                    item["items"] / icb_month_to_headcount.get(f"{icb}_{month}", 1)
                    for item in api_output
                    if item.get("row_name") == icb and item.get("date") == month
                )
            else:
                total_for_month = sum(
                    item["items"]
                    for item in api_output
                    if item.get("row_name") == icb and item.get("date") == month
                )

            if icb in icb_to_quantity:
                icb_to_quantity[icb] += total_for_month
            else:
                icb_to_quantity[icb] = total_for_month

            icb_to_quantity[icb] = total_for_month

        icb_with_highest_ordering_per_month[month] = max(
            icb_to_quantity.items(), key=lambda x: x[1], default=(None, 0)
        )

    return icb_with_highest_ordering_per_month


def get_unique_items_by_key(api_output: list[dict], key: str) -> list:
    items = set([i[key] for i in api_output if i.get(key)])
    return list(items)


###############
# Stage Three #
###############


def generate_weighting_by_icb_headcount(chemical_code: str) -> dict[str, int]:
    url = f"https://openprescribing.net/api/1.0/org_details/?org_type=icb&keys=total_list_size&format=json&code={chemical_code}"

    api_output = retrieve_api_output(url)

    if not api_output or not isinstance(api_output, list):
        raise OPToolException_API_connection_failed(
            "No data was returned for the chemical code provided.  Please check the code and try again."
        )

    unique_icbs = get_unique_items_by_key(api_output, "row_name")
    unique_months = sorted(get_unique_items_by_key(api_output, "date"), reverse=True)

    icb_month_to_headcount: dict[str, int] = {}

    for month in unique_months:
        for icb in unique_icbs:
            key = f"{icb}_{month}"

            headcount = next(
                (
                    item["total_list_size"]
                    for item in api_output
                    if item.get("row_name") == icb and item.get("date") == month
                ),
                1,  # Default to 1 if not found to avoid div/0
            )

            icb_month_to_headcount[key] = headcount

    return icb_month_to_headcount


# Output functions


def parse_highest_orderer_for_month(
    info_from_api: dict[str, tuple[str, int]],
) -> list[str]:
    """
    Parses the list of highest spenders into a list of strings for output

    In format date: [Date] [ICB Name]
    """
    return [f"{line[0]} {line[1][0]}" for line in info_from_api.items()]


def produce_output(chemical_name: str, spending_by_org: dict) -> str:
    """
    Produces a string to output to the user
    """
    output = "\n" + str(chemical_name) + "\n\n"

    output += "\n".join(parse_highest_orderer_for_month(spending_by_org))

    return output
