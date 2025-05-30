"""
This allows us to differentiate between expected and unexpected errors, and handle them differently.
"""

class OPToolException(BaseException):
    ...