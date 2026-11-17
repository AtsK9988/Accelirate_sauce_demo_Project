import re
from decimal import Decimal

import pytest
from playwright.sync_api import expect

ITEMS = ["sauce-labs-backpack", "sauce-labs-bike-light"]


def money(text: str) -> Decimal:
    """'Item total: $39.98' -> Decimal('39.98')"""
    return Decimal(re.search(r"\$([\d.]+)", text).group(1))


@pytest.mark.smoke
def test_end_to_end_checkout(page, inventory_page, cart_page, checkout_page):
    inventory_page.open()
    for slug in ITEMS:
        inventory_page.add_to_cart(slug)
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.open_cart()
    expect(cart_page.item_names).to_have_text(["Sauce Labs Backpack", "Sauce Labs Bike Light"])

    cart_page.checkout()
    checkout_page.fill_info("Test", "User", "12345")
    checkout_page.continue_()

    expect(page).to_have_url(re.compile(r"checkout-step-two"))
    expect(checkout_page.total).to_be_visible()
    item_total = money(checkout_page.subtotal.inner_text())
    tax = money(checkout_page.tax.inner_text())
    total = money(checkout_page.total.inner_text())
    assert item_total + tax == total

    checkout_page.finish()
    expect(checkout_page.complete_header).to_have_text("Thank you for your order!")
