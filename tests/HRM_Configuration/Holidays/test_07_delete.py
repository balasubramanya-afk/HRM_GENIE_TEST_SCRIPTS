import re
from playwright.sync_api import Page, expect


def test_delete_holiday(holidays_page: Page) -> None:
    page = holidays_page
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")
    page.get_by_role("row", name="Albania south-east Bangalore").get_by_role("button").nth(1).click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()

