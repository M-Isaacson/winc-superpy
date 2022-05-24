"""Execute actions on the data."""

# Local modules:
import settings
import app_data
import helpers
import theming

cfg = settings.Settings()


def update_product(update_type: str, new_values: tuple) -> bool:
    """
    Update a product with new values. The new_values tuple has various length
    depending on the update_type.
    The items in the tuple are: 0:id, 1:amount, 2:total price of sale or purchase
    """
    if update_type in ["stock", "purchase", "sell"]:
        products = app_data.ReadWriteCSV(cfg.dataset_properties("products"))
        # Get  record to change (the id is the first value in the new_values tuple.)
        old_values = products.read_record(new_values[0])
        # Setting base settings for new record. Some values needs to be
        # updated but some don't. So to avoid to write out all the fields
        # again and again, only the appropriate fields will be changed based
        # on the update type.
        new_record = {
            "id": old_values["id"],
            "product_name": old_values["product_name"],
            "total_bought": old_values["total_bought"],
            "total_sold": old_values["total_sold"],
            "total_in_stock": old_values["total_in_stock"],
            "total_expired": old_values["total_expired"],
            "sum_costs": old_values["sum_costs"],
            "sum_revenues": old_values["sum_revenues"],
        }
        if update_type == "stock":
            total_in_stock = int(old_values["total_in_stock"]) - new_values[1]
            total_expired = int(old_values["total_expired"]) + new_values[1]

            new_record.update({"total_in_stock": str(total_in_stock)})
            new_record.update({"total_expired": str(total_expired)})

        elif update_type == "purchase":
            total_bought = int(old_values["total_bought"]) + new_values[1]
            total_in_stock = int(old_values["total_in_stock"]) + new_values[1]
            sum_costs = round((float(old_values["sum_costs"]) + new_values[2]), 2)

            new_record.update({"total_bought": str(total_bought)})
            new_record.update({"total_in_stock": str(total_in_stock)})
            new_record.update({"sum_costs": str(sum_costs)})

        elif update_type == "sell":
            total_sold = int(old_values["total_sold"]) + new_values[1]
            total_in_stock = int(old_values["total_in_stock"]) - new_values[1]
            sum_revenues = round((float(old_values["sum_revenues"]) + new_values[2]), 2)

            new_record.update({"total_sold": str(total_sold)})
            new_record.update({"total_in_stock": str(total_in_stock)})
            new_record.update({"sum_revenues": str(sum_revenues)})

        else:
            return False
        products.update_record(new_record)
        return True


def update_stock():
    """Products with overdue expiration dates will be removed from stock."""
    # Create data set to work with.
    purchases = app_data.ReadWriteCSV(cfg.dataset_properties("purchases"))
    stock_data = purchases.read_all_from_csv()
    # The update_counter keeps track of the amount of updates occurred
    update_counter = 0
    for row in stock_data:
        # Only if stock amount is greater then 0, it is worth checking the date.
        if int(row["stock_amount"]) > 0:
            # Expiration is overdue if date is today or earlier.
            if helpers.days_between_dates(cfg.application_date(), row["expiration_date"]) < 1:
                # All conditions are met to update the current record.
                amount_expired = int(row["stock_amount"])
                # Update the product record.
                if update_product("stock", (row["product_id"], amount_expired)) is False:
                    raise ValueError(f"Could not update product ({row['product_id']})!")
                # Update stock_data record.
                row["stock_amount"] = "0"
                row["amount_expired"] = amount_expired
                update_counter += 1
    if update_counter > 0:
        # Overwrite complete purchase csv file.
        purchases.write_all_to_csv(stock_data)
        theming.rich_msg(
            f"Stock has been checked: {update_counter} product items were expired and removed from stock.\n",
            "info",
        )


