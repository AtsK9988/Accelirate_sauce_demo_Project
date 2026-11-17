from .base_page import BasePage


class CartPage(BasePage):
    path = "/cart.html"

    @property
    def item_names(self):
        return self.page.get_by_test_id("inventory-item-name")

    def remove(self, slug):
        self.page.get_by_test_id(f"remove-{slug}").click()

    def continue_shopping(self):
        self.page.get_by_test_id("continue-shopping").click()

    def checkout(self):
        self.page.get_by_test_id("checkout").click()
