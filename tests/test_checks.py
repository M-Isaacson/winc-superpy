"""Test checks module."""

import src.checks as checks
import pytest

invalid_date_checks = [
    "vijf juni negentienvijftig",
    "15 mei 2022",
    "100-04-02",
    "",
    "2019/03/01",
    "20-23-1990",
    "2018-10-64",
    "2012-23-10",
    "2010-8-20",
    "2010-08-2",
    2012 - 12 - 12,
    2012 / 12 / 12,
    2012,
    12,
    2012.12,
]


@pytest.mark.parametrize("command", ["purchase", "report"])
@pytest.mark.parametrize("invalid", invalid_date_checks)
def test_valid_date_type_has_invalid_date_argument(command, invalid):
    """Test to check if a invalid date returns None."""
    assert checks.valid_date_type(invalid, command) is None


valid_date_checks = [
    ("today", "day"),
    ("yesterday", "day"),
    ("2020-01-23", "date"),
    ("2020-01", "month"),
    ("2020-1", "quarter"),
    ("2020", "year"),
]


@pytest.mark.parametrize("valid, result", valid_date_checks)
def test_valid_date_type_has_valid_date_argument(valid, result):
    """Test to check if a valid date returns a string."""
    assert checks.valid_date_type(valid, "report") == result
