import pytest
from playwright.sync_api import expect


@pytest.mark.regression
@pytest.mark.parametrize(
    "first, last, postal, expected_error",
    [
        ("", "User", "12345", "First Name is required"),
        ("Test", "", "12345", "Last Name is required"),
        ("Test", "User", "", "Postal Code is required"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code"],
)
def test_checkout_form_validation(inventory_page, cart_page, checkout_page,
                                  first, last, postal, expected_error):
    inventory_page.open()
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.open_cart()
    cart_page.checkout()

    checkout_page.fill_info(first, last, postal)
    checkout_page.continue_()

    expect(checkout_page.error).to_contain_text(expected_error)
