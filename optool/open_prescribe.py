from requests import Response, get as get_http

from re import match
from .exceptions import (
    OPToolException_API_connection_failed,
    OPToolException_BNF_Code_was_invalid,
)
from rich.console import Console


def main(bnf_code: str, console: Console) -> None:
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
    output = produce_output(chemical, [])

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


def retrieve_api_output(url: str) ->  dict | list:
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
        raise OPToolException_BNF_Code_was_invalid("The BNF Code returned {len(chemical_names)} names for base chemical, which should be possible...  Please report this")

    return chemical_names[0], chemical_name_from_code

#############
# Stage Two #
#############

def get_spending_by_org(chemical_code: str) -> list:
    url = f"https://openprescribing.net/api/1.0/spending_by_org/?format=json&org_type=icb&code={chemical_code}"

    output = retrieve_api_output(url)
    assert isinstance(output, list)

    unique_icbs = get_unique_items_by_key(output, 'row_name')
    unique_months = get_unique_items_by_key(output, 'date')

    for month in unique_months:
        TODO: pickup here.

    


def get_unique_items_by_key(api_output: list[dict], key: str) -> list:
    items = set([i[key] for i in api_output if i.get(key)])
    return list(items)


def produce_output(chemical_name: str, spending_by_org: list[str]) -> str:
    """
    Produces a string to output to the user
    """
    output = "\n" + str(chemical_name) + "\n"

    output += "\n".join(spending_by_org)

    return output
