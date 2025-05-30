from requests import get as get_http

from re import match
from optool.exceptions import (
    OPToolException_API_connection_failed,
    OPToolException_BNF_Code_was_invalid,
    OPToolException_API_connection_failed,
)
from rich.console import Console

API_BASE = "https://openprescribing.net/api"


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
    api_output = retrieve_api_output(bnf_code)
    output = produce_output(api_output)

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

    bnf_regex = r"[0-9]{6}[A-Z0-9]{9}"

    if not match(bnf_regex, bnf_str):
        raise OPToolException_BNF_Code_was_invalid(
            "Code doesn't appear to be a valid BNF code"
        )

    return


def retrieve_api_output(url: str) -> dict:
    """
    Accesses the API and uses the output and turns it into a limited set of info we need for the specs
    """
    output_http = get_http(url, timeout=5000, allow_redirects=True)

    if output_http.status_code == 404:
        raise OPToolException_API_connection_failed("The code did not match any BNF item(s)")

    if 302 <= output_http.status_code >= 200:
        raise OPToolException_API_connection_failed(f"Attempting to connect to the API Failed.  We got a response code of {output_http.status_code}  You could try again, or contact technical support.")
    
    if (content_type := output_http.headers.get('Content-Type')) is not None and content_type != 'application/json':
        raise OPToolException_API_connection_failed("We didn't get the type of data we were expecting from the API!")
    
    data = output_http.json()

    return data



def retrieve_single_drug(bnf_code: str) -> dict:
    url = f"https://openprescribing.net/api/1.0/bnf_code/?exact=true&format=json&q={bnf_code}"
    return retrieve_api_output(url)


def 


def produce_output(api_output: dict) -> str:
    """
    Produces a string to output to the user
    """
    return str(api_output[0]['name'])
