import re
from playwright.sync_api import Page, expect


def test_search_holiday(holidays_page: Page) -> None:
    page = holidays_page
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")
    page.get_by_role("button", name="Reset Filters").click()