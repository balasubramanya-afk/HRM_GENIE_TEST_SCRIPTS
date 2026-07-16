import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_login_and_navigate_to_holidays(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "01_login_navigate_holidays")