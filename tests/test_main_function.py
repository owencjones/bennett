import pytest

from optool import (
    main,
    produce_output,
    retrieve_api_output,
    validate_bnf_code,
)
from .fixtures import *  # noqa: F403
from unittest.mock import MagicMock, patch


class TestMain:

    validate_bnf_code_mock = MagicMock()
    retrieve_api_output_mock = MagicMock()
    produce_output_mock = MagicMock()

    @pytest.mark.parametrize(
        "func",
        [
            validate_bnf_code,  # Sad path
            retrieve_api_output,  # Sad path
            produce_output,  # Sad path
            None,  # Happy path
        ],
    )
    def test_throws_exception_if_any_called_function_raises(self, func):
        # Initial happy path setup.
        with patch(
            "optool.open_prescribe.validate_bnf_code", self.validate_bnf_code_mock
        ) as mock_v, patch(
            "optool.open_prescribe.retrieve_api_output", self.retrieve_api_output_mock
        ) as mock_r, patch(
            "optool.open_prescribe.produce_output", self.produce_output_mock
        ) as mock_p:

            mock_console = MagicMock()

            # Set the output values
            self.retrieve_api_output_mock.return_value = "TestValue 1"
            self.produce_output_mock.return_value = "TestValue 2"

            if func is None:
                main("BNFCODE", mock_console)
                mock_v.assert_called_once()
                mock_r.assert_called_once_with("BNFCODE")
                mock_p.assert_called_once_with("TestValue 1")
                mock_console.print.assert_called_once_with("TestValue 2")
                return True

            elif func.__name__ == "validate_bnf_code":
                mock_v.side_effect = TestException()
            elif func.__name__ == "retrieve_api_output":
                mock_r.side_effect = TestException()
            elif func.__name__ == "produce_output":
                mock_p.side_effect = TestException()

            with pytest.raises(TestException):
                main("BNFCODE", mock_console)
