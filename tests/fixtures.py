from unittest.mock import MagicMock, patch

import pytest
from requests import Response


class TestException(Exception): ...


@pytest.fixture
def get_http_fixture():
    with patch("optool.open_prescribe.get_http", spec=Response) as get_http_mock:
        get_http_mock.status_code = 200
        get_http_mock.headers = dict()
        get_http_mock.headers["Content-type"] = "application/json"
        get_http_mock.json = MagicMock()
        get_http_mock.json.return_value = {"foo": "bar"}

        yield get_http_mock
