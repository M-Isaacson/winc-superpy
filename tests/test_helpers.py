"""Test helpers module."""
import src.helpers as helpers
import pytest


# ========= DATE_YESTERDAY =========
def test_date_yesterday_current_date_raises_exception(invalid_date):
    """Testing if an exeption is raised, when argument is not a valid date. Makes use of conftest."""
    with pytest.raises(Exception):
        helpers.date_yesterday(invalid_date)


# Variables to use in test_date_yesterday_result.
calc_yesterday_dates = [
    ("0100-10-10", "0100-10-09"),
    ("2013-03-01", "2013-02-28"),
    ("2020-03-01", "2020-02-29"),
    ("2224-04-05", "2224-04-04"),
]
ids_calc_yesterday_dates = []
for calc_yesterday_value in calc_yesterday_dates:
    ids_calc_yesterday_dates.append(f"{calc_yesterday_value[0]} >> {calc_yesterday_value[1]}")


@pytest.mark.parametrize("current_date,result", calc_yesterday_dates, ids=ids_calc_yesterday_dates)
def test_date_yesterday_result(current_date, result):
    """Testing if argument returns valid date of yesterday."""
    assert helpers.date_yesterday(current_date) == result


# ========= DAYS_BETWEEN_DATES =========
def test_days_between_dates_base_date_raises_exception(invalid_date):
    """Testing if an exeption is raised, when first argument is not a valid date. Makes use of conftest."""
    with pytest.raises(Exception):
        helpers.days_between_dates(invalid_date, "2020-02-02")


def test_days_between_dates_offset_date_raises_exception(invalid_date):
    """Testing if an exeption is raised, when second argument is not a valid date. Makes use of conftest."""
    with pytest.raises(Exception):
        helpers.days_between_dates("2020-02-02", invalid_date)


# Variables to use in test_days_between_dates_result.
substract_dates = [
    ("2030-10-10", "2030-10-05", -5),
    ("2030-10-05", "2030-10-10", 5),
    ("2020-02-29", "2020-03-01", 1),
    ("2021-02-28", "2021-03-01", 1),
]
ids_substract_dates = []
for substract_value in substract_dates:
    ids_substract_dates.append(
        f"'{substract_value[1]}'-'{substract_value[0]}' >> {substract_value[2]}"
    )


@pytest.mark.parametrize("base,offset,result", substract_dates, ids=ids_substract_dates)
def test_days_between_dates_result(base, offset, result):
    """Testing if arguments returns valid result of subtraction."""
    assert helpers.days_between_dates(base, offset) == result


# ========= VALUTA_NOTATION =========
def test_valuta_notation_string_raises_exception():
    """Testing if string as argument returns an exception."""
    with pytest.raises(Exception):
        helpers.valuta_notation("five")


# Variables to use in test_valuta_notation_result
valuta_notations = [
    (1, "€ 1.00"),
    (1.0, "€ 1.00"),
    (1.001, "€ 1.001"),
    (1.1, "€ 1.10"),
    (1.3456789012, "€ 1.3456789012"),
    (0, "€ 0.00"),
    (0.1, "€ 0.10"),
]
ids_valuta_notations = []
for valuta_value in valuta_notations:
    ids_valuta_notations.append(f"'{valuta_value[0]} >> {valuta_value[1]}")


@pytest.mark.parametrize("number,result", valuta_notations, ids=ids_valuta_notations)
def test_valuta_notation_result(number, result):
    """Testing if a number gives back the expexted valuta notation."""
    assert helpers.valuta_notation(number) == result
