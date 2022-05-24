"""Detecting and reporting errors."""

# Python built-in modules:
from datetime import datetime

# Local modules:
import settings
import app_data
import theming
import helpers

cfg = settings.Settings()


def product_available(product_name: str, command: str) -> bool:
    """Checks if product is available and creates new product record if neccessary."""
    # Create a product object.
    products = app_data.ReadWriteCSV(cfg.dataset_properties("products"))
    # If product has id then it exists.
    product_id = products.get_record_id(product_name, "product_name")
    # When new products is purchased.
    if product_id is None and command == "purchase":
        # Create a new product record.
        product_id = products.create_record_id()
        new_record = {
            "id": product_id,
            "product_name": product_name,
            "total_bought": "0",
            "total_sold": "0",
            "total_in_stock": "0",
            "total_expired": "0",
            "sum_costs": "0.00",
            "sum_revenues": "0.00",
        }
        products.append_record(new_record)
    elif product_id is None:
        theming.rich_msg(f"The product ('{product_name}') is not available!\n", "error")
        return False
    return True


def amount_available(amount: int, product_name: str) -> bool:
    """Checks if the amount of a certain product is available."""
    products = app_data.ReadWriteCSV(cfg.dataset_properties("products"))
    product_id = products.get_record_id(product_name, "product_name")
    # Get product record to fetch total stock amount
    product_record = products.read_record(product_id)
    if amount < int(product_record["total_in_stock"]):
        return True
    else:
        theming.rich_msg(
            f"Only {product_record['total_in_stock']} of {product_name} in stock!\n", "error"
        )
        return False


def valid_date_type(the_date: str, command: str) -> str:
    """Checks if the date is valid."""

    # What date type measured by length of string.
    if str(the_date).isalpha():
        date_type = "day"
    elif len(str(the_date)) == 10:
        date_type = "date"
    elif len(str(the_date)) == 7:
        date_type = "month"
    elif len(str(the_date)) == 6:
        date_type = "quarter"
    elif len(str(the_date)) == 4:
        date_type = "year"
    else:
        theming.rich_msg(f"The date ('{the_date}') has not a valid notation!\n", "error")
        date_type = None

    # Does the date have the proper format and value.
    if date_type == "day" and the_date not in ["today", "yesterday"]:
        theming.rich_msg(f"The day ('{the_date}') can only be 'today' or 'yesterday'!\n", "error")
        date_type = None
    elif date_type in ["date", "month", "year"]:
        if date_type == "date":
            date_format = "%Y-%m-%d"
        if date_type == "month":
            date_format = "%Y-%m"
        if date_type == "year":
            date_format = "%Y"
        try:
            datetime.strptime(the_date, date_format)
        except Exception:
            theming.rich_msg(f"The date ('{the_date}') has not a valid notation!\n", "error")
            date_type = None
        # In case the date is the expiration date in a purchase
        if date_type == "date" and command == "purchase":
            if helpers.days_between_dates(cfg.application_date(), the_date) <= 8:
                theming.rich_msg(
                    f"Expiration date ('{the_date}') can not be less then 8 days beyond date of purchase!\n",
                    "error",
                )
                date_type = None
    elif date_type == "quarter":
        slice_year = the_date[0:4]
        try:
            datetime.strptime(slice_year, "%Y")
        except Exception:
            theming.rich_msg(f"The year in '{the_date}' is not a valid notation!\n", "error")
            date_type = None
        slice_quarter = the_date[-1]
        if slice_quarter not in ("1", "2", "3", "4"):
            theming.rich_msg(f"The quarter in '{the_date}' should be a 1,2,3 or 4 !\n", "error")
            date_type = None
    elif date_type is None and command == "report":
        theming.rich_msg(
            "Please enter 'yesterday', 'today', a date ('yyyy-mm-dd'), month ('yyyy-mm'), quarter ('yyyy-q') or a year ('yyyy') in the command prompt!",
            "error",
        )
        date_type = None

    return date_type