def advance(days: int):
    """Sets application date to a date in the future or back to today."""
    cfg.set_days_advanced(days)
    theming.rich_header(f" SUPERPY {cfg.application_date(long_date=True)} ")
    theming.rich_msg(f"Application date has been set to {cfg.application_date()}.\n", "success")


def purchase(product_name: str, amount: int, price: float, expiration: str):
    """Purchase a product."""
    purchases = app_data.ReadWriteCSV(cfg.dataset_properties("purchases"))
    products = app_data.ReadWriteCSV(cfg.dataset_properties("products"))
    # Create new purchase id.
    purchase_id = purchases.create_record_id()
    # Calculate total price of purchase.
    total_price = round(price * amount, 2)
    # Get product_id
    product_id = products.get_record_id(product_name, "product_name")
    # Append new record to purchases.
    purchases.append_record(
        {
            "id": purchase_id,
            "product_id": product_id,
            "product_name": product_name,
            "amount_bought": str(amount),
            "date_bought": cfg.application_date(),
            "unit_price": str(price),
            "total_price": str(total_price),
            "stock_amount": str(amount),
            "expiration_date": str(expiration),
            "amount_expired": "0",
        }
    )
    # Update the totals in the products file.
    if update_product("purchase", (product_id, amount, total_price)):
        theming.rich_msg(
            f"{str(amount)} {product_name} (with a price of {helpers.valuta_notation(price)} each) were purchased for a total of {helpers.valuta_notation(total_price)}\n",
            "success",
        )
    else:
        raise ValueError(f"Something went wrong while updating product ('{product_id}') values!")


def sell(product_name: str, amount: int, price: float):
    """Sell a product."""
    sales = app_data.ReadWriteCSV(cfg.dataset_properties("sales"))
    products = app_data.ReadWriteCSV(cfg.dataset_properties("products"))
    purchases = app_data.ReadWriteCSV(cfg.dataset_properties("purchases"))
    sale_id = sales.create_record_id()
    product_id = products.get_record_id(product_name, "product_name")
    total_price = round(price * amount, 2)
    sales.append_record(
        {
            "id": sale_id,
            "product_id": product_id,
            "product_name": product_name,
            "amount_sold": str(amount),
            "date_sold": cfg.application_date(),
            "unit_price": str(price),
            "total_price": str(total_price),
        }
    )
    # Update records in purchase/stock file.
    # Because the supermarkt's policy on sales is First In First Out, the amount
    # must be substracted of the oldest purchase, then the next oldest, etc.
    purchases_data = purchases.read_all_from_csv()
    # Sorting on expiration date to access oldest first.
    purchases_sorted = sorted(purchases_data, key=lambda k: k["expiration_date"])
    # Store the amount sold in a variable which will decrease when iterating over purchases
    amount_sold = amount
    # Iterate over all purchases untill amount_sold = 0
    for row in purchases_sorted:
        if amount_sold > 0:
            if int(row["stock_amount"]) > 0 and row["product_id"] == product_id:
                # Create integer to calculate with
                stock_amount = int(row["stock_amount"])
                # Either the amount sold is greater then or equal to the amount
                # in stock of current record
                if amount_sold >= stock_amount:
                    amount_sold = amount_sold - stock_amount
                    stock_amount = 0
                # or the amount sold is smaller.
                else:
                    stock_amount = stock_amount - amount_sold
                    amount_sold = 0
                # Update the amount left in stock.
                row["stock_amount"] = str(stock_amount)
        else:
            # Every record has been passed or the amount_sold is 0.
            break
    # Overwrite complete purchase csv file.
    purchases.write_all_to_csv(purchases_sorted)
    # Update the totals in de products file.
    if update_product("sell", (product_id, amount, total_price)):
        theming.rich_msg(
            f"{str(amount)} {product_name} (with a price of {helpers.valuta_notation(price)} each) were sold for a total of {helpers.valuta_notation(total_price)}\n",
            "success",
        )
    else:
        raise ValueError(f"Something went wrong while updating product ('{product_id}') values!")
