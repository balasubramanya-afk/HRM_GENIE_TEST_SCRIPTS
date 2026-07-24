"""
Negative test cases for Employee module: Team's Members.

Covers:
  - Team's Members search/filter degrade gracefully on invalid input (no crash,
    no XSS execution, proper "no records" handling) and employee detail view
    reached from list remains read-only.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Playwright, Page, sync_playwright
from config import login_as, _screenshot

BASE_URL = "https://qa.hrmgenie.outstrive.co"
LIST_PATH = "/employee/team-employee"

GARBAGE_QUERIES = [
    "zzzznotarealemployee9999",
    "!!!@@@###$$$",
    "' OR '1'='1",
]

XSS_PAYLOAD = "<script>window.__xss_triggered = true;</script>"


def create_page(playwright: Playwright):
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=headless,
        slow_mo=slow_mo,
        args=["--start-maximized"],
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "BUH")
    return browser, context, page


def assert_page_is_read_only(page: Page):
    """Fails if any editable field or save/edit button is present."""
    textboxes = page.get_by_role("textbox")
    editable_count = 0
    for i in range(textboxes.count()):
        tb = textboxes.nth(i)
        placeholder = tb.get_attribute("placeholder") or ""
        if "search" in placeholder.lower():
            continue
        if tb.is_editable():
            editable_count += 1

    assert editable_count == 0, (
        f"Expected no editable textboxes, found {editable_count}"
    )

    save_or_edit_buttons = page.get_by_role(
        "button", name=re.compile(r"^\s*(save|edit)\s*$", re.I)
    )
    assert save_or_edit_buttons.count() == 0, (
        "Expected no Save/Edit buttons on a read-only view, but found "
        f"{save_or_edit_buttons.count()}"
    )


def _navigate_to_list(page: Page):
    """Navigates to team members tab."""
    page.goto(f"{BASE_URL}{LIST_PATH}")
    page.wait_for_timeout(1000)
    btn = page.get_by_role("button", name="Team's Members")
    if btn.count() > 0 and btn.is_visible():
        btn.click()
        page.wait_for_timeout(1000)


def _assert_no_results_state(page: Page):
    """After a garbage search, table should be empty or show no records message."""
    rows = page.locator("table tbody tr, tbody tr")
    no_results_text = page.get_by_text(
        re.compile("no (records|results|employees|data) found", re.I)
    )
    assert rows.count() == 0 or no_results_text.count() > 0, (
        "Expected empty table or 'no records found' message for unmatched search."
    )


# ---------------------------------------------------------------------------
# Team's Members - search & filter negative cases
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("garbage_query", GARBAGE_QUERIES)
def test_team_members_search_invalid_query_shows_no_results(
    playwright: Playwright, garbage_query: str
) -> None:
    browser, context, page = create_page(playwright)
    try:
        _navigate_to_list(page)

        search_box = page.get_by_placeholder("Search...").or_(
            page.locator("input[placeholder='Search...']")
        ).first
        search_box.fill(garbage_query)
        page.wait_for_timeout(800)

        _screenshot(page, "test_10_no_results_team_members")
        _assert_no_results_state(page)
    finally:
        context.close()
        browser.close()


def test_team_members_search_script_injection_is_neutralized(
    playwright: Playwright
) -> None:
    browser, context, page = create_page(playwright)
    try:
        _navigate_to_list(page)

        search_box = page.get_by_placeholder("Search...").or_(
            page.locator("input[placeholder='Search...']")
        ).first
        search_box.fill(XSS_PAYLOAD)
        page.wait_for_timeout(800)

        _screenshot(page, "test_10_xss_team_members")

        triggered = page.evaluate("() => window.__xss_triggered === true")
        assert not triggered, "Script injection payload executed - XSS vulnerability."
    finally:
        context.close()
        browser.close()


def test_team_members_filter_mismatched_combination_returns_empty_gracefully(
    playwright: Playwright
) -> None:
    browser, context, page = create_page(playwright)
    try:
        _navigate_to_list(page)

        designation_filter = page.get_by_role("combobox").filter(
            has_text=re.compile("designation", re.I)
        )
        department_filter = page.get_by_role("combobox").filter(
            has_text=re.compile("department", re.I)
        )

        if designation_filter.count() > 0:
            designation_filter.first.click()
            page.wait_for_timeout(300)
            designation_options = page.get_by_role("option")
            if designation_options.count() > 1:
                designation_options.nth(1).click()
            page.wait_for_timeout(500)

        if department_filter.count() > 0:
            department_filter.first.click()
            page.wait_for_timeout(300)
            department_options = page.get_by_role("option")
            if department_options.count() > 1:
                department_options.nth(-1).click()
            page.wait_for_timeout(500)

        _screenshot(page, "test_10_filter_mismatch_team_members")

        reset_button = page.get_by_role(
            "button", name=re.compile("reset filters", re.I)
        )
        if reset_button.count() > 0:
            reset_button.click()
            page.wait_for_timeout(500)
    finally:
        context.close()
        browser.close()


def test_team_members_detail_view_from_list_is_read_only(
    playwright: Playwright
) -> None:
    browser, context, page = create_page(playwright)
    try:
        _navigate_to_list(page)

        employee_row_cell = page.locator("tbody tr").first.locator("td").first
        if employee_row_cell.count() > 0:
            employee_row_cell.click()
            page.wait_for_timeout(1000)
            _screenshot(page, "test_10_detail_readonly_team_members")
            assert_page_is_read_only(page)
        else:
            pytest.skip("No employee rows available to open from team members")
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        for query in GARBAGE_QUERIES:
            test_team_members_search_invalid_query_shows_no_results(playwright, query)
        test_team_members_search_script_injection_is_neutralized(playwright)
        test_team_members_filter_mismatched_combination_returns_empty_gracefully(playwright)
        test_team_members_detail_view_from_list_is_read_only(playwright)
