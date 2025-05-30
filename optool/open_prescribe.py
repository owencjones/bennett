from re import match
from optool.exceptions import OPToolException, OPToolException_BNF_Code_was_invalid
from rich.console import Console

API_BASE = "https://openprescribing.net/api/"


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
    
    if len(bnf_str) < 15:
        raise OPToolException_BNF_Code_was_invalid("The tool currently only accepts full 15 character BNF codes, sorry!")
    elif (len(bnf_str) > 15):
        raise OPToolException_BNF_Code_was_invalid("The code you entered was too long to be valid.")
    
    bnf_regex = r"[0-9]{6}[A-Z0-9]{9}"

    if not match(bnf_regex, bnf_str):
        raise OPToolException_BNF_Code_was_invalid("Code doesn't appear to be a valid BNF code")
    
    return


def retrieve_api_output(bnf_code: str) -> dict:
    """
    Accesses the API and uses the output and turns it into a limited set of info we need for the specs
    """
    raise NotImplementedError


def produce_output(api_output: dict) -> str:
    """
    Produces a string to output to the user
    """
    raise NotImplementedError

