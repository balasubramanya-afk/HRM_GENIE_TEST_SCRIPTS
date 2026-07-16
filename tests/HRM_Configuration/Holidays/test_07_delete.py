import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_delete_holiday(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")
    page.get_by_role("row", name="Albania south-east Bangalore").get_by_role("button").nth(1).click()
    page.get_by_role("button", name="Delete").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()
    _screenshot(page, "07_delete_holiday_done")
