from json import loads
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from requests import Response

from optool import (
    retrieve_api_output,
    retrieve_single_drug_chemical,
)
from optool.exceptions import OPToolException_API_connection_failed
from optool.open_prescribe import get_spending_by_org

from .fixtures import * #noqa: F403

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

    def test_something(self) -> None:
        output = get_spending_by_org("1304000H0")
        assert output
