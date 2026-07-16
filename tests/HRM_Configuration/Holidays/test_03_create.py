import re
from playwright.sync_api import Page, expect


def test_create_holiday(holidays_page: Page) -> None:
    page = holidays_page
    page.get_by_role("button", name="+ New Holiday").click()
    page.get_by_label("Country *").click()
    page.get_by_label("India").click()
    page.get_by_label("Region*").click()
    page.get_by_label("west", exact=True).click()
    page.get_by_label("Region*").click()
    page.get_by_label("South West").get_by_text("South West").click()
    page.get_by_label("Kerala").click()
    page.get_by_placeholder("e.g. Independence Day").click()
    page.get_by_placeholder("e.g. Independence Day").fill("testing-diwali")
    page.get_by_label("Start Date *").click()
    page.get_by_label("Friday, July 17th,").first.click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Friday, July 17th, 2026,").first.click()
    page.get_by_label("Friday, July 17th,").first.click()
    page.locator("div").filter(has_text=re.compile(r"^Send this update to all employees$")).first.click()
    page.get_by_role("button", name="Create").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()

