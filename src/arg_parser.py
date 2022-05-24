"""Get user input from CLI."""

# Python built-in modules
import argparse
import sys


def get_parser_args() -> object:
    """Gets command and arguments from command line."""

    the_parser = argparse.ArgumentParser()

    # Subparsers for each main command.
    subparsers = the_parser.add_subparsers(title="Commands", dest="command")
    advance_parser = subparsers.add_parser(
        "advance",
        help="Set the application to a date in the future => advance <days>.",
    )
    purchase_parser = subparsers.add_parser(
        "purchase",
        help="Purchase a product => purchase <product-name> <quantity> <unit-price> <expiration-date>.",
    )
    sell_parser = subparsers.add_parser(
        "sell", help="Sell a product => sell <product-name> <quantity> <unit-price>."
    )
    inventory_parser = subparsers.add_parser(
        "inventory",
        help="Inventory of one or all products => inventory [<product-name>] <output>.",
    )
    report_parser = subparsers.add_parser(
        "report", help="Create reports => report <subject> <date-range> <output>."
    )

    # 'advance' arguments.
    advance_parser.add_argument(
        "days",
        type=int,
        choices=[0, 1, 2, 3, 4],
        metavar="<days>",
        help="Set the application date 0 - 4 days in the future (0=today, 1=tomorrow, etc.)",
    )

    # 'purchase' and 'sell' arguments.
    for sp in [purchase_parser, sell_parser]:
        sp.add_argument(
            "product",
            type=lambda s: s.lower(),  # Source: https://stackoverflow.com/a/27616814
            metavar="<product-name>",
            help="Name of the product.",
        )
        sp.add_argument("amount", type=int, metavar="<quantity>", help="Amount of the product.")
        sp.add_argument("unit_price", type=float, metavar="<unit-price>", help="Price per unit.")
    purchase_parser.add_argument(
        "expiration_date",
        metavar="<expiration_date>",
        help="Expiration date like 'yyyy-mm-dd', must be more then 5 days in the future.",
    )

    # 'inventory' and 'report' arguments.
    inventory_parser.add_argument(
        "-p",
        "--product",
        type=lambda s: s.lower(),
        metavar="<product-name>",
        help="Name of the product.",
    )
    report_parser.add_argument(
        "subject",
        type=lambda s: s.lower(),
        metavar="<subject>",
        choices=["purchases", "sales"],
        help="Choose subject from: 'purchases' or 'sales'.",
    )
    report_parser.add_argument(
        "date_range",
        type=lambda s: s.lower(),
        metavar="<date-range>",
        help="Please enter 'yesterday', 'today', a date ('yyyy-mm-dd'), month ('yyyy-mm'), quarter ('yyyy-q') or a year ('yyyy').",
    )
    for sp in [inventory_parser, report_parser]:
        sp.add_argument(
            "output",
            type=lambda s: s.lower(),  # Source: https://stackoverflow.com/a/27616814
            metavar="<output>",
            choices=[
                "screen",
                "csv",
                "json",
            ],
            help="Name of the device. Choose from 'screen', 'csv' or json.",
        )

    # Print the usage info if no command is given. Source: https://stackoverflow.com/a/29312757
    if len(sys.argv) == 1:
        the_parser.print_usage()
        the_parser.exit()

    return the_parser.parse_args()
