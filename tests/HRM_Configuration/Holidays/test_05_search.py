import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_search_holiday(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")
    _screenshot(page, "05_search_results")
    page.get_by_role("button", name="Reset Filters").click()