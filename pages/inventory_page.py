from .base_page import BasePage


class InventoryPage(BasePage):
    path = "/inventory.html"

    @property
    def item_names(self):
        return self.page.get_by_test_id("inventory-item-name")

    @property
    def item_prices(self):
        return self.page.get_by_test_id("inventory-item-price")

    @property
    def sort_dropdown(self):
        return self.page.get_by_test_id("product-sort-container")

    @property
    def cart_badge(self):
        return self.page.get_by_test_id("shopping-cart-badge")

    def sort_by(self, option_value):  # "az", "za", "lohi", "hilo"
        self.sort_dropdown.select_option(option_value)

    def add_button(self, slug):  # e.g. "sauce-labs-backpack"
        return self.page.get_by_test_id(f"add-to-cart-{slug}")

    def remove_button(self, slug):
        return self.page.get_by_test_id(f"remove-{slug}")

    def add_to_cart(self, slug):
        self.add_button(slug).click()

    def open_cart(self):
        self.page.get_by_test_id("shopping-cart-link").click()
