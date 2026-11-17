import re

import pytest
from playwright.sync_api import expect


@pytest.mark.anonymous
@pytest.mark.smoke
def test_valid_login_lands_on_inventory(page, login_page, credentials):
    login_page.open().login(*credentials)
    expect(page).to_have_url(re.compile(r"/inventory\.html"))


@pytest.mark.anonymous
@pytest.mark.regression
@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["locked_out_user", "empty_username", "empty_password"],
)
def test_invalid_login_shows_error(login_page, username, password, expected_error):
    login_page.open().login(username, password)
    expect(login_page.error).to_contain_text(expected_error)
