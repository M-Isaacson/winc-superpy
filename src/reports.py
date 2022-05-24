"""Creating reports."""

# Python built-in modules:
import os.path
from datetime import date
from datetime import datetime

# Third party libraries:
import pandas as pd
from tabulate import tabulate

# Local modules:
import settings
import helpers

cfg = settings.Settings()


def inventory(product: str, output: str):
    """Shows inventory of all products or one product."""
    df = pd.read_csv(
        cfg.dataset_properties("products")["path"], delimiter=cfg.csv_delimiter(), index_col="id"
    )
    # Remove unneccessary columns from dataframe.
    df.drop(columns=["sum_costs", "sum_revenues"], inplace=True)
    if product == "all":
        report_df = df.sort_values(by="product_name")
        report_title = "Inventory of all products:".upper()
        file_name = f"inventory_all_{cfg.application_date()}"
    else:
        product_filter = df["product_name"] == product
        report_df = df.loc[product_filter]
        report_title = f"Inventory of {product}:".upper()
        file_name = f"inventory_{product}_{cfg.application_date()}"

    if output == "screen":
        print(report_title)
        print(tabulate(report_df, headers="keys", tablefmt="grid"))
    if output == "csv":
        file_path = os.path.join(cfg.reports_dir(), f"{file_name}.csv")
        report_df.to_csv(file_path, sep=cfg.csv_delimiter())
    if output == "json":
        file_path = os.path.join(cfg.reports_dir(), f"{file_name}.json")
        report_df.to_json(file_path, index=1, orient="records")


def report(subject: str, date_range: str, date_type: str, output: str):
    """Creates purchases or sales report."""
    # Creating a dataframe.
    if subject == "purchases":
        df = pd.read_csv(
            cfg.dataset_properties("purchases")["path"],
            delimiter=cfg.csv_delimiter(),
            index_col="id",
        )
        date_field = "date_bought"
        # Remove unneccessary columns from dataframe.
        df.drop(columns=["stock_amount", "amount_expired", "expiration_date"], inplace=True)
    if subject == "sales":
        df = pd.read_csv(
            cfg.dataset_properties("sales")["path"], delimiter=cfg.csv_delimiter(), index_col="id"
        )
        date_field = "date_sold"

    # Convert string to datetime object.
    df[date_field] = pd.to_datetime(df[date_field], format="%Y-%m-%d")

    # Convert string to float.
    df["total_price"] = pd.to_numeric(df["total_price"])

    # Preparing report variables.
    if date_type == "day" or date_type == "date":
        if date_range == "yesterday":
            the_date = helpers.date_yesterday(cfg.application_date())
        elif date_range == "today":
            the_date = cfg.application_date()
        else:
            the_date = date_range
        date_object = date.fromisoformat(the_date)
        long_date = f"{date_object.strftime('%A, %d %B %Y')}"
        report_filter = df[date_field] == the_date
    if date_type == "month":
        year_date = int(date_range[0:4])
        month_date = int(date_range[5:])
        report_filter = (df[date_field].dt.year == year_date) & (
            df[date_field].dt.month == month_date
        )
        the_date = date_range
        date_object = datetime.strptime(date_range, "%Y-%m")
        long_date = f"{date_object.strftime('%B %Y')}"
    if date_type == "quarter":
        year_date = int(date_range[0:4])
        quarter_date = int(date_range[-1])
        report_filter = (df[date_field].dt.year == year_date) & (
            df[date_field].dt.quarter == quarter_date
        )
        the_date = date_range
        quarter_split = date_range.split("-")
        long_date = f"Q{quarter_split[1]} of {quarter_split[0]}"
    if date_type == "year":
        report_filter = df[date_field].dt.year == date_range
        the_date = date_range
        long_date = date_range

    report_title = f"{subject.capitalize()} in {long_date}"
    file_name = f"{subject}_{the_date}"

    # Setting filter
    df = df.loc[report_filter]

    df[date_field] = df[date_field].dt.date

    # Create and set format for valuta
    total = df["total_price"].sum()
    df["unit_price"] = df["unit_price"].apply(lambda x: helpers.valuta_notation(float(x)))
    df["total_price"] = df["total_price"].apply(lambda x: helpers.valuta_notation(float(x)))

    if output == "screen":
        print(f"{report_title} - Total of {subject}: {helpers.valuta_notation(float(total))}")
        print(tabulate(df, headers="keys", tablefmt="pretty"))
    if output == "csv":
        file_path = os.path.join(cfg.reports_dir(), f"{file_name}.csv")
        df.to_csv(file_path, sep=cfg.csv_delimiter)
    if output == "json":
        file_path = os.path.join(cfg.reports_dir(), f"{file_name}.json")
        df.to_json(file_path, index=1, orient="records")
