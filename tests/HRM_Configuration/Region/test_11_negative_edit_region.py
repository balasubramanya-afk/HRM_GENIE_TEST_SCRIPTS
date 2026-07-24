"""
test_11_negative_edit_region.py
================================
Negative test cases for HRM Genie -> HRM Configuration -> Region module (Editing).

Scenarios covered:
  1. Stale region edit (editing a region that was deleted elsewhere or via back navigation)
     -> graceful not-found/error state displayed, no incorrect record updated.
  2. Duplicate region name on update -> error message displayed, duplicate update blocked.
  3. Empty mandatory fields on edit -> validation message shown, modal remains open.
  4. Cancellation of edit dialog -> changed values discarded, original row preserved.
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

EXISTING_REGION_NAME = "South west"


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


def click_edit_on_row(page, name: str):
    row = get_row(page, name)
    row.locator("button").nth(0).click()
    page.wait_for_timeout(500)


def click_delete_on_row(page, name: str):
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
    """Creates a throwaway region via the UI for use in edit/delete tests."""
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


def ensure_region_exists(page, name: str = EXISTING_REGION_NAME):
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
# Region edit - negative test cases
# ---------------------------------------------------------------------------

def test_edit_after_region_deleted_shows_not_found(playwright: Playwright) -> None:
    """If a region is deleted and the user then tries to act on a stale reference
    to it (e.g. via browser back navigation to a cached list), attempting to edit
    it should show a graceful not-found/error state rather than a broken or blank
    form, and must not silently edit a different region."""
    browser, context, page = create_page(playwright)
    timestamp = datetime.now().strftime("%H%M%S")
    region_name = f"NegRegionStaleEdit_{timestamp}"
    try:
        ensure_on_region_page(page)

        create_temp_region(page, region_name)

        # Delete the region
        click_delete_on_row(page, region_name)
        confirm_btn = page.get_by_role("button", name=re.compile(r"^(delete|yes|confirm)$", re.I))
        expect(confirm_btn).to_be_visible(timeout=5000)
        confirm_btn.click()
        page.wait_for_timeout(1000)
        close_toast(page)

        # Simulate a stale reference: navigate back or check stale row interaction
        page.go_back()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_11_region_stale_list_after_back")

        stale_row = page.get_by_role("row", name=re.compile(re.escape(region_name), re.I))
        if stale_row.count() > 0:
            stale_row.first.locator("button").nth(0).click()
            page.wait_for_timeout(1000)
            _screenshot(page, "test_11_region_stale_edit_attempt")

            not_found_message = page.get_by_text(re.compile(r"not found|no longer exists|unavailable", re.I))
            edit_heading = page.get_by_role("heading", name=re.compile(r"edit region", re.I))

            assert not_found_message.count() > 0 or edit_heading.count() == 0, (
                "Editing a deleted region's stale row opened an edit form instead of "
                "showing a not-found/error state"
            )
        else:
            page.reload(wait_until="networkidle")
            page.wait_for_timeout(1000)
            expect(get_row(page, region_name)).to_have_count(0, timeout=5000)
    finally:
        delete_region_if_exists(page, region_name)
        context.close()
        browser.close()


def test_edit_region_duplicate_name_shows_error(playwright: Playwright) -> None:
    """Editing an existing region and updating its name to match another region's name
    should be rejected with a duplicate name validation error."""
    browser, context, page = create_page(playwright)
    timestamp = datetime.now().strftime("%H%M%S")
    temp_name = f"NegRegionEditDup_{timestamp}"
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        create_temp_region(page, temp_name)

        click_edit_on_row(page, temp_name)
        page.wait_for_timeout(500)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(EXISTING_REGION_NAME)
        else:
            page.get_by_placeholder("Enter Region").fill(EXISTING_REGION_NAME)

        _screenshot(page, "test_11_region_edit_duplicate_name_before_update")

        page.get_by_role("button", name=re.compile(r"^(update|save)$", re.I)).click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_11_region_edit_duplicate_name_after_update")

        duplicate_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
            has_text=re.compile(r"already exists|duplicate|already (in use|taken)", re.I)
        )
        edit_modal_open = page.get_by_role("heading", name=re.compile(r"edit region", re.I)).is_visible()

        assert duplicate_message.count() > 0 or edit_modal_open, (
            "Updating region to a duplicate name was not blocked"
        )

        # Cleanup modal
        cancel_btn = page.get_by_role("button", name="Cancel")
        if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
            cancel_btn.first.click()
    finally:
        delete_region_if_exists(page, temp_name)
        context.close()
        browser.close()


def test_edit_region_empty_fields_shows_validation(playwright: Playwright) -> None:
    """Clearing mandatory fields (e.g. Region name) while editing should trigger validation
    and block the update operation."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        click_edit_on_row(page, EXISTING_REGION_NAME)
        page.wait_for_timeout(500)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill("")
        else:
            page.get_by_placeholder("Enter Region").fill("")

        _screenshot(page, "test_11_region_edit_empty_fields")

        page.get_by_role("button", name=re.compile(r"^(update|save)$", re.I)).click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_11_region_edit_empty_after_submit")

        validation_message = page.get_by_text(re.compile(r"required|is mandatory|please enter", re.I))
        expect(validation_message.first).to_be_visible(timeout=5000)

        cancel_btn = page.get_by_role("button", name="Cancel")
        if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
            cancel_btn.first.click()
    finally:
        filter_region_table(page, "")
        context.close()
        browser.close()


def test_cancel_edit_discards_changes(playwright: Playwright) -> None:
    """Modifying fields in the edit region modal and clicking Cancel should discard
    the changes without altering the original record."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        click_edit_on_row(page, EXISTING_REGION_NAME)
        page.wait_for_timeout(500)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill("Temporary Modified Name")
        else:
            page.get_by_placeholder("Enter Region").fill("Temporary Modified Name")

        _screenshot(page, "test_11_region_edit_cancel_before")

        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(500)

        # Original row must still exist with unchanged name
        expect(get_row(page, EXISTING_REGION_NAME)).to_be_visible(timeout=5000)
        expect(page.get_by_role("row", name="Temporary Modified Name")).to_have_count(0, timeout=3000)
    finally:
        filter_region_table(page, "")
        delete_region_if_exists(page, "Temporary Modified Name")
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_edit_after_region_deleted_shows_not_found(playwright)
        test_edit_region_duplicate_name_shows_error(playwright)
        test_edit_region_empty_fields_shows_validation(playwright)
        test_cancel_edit_discards_changes(playwright)
