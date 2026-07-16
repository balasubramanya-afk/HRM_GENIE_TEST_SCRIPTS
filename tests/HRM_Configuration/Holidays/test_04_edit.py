import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_edit_holiday(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("row", name="India South West Kerala").get_by_role("button").first.click()
    page.get_by_label("Country *").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_label("Region").click()
    page.get_by_label("south-east").get_by_text("south-east").click()
    page.locator("#branch-78").click()
    page.get_by_label("Bangalore").click()
    page.get_by_placeholder("Occasion", exact=True).click()
    page.get_by_placeholder("Occasion", exact=True).click()
    page.get_by_placeholder("Occasion", exact=True).fill("testing-pongal")
    page.get_by_label("Start Date *").click()
    page.get_by_label("Saturday, July 18th,").first.click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Start Date *").click()
    page.get_by_label("Monday, July 20th,").first.click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Tuesday, July 21st,").first.click()
    _screenshot(page, "04_edit_holiday_form")
    page.get_by_role("button", name="Update").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")
    _screenshot(page, "04_edit_holiday_done")
