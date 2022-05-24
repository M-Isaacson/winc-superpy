"""Main script."""

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Python built-in modules:
import os

# Local modules:
import settings
import theming
import arg_parser
import checks
import actions
import reports


def main():
    """Main application script."""

    # Create settings object.
    cfg = settings.Settings()

    # Create application files and reports dir, if they do not exist.
    if not os.path.exists(cfg.app_files_dir()):
        os.makedirs(cfg.app_files_dir())
    if not os.path.exists(cfg.reports_dir()):
        os.makedirs(cfg.reports_dir())

    # Print application header.
    theming.rich_header(f" SUPERPY {cfg.application_date(long_date=True)} ")

    # If there are products with overdue expiration dates then update stock accordingly.
    actions.update_stock()

    # Get arguments from argsparser.
    args = arg_parser.get_parser_args()

    # Catching errors not caught by argparser and processing accordingly.
    if args.command == "advance":
        actions.advance(args.days)

    elif args.command == "purchase":
        if checks.product_available(args.product, args.command):
            if checks.valid_date_type(args.expiration_date, args.command) == "date":
                actions.purchase(args.product, args.amount, args.unit_price, args.expiration_date)

    elif args.command == "sell":
        if checks.product_available(args.product, args.command):
            if checks.amount_available(args.amount, args.product):
                actions.sell(args.product, args.amount, args.unit_price)

    elif args.command == "inventory":
        if args.product is None:
            reports.inventory("all", args.output)
        elif checks.product_available(args.product, args.command):
            reports.inventory(args.product, args.output)

    elif args.command == "report":
        date_type = checks.valid_date_type(args.date_range, args.command)
        if date_type is not None:
            reports.report(args.subject, args.date_range, date_type, args.output)


if __name__ == "__main__":
    main()
