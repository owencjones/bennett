from json import loads
from pathlib import Path
from unittest.mock import patch
import pytest
from requests import Response

from optool import (
    retrieve_api_output,
    retrieve_single_drug_chemical,
)
from optool.exceptions import OPToolException_API_connection_failed
from optool.open_prescribe import get_spending_by_org

from .fixtures import *  # noqa: F403


class TestApiRetrieveApiOutput:

    @pytest.mark.parametrize("status_code", [200, 201])
    def test_all_of_the_valid_statuses(
        self, status_code: int, get_http_fixture: Response
    ):
        get_http_fixture.status_code = status_code
        with pytest.raises(OPToolException_API_connection_failed):
            retrieve_api_output("SOMEURL")

    @pytest.mark.parametrize("status_code", list(range(100, 199)))
    def test_fails_on_early_range(self, status_code: int, get_http_fixture: Response):
        get_http_fixture.status_code = status_code
        with pytest.raises(OPToolException_API_connection_failed):
            retrieve_api_output("SOMEURL")

    @pytest.mark.parametrize("status_code", list(range(303, 600)))
    def test_fails_on_late_range(self, status_code: int, get_http_fixture: Response):
        get_http_fixture.status_code = status_code
        with pytest.raises(OPToolException_API_connection_failed):
            retrieve_api_output("SOMEURL")

    # @pytest.mark.xfail(reason="Requires network, so may fail safely")
    def test_one_real_connection(self) -> None:
        retrieve_api_output(
            "https://openprescribing.net/api/1.0/bnf_code/?exact=true&format=json&q=1304000H0AAAAAA"
        )


class TestRetrieveSingleDrug:

    @pytest.mark.parametrize(
        "bnf_code, expectation",
        [
            ("1304000H0AAAAAA", "Clobetasone butyrate"),
            ("0212000AAAAAIAI", "Rosuvastatin calcium"),
            ("0407010ADBCAAAB", "Paracetamol and ibuprofen"),
            ("0301020I0BBAFAF", "Ipratropium bromide"),
            ("040702040BEABAC", "Tramadol hydrochloride"),
        ],
    )
    def test_successfully_retrieves_a_real_bnf_entry(self, bnf_code, expectation):
        output = retrieve_single_drug_chemical(bnf_code)

        assert output[0] == expectation


class TestGetSpendingByOrg:
    # For speed this is done on a expected output for expected output

    @pytest.fixture
    def mocked_api_response(self):
        test_data = (
            (Path(__file__).parent) / "data" / "spending_by_org.json"
        ).read_text(encoding="utf-8")
        with patch(
            "optool.open_prescribe.retrieve_api_output", return_value=loads(test_data)
        ) as mock:
            yield mock

    @pytest.fixture
    def mocked_output(self, mocked_api_response):
        test_data = (
            (Path(__file__).parent) / "data" / "spending_by_org_expectation.json"
        ).read_text(encoding="utf-8")
        return loads(test_data)
    
    """
    These tests are not intended to be exhaustive, but rather to ensure that the function
    behaves as expected with a known input and output.

    The tests of `TestApiRetrieveApiOutput` are more illustrative of my usual style.
    """

    def test_output_is_correct(self, mocked_api_response, mocked_output) -> None:
        output = get_spending_by_org("1304000H0")
        
        assert len(mocked_output) == len(output), "Output was of a different length!"
        
        simplified_mocked_output = [(k, v[0], v[1]) for k,v in mocked_output.items()]
        simplified_output = [(k, v[0], v[1]) for k, v in output.items()]

        assert simplified_mocked_output == simplified_output, "Output did not match expectation"