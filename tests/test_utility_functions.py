import pytest

from optool.open_prescribe import get_unique_items_by_key


class TestGetUniqueItemsByKey:
    def test_unique_items_by_key(self):
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 30},
            {"name": "Charlie", "age": 35},
        ]
        expected = ["Charlie", "Bob", "Alice"]
        result = get_unique_items_by_key(data, "name")
        assert sorted(result) == sorted(expected)

    def test_empty_list(self):
        result = get_unique_items_by_key([], "name")
        assert result == []