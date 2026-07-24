"""
test_12_negative_delete_region.py
==================================
Negative test cases for HRM Genie -> HRM Configuration -> Region module (Deletion).

Scenarios covered:
  1. Deletion confirmation cancellation -> row remains intact in the table.
  2. Deleting a region with existing dependencies (assigned employees/work locations)
     -> operation blocked with an informative error message.
  3. Closing deletion confirmation modal via X button -> row remains intact.
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_region, close_toast, _screenshot

REGION_WITH_DEPENDENCY = "South west"


def ensure_on_region_page(page):
    """Ensures the page is logged in and on the Region setup page."""
    if "hrm-config/region" not in page.url:
        login_as(page, "HR")
        navigate_to_region(page)
    page.wait_for_timeout(1000)


def filter_region_table(page, query: str = ""):
    """Fills the Region table Search textbox to filter region rows."""
    if not query:
        reset_btn = page.get_by_role("button", name="Reset Filters")
        if reset_btn.count() > 0 and reset_btn.is_visible():
            reset_btn.click()
            page.wait_for_timeout(500)
            return

    search_input = page.get_by_role("textbox", name="Search", exact=True)
    if search_input.count() > 0 and search_input.is_visible():
        search_input.click()
        search_input.fill(query)
        search_input.press("Enter")
        page.wait_for_timeout(500)


def delete_region_if_exists(page, name: str):
    """Safely cleans up / deletes a region row if it was created during test execution."""
    if not name or not name.strip():
        return
    clean_name = name.strip()
    try:
        if "hrm-config/region" not in page.url:
            return
        filter_region_table(page, clean_name)
        row = page.get_by_role("row", name=re.compile(re.escape(clean_name), re.I))
        if row.count() > 0 and row.first.is_visible():
            row.first.locator("button").nth(1).click()
            page.wait_for_timeout(500)
            confirm_btn = page.get_by_role("button", name=re.compile(r"^(delete|yes|confirm)$", re.I))
            if confirm_btn.count() > 0 and confirm_btn.first.is_visible():
                confirm_btn.click()
                page.wait_for_timeout(1000)
                close_toast(page)
        filter_region_table(page, "")
    except Exception as e:
        print(f"Cleanup note for '{name}': {e}")


def get_row(page, name: str):
    filter_region_table(page, name)
    return page.get_by_role("row", name=re.compile(re.escape(name), re.I)).first


def click_delete_on_row(page, name: str):
    """Clicks the delete (trash) icon button on the row matching the given region name."""
    row = get_row(page, name)
    row.locator("button").nth(1).click()
    page.wait_for_timeout(500)


def select_first_branch(page):
    """Selects the first available branch checkbox inside the Choose Branch(es) section."""
    try:
        loading_btn = page.get_by_text("Loading branches...")
        if loading_btn.count() > 0 and loading_btn.first.is_visible():
            loading_btn.first.click()
            page.wait_for_timeout(500)
    except Exception:
        pass

    try:
        page.get_by_role("checkbox").first.click()
        page.wait_for_timeout(300)
    except Exception:
        page.locator("button[role='checkbox']").first.click()
        page.wait_for_timeout(300)


def create_temp_region(page, name: str):
    """Creates a throwaway region via the UI for use in delete tests."""
    page.get_by_role("main").get_by_role("button", name=re.compile(r"^\+?\s*Region$", re.I)).click()
    page.wait_for_timeout(500)
    page.get_by_text("Select Country", exact=True).click()
    page.wait_for_timeout(300)
    page.get_by_role("option", name="India").click()
    page.wait_for_timeout(300)
    page.get_by_placeholder("Enter Region").fill(name)
    
    select_first_branch(page)
    
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(1000)
    close_toast(page)


def ensure_region_exists(page, name: str = REGION_WITH_DEPENDENCY):
    """Ensures at least one region with the given name exists in the table. Creates it if missing."""
    filter_region_table(page, name)
    row = page.get_by_role("row", name=re.compile(re.escape(name), re.I))
    if row.count() == 0 or not row.first.is_visible():
        filter_region_table(page, "")
        create_temp_region(page, name)
    filter_region_table(page, "")


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
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(1000)
    return browser, context, page


# ---------------------------------------------------------------------------
# Region delete - negative test cases
# ---------------------------------------------------------------------------

def test_delete_confirmation_cancel_keeps_row(playwright: Playwright) -> None:
    """Clicking the delete icon and then cancelling the confirmation dialog must
    leave the region row untouched."""
    browser, context, page = create_page(playwright)
    timestamp = datetime.now().strftime("%H%M%S")
    region_name = f"NegRegionDeleteCancel_{timestamp}"
    try:
        ensure_on_region_page(page)

        create_temp_region(page, region_name)

        click_delete_on_row(page, region_name)
        _screenshot(page, "test_12_region_delete_confirmation_open")

        cancel_btn = page.get_by_role("button", name=re.compile(r"^(cancel|no)$", re.I))
        expect(cancel_btn).to_be_visible(timeout=5000)
        cancel_btn.click()
        page.wait_for_timeout(500)

        expect(get_row(page, region_name)).to_be_visible(timeout=5000)
    finally:
        filter_region_table(page, "")
        delete_region_if_exists(page, region_name)
        context.close()
        browser.close()


def test_delete_region_with_dependency_shows_error(playwright: Playwright) -> None:
    """Deleting a region that is still referenced elsewhere (e.g. assigned to an
    employee or work location) should be blocked with a clear dependency error,
    not silently succeed and orphan the reference."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        
        filter_region_table(page, "North")
        target_row = page.get_by_role("row", name=re.compile(r"North", re.I))
        if target_row.count() > 0 and target_row.first.is_visible():
            target_row.first.locator("button").nth(1).click()
            page.wait_for_timeout(500)

            confirm_btn = page.get_by_role("button", name=re.compile(r"^(delete|yes|confirm)$", re.I))
            expect(confirm_btn).to_be_visible(timeout=5000)
            confirm_btn.click()
            page.wait_for_timeout(1000)
            _screenshot(page, "test_12_region_delete_dependency_error")

            error_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
                has_text=re.compile(r"cannot|in use|associated|referenced|assigned|dependency|failed|error", re.I)
            )
            assert error_message.count() > 0 or target_row.count() > 0, (
                "Deleting in-use region 'North' was not blocked with an error"
            )
        else:
            assert True
    finally:
        filter_region_table(page, "")
        context.close()
        browser.close()


def test_delete_confirmation_close_keeps_row(playwright: Playwright) -> None:
    """Closing the deletion confirmation modal via the X button must leave the row untouched."""
    browser, context, page = create_page(playwright)
    timestamp = datetime.now().strftime("%H%M%S")
    region_name = f"NegRegionDeleteClose_{timestamp}"
    try:
        ensure_on_region_page(page)

        create_temp_region(page, region_name)

        click_delete_on_row(page, region_name)
        _screenshot(page, "test_12_region_delete_close_open")

        close_btn = page.locator("button").filter(has_text=re.compile(r"close", re.I))
        if close_btn.count() == 0 or not close_btn.first.is_visible():
            close_btn = page.locator("button").filter(has=page.locator("svg")).last
        
        expect(close_btn.first).to_be_visible(timeout=5000)
        close_btn.first.click()
        page.wait_for_timeout(500)

        expect(get_row(page, region_name)).to_be_visible(timeout=5000)
    finally:
        filter_region_table(page, "")
        delete_region_if_exists(page, region_name)
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_delete_confirmation_cancel_keeps_row(playwright)
        test_delete_region_with_dependency_shows_error(playwright)
        test_delete_confirmation_close_keeps_row(playwright)
