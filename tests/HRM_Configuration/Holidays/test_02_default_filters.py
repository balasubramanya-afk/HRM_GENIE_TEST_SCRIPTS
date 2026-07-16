import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_default_filters(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("button", name="Holidays").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("All Countries").click()
    page.get_by_role("button", name=re.compile(r"to \d{2}-\d{2}-\d{4}")).click()
    page.get_by_role("button", name="June 2026").click()
    page.get_by_role("dialog").click()
    page.get_by_text("Holidays+ New Holiday").click()
    _screenshot(page, "02_default_filters")