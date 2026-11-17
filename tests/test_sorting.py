import pytest
from playwright.sync_api import expect


@pytest.mark.regression
def test_sort_price_low_to_high(inventory_page):
    inventory_page.open()
    prices = [float(t.replace("$", "")) for t in inventory_page.item_prices.all_inner_texts()]
    expected = [f"${p:.2f}" for p in sorted(prices)]

    inventory_page.sort_by("lohi")

    expect(inventory_page.item_prices).to_have_text(expected)


@pytest.mark.regression
def test_sort_name_z_to_a(inventory_page):
    inventory_page.open()
    expected = sorted(inventory_page.item_names.all_inner_texts(), reverse=True)

    inventory_page.sort_by("za")

    expect(inventory_page.item_names).to_have_text(expected)
