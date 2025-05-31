from unittest.mock import MagicMock, patch
import pytest
from requests import Response

from optool import (
    retrieve_api_output,
    retrieve_single_drug,
)
from optool.exceptions import OPToolException_API_connection_failed


class TestApiRetrieveApiOutput:

    @pytest.fixture
    def get_http_fixture(self):
        with patch("optool.open_prescribe.get_http", spec=Response) as get_http_mock:
            get_http_mock.status_code = 200
            get_http_mock.headers = dict()
            get_http_mock.headers["Content-type"] = "application/json"
            get_http_mock.json = MagicMock()
            get_http_mock.json.return_value = {"foo": "bar"}

            yield get_http_mock

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

    @pytest.mark.xfail(reason="Requires network, so may fail safely")
    def test_one_real_connection(self) -> None:
        retrieve_api_output("https://openprescribing.net/api/1.0/bnf_code/?exact=true&format=json&q=1304000H0AAAAAA")


class TestRetrieveSingleDrug:

    @pytest.mark.parametrize(
        "bnf_code, expectation",
        [
            ("1304000H0AAAAAA", "Clobetasone 0.05% cream"),
            ("0212000AAAAAIAI", "Rosuvastatin 40mg capsules"),
            ("0407010ADBCAAAB", "Combogesic 500mg/150mg tablets"),
            ("0301020I0BBAFAF", "Atrovent 250micrograms/1ml nebuliser liquid UDVs"),
            ("040702040BEABAC", "Dromadol SR 100mg tablets"),
        ],
    )
    def test_successfully_retrieves_a_real_bnf_entry(self, bnf_code, expectation):
        assert retrieve_single_drug(bnf_code) == expectation
