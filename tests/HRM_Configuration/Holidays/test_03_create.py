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
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_label("Algeria").get_by_text("Algeria").click()
    page.get_by_role("combobox", name="Region*").click()
    page.get_by_role("option", name="West").click()
    page.get_by_role("checkbox", name="Goa South").click()
    page.get_by_role("textbox", name="Holiday Occasion *").click()
    page.get_by_role("textbox", name="Holiday Occasion *").fill("Testing-sankranthiii")
    page.get_by_role("button", name="Jul 16,").first.click()
    page.get_by_role("button", name="Friday, July 17th,").click()
    page.get_by_role("checkbox", name="Send this update to all").click()
    page.get_by_role("button", name="Create").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()
    _screenshot(page, "03_create_holiday_done")
