"""Test reports module."""
import pytest

product_fields = [
    "sum_costs",
    "sum_revenues",
    "product_name",
]


@pytest.mark.parametrize("property", product_fields)
def test_products_dataset_properties_has_crucial_fields(cfg, property):
    """Testing if crucial fields are in the products dataset."""
    the_dict = cfg.dataset_properties("products")
    the_values = the_dict.get("fields")
    assert property in the_values


purchase_fields = [
    "date_bought",
    "stock_amount",
    "amount_expired",
    "expiration_date",
    "unit_price",
    "total_price",
]


@pytest.mark.parametrize("property", purchase_fields)
def test_purchases_dataset_properties_has_crucial_fields(cfg, property):
    """Testing if crucial fields are in the products dataset."""
    the_dict = cfg.dataset_properties("purchases")
    the_values = the_dict.get("fields")
    assert property in the_values


sale_fields = [
    "date_sold",
    "total_price",
    "unit_price",
    "total_price",
]


@pytest.mark.parametrize("property", sale_fields)
def test_sales_dataset_properties_has_crucial_fields(cfg, property):
    """Testing if crucial fields are in the products dataset."""
    the_dict = cfg.dataset_properties("sales")
    the_values = the_dict.get("fields")
    assert property in the_values
