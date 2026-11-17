import os
import re

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption("--sauce-user", default=os.getenv("SAUCE_USER", "standard_user"))
    parser.addoption("--sauce-password", default=os.getenv("SAUCE_PASSWORD", "secret_sauce"))


@pytest.fixture(scope="session", autouse=True)
def _set_test_id_attribute(playwright):
    # Sauce Demo uses data-test="...", Playwright expects data-testid by default
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def credentials(pytestconfig):
    return pytestconfig.getoption("--sauce-user"), pytestconfig.getoption("--sauce-password")


@pytest.fixture(scope="session")
def storage_state_path(_set_test_id_attribute, browser, base_url, credentials, tmp_path_factory):
    """Log in once per session (once per xdist worker) and save the login state."""
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).open().login(*credentials)
    expect(page).to_have_url(re.compile(r"/inventory\.html"))
    context.storage_state(path=str(path))
    context.close()
    return str(path)


@pytest.fixture
def browser_context_args(browser_context_args, request):
    """Tests start logged in, unless marked with @pytest.mark.anonymous."""
    if request.node.get_closest_marker("anonymous"):
        return browser_context_args
    state = request.getfixturevalue("storage_state_path")
    return {**browser_context_args, "storage_state": state}


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)
