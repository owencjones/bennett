#!/usr/bin/python3

from argparse import ArgumentParser, Namespace
from rich_argparse import RichHelpFormatter
from rich.console import Console

from optool import main, OPToolException, OPToolException_BNF_Code_was_invalid, OPToolException_API_connection_failed


if __name__ == "__main__":

    console = Console()
    try:

        argument_parser = ArgumentParser(
            prog="OpenPrescribe Command Line Tool",
            description="A tool for accessing the OpenPrescribe API to lookup a BNF code",
            formatter_class=RichHelpFormatter
        )
        
        argument_parser.add_argument(
            "bnf_code",
            type=str,
            help="The BNF code to look up",
        )

        args: Namespace = argument_parser.parse_args()
        bnf_code = str(args.bnf_code) if "bnf_code" in args else ""

        main(bnf_code, console)

    except OPToolException_BNF_Code_was_invalid as exc:
        console.print(exc.message)
        exit(1)

    except OPToolException_API_connection_failed as exc:
        console.print(exc.message)
        exit(2)

    except OPToolException:
        console.print("[red]Unfortunately an error occurred with the tool or server.[/red]")
        console.print("Check your internet connection, and if you still have issues, contact technical support.\n")
        console.print_exception()

        exit(100)

    except Exception:
        console.print("[red]An error has occurred that we were not expecting[/red]")
        console.print("Report the below output to technical support:\n")
        console.print_exception()

        exit(255)