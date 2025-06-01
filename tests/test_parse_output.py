import pytest

from optool.open_prescribe import produce_output, parse_highest_orderer_for_month


class TestParseProduceOutput:
    def test_produces_correct_output(self):
        chemical_name = "Test Chemical"
        spending_by_org = {
            "2023-01": ("ICB A", 1000),
            "2023-02": ("ICB B", 2000),
        }
        expected_output = "\nTest Chemical\n\n2023-01 ICB A\n2023-02 ICB B"
        assert produce_output(chemical_name, spending_by_org) == expected_output

    def test_empty_spending_by_org(self):
        chemical_name = "Test Chemical"
        spending_by_org = {}
        expected_output = "\nTest Chemical\n\n"
        assert produce_output(chemical_name, spending_by_org) == expected_output


class TestParseHighestOrdererForMonth:

    def test_parses_correctly(self):
        info_from_api = {
            "2023-01": ("ICB A", 1000),
            "2023-02": ("ICB B", 2000),
        }
        expected_output = [
            "2023-01 ICB A",
            "2023-02 ICB B",
        ]
        assert parse_highest_orderer_for_month(info_from_api) == expected_output

    def test_empty_input(self):
        assert parse_highest_orderer_for_month({}) == []