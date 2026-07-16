import re
from playwright.sync_api import Page, expect


def test_login_and_navigate_to_holidays(logged_in_page: Page) -> None:
    page = logged_in_page
    page.goto("https://qa.hrmgenie.outstrive.co/")
    page.wait_for_load_state("networkidle")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")