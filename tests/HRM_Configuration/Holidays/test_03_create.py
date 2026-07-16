import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_create_holiday(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
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
    _screenshot(page, "03_create_holiday_form")
    page.get_by_role("button", name="Create").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()
    _screenshot(page, "03_create_holiday_done")
