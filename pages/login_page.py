from .base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def login(self, username, password):
        self.page.get_by_test_id("username").fill(username)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-button").click()

    @property
    def error(self):
        return self.page.get_by_test_id("error")
