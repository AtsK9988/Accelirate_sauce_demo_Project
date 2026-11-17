import pytest
from playwright.sync_api import expect

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


@pytest.mark.smoke
def test_remove_item_updates_buttons_and_badge(inventory_page, cart_page):
    inventory_page.open()
    inventory_page.add_to_cart(BACKPACK)
    inventory_page.add_to_cart(BIKE_LIGHT)
    inventory_page.open_cart()

    cart_page.remove(BACKPACK)
    cart_page.continue_shopping()

    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.add_button(BACKPACK)).to_be_visible()
    expect(inventory_page.remove_button(BIKE_LIGHT)).to_be_visible()
