import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot


def test_sort_combinations(page: Page) -> None:
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()
    page.wait_for_load_state("networkidle")
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_role("button", name="Reset Filters").click()

    # Use dynamic regex matching for the date range filter button
    date_filter_btn = page.get_by_role("button", name=re.compile(r"to \d{2}-\d{2}-\d{4}"))

    date_filter_btn.click()
    page.get_by_label("Saturday, June 20th, 2026,").first.dblclick()
    page.get_by_label("Monday, July 20th,").first.dblclick()
    page.get_by_label("Tuesday, July 21st,").first.click()
    page.get_by_text("Holidays+ New Holiday").click()

    date_filter_btn.click()
    page.get_by_role("button", name="Today", exact=True).dblclick()

    date_filter_btn.click()
    page.get_by_role("button", name="Yesterday").click()

    # Last 14 days
    date_filter_btn.click()
    page.get_by_role("button", name="Last 14 days").click()

    date_filter_btn.click()
    page.get_by_text("TodayYesterdayLast 7 daysLast").click()

    # This Week
    date_filter_btn.click()
    page.get_by_role("button", name="This Week").click()

    # Last Week
    date_filter_btn.click()
    page.get_by_role("button", name="Last Week").click()

    # This Month
    date_filter_btn.click()
    page.get_by_role("button", name="This Month").click()

    # Last Month
    date_filter_btn.click()
    page.get_by_role("button", name="Last Month").click()
    _screenshot(page, "06_sort_combinations")
