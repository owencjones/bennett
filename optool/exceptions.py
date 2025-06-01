"""
This allows us to differentiate between expected and unexpected errors, and handle them differently.
"""


class OPToolException(BaseException):
    def __init__(self, message: str):
        self.message = message
        super()


class OPToolException_BNF_Code_was_invalid(OPToolException): ...


class OPToolException_API_connection_failed(OPToolException): ...
