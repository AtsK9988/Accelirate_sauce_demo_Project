from .base_page import BasePage


class CheckoutPage(BasePage):
    path = "/checkout-step-one.html"

    @property
    def error(self):
        return self.page.get_by_test_id("error")

    @property
    def subtotal(self):
        return self.page.get_by_test_id("subtotal-label")

    @property
    def tax(self):
        return self.page.get_by_test_id("tax-label")

    @property
    def total(self):
        return self.page.get_by_test_id("total-label")

    @property
    def complete_header(self):
        return self.page.get_by_test_id("complete-header")

    def fill_info(self, first, last, postal):
        self.page.get_by_test_id("firstName").fill(first)
        self.page.get_by_test_id("lastName").fill(last)
        self.page.get_by_test_id("postalCode").fill(postal)

    def continue_(self):
        self.page.get_by_test_id("continue").click()

    def finish(self):
        self.page.get_by_test_id("finish").click()
