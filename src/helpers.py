""" Generic functions."""

# Python built-in modules
from datetime import date, timedelta


def date_yesterday(current_date: str) -> str:
    """Calculates yesterdays date from a certain date."""
    try:
        len(current_date) == 10
        today = date.fromisoformat(current_date)
        yesterday = today - timedelta(days=1)
        return date.isoformat(yesterday)
    except Exception:
        raise  # Source: https://stackoverflow.com/questions/57080127/pytest-raises-failed-did-not-raise-with-try-except


def days_between_dates(date_base: str, date_offset: str) -> int:
    """Calulates the amount of days between two dates."""
    try:
        len(date_base) == 10
        len(date_offset) == 10
        base = date.fromisoformat(date_base)
        offset = date.fromisoformat(date_offset)
        amount = offset - base
        return amount.days
    except Exception:
        raise


def valuta_notation(number: float, valuta: str = "€") -> str:
    """Turns a floating point number into valuta notation."""
    try:
        if type(number) == int:
            number = float(number)
        number_list = str(number).split(".")
        length = len(number_list[1])
        # There are at least 2 digits, but there could be more.
        if length > 2:
            digits = length
        else:
            digits = 2
        return f"{valuta} {number:.{digits}f}"
    except Exception:
        raise
