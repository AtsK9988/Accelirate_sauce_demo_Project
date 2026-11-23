from playwright.sync_api import Page, expect

Base_Url ="https://www.saucedemo.com/"

def login(page:Page, username:str, password:str)-> None:
      page.goto(Base_Url)
      page.get_by_placeholder("Username").fill(username)
      page.get_by_placeholder("Password").fill(password)
      page.get_by_role("button", name="Login").click()

# 1. Practice: locators, fill, click, URL and text assertions
def test_valid_login(page:Page):
      login("standard_user","secret_sauce")
      expect(page).to_have_url(f"{Base_Url}/inventory.html")


