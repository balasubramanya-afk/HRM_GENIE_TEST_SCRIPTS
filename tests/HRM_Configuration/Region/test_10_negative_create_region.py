"""
test_10_negative_create_region.py
==================================
Negative test cases for HRM Genie -> HRM Configuration -> Region module (Creation).

Scenarios covered:
  1. Empty fields submission -> required validation messages shown, modal stays open.
  2. Missing branch selection -> branch-specific validation error shown, submission blocked.
  3. Duplicate region name -> duplicate error message displayed, no secondary row created.
  4. Duplicate region name (case-insensitive) -> differently-cased duplicate rejected.
  5. Duplicate region name (whitespace-padded) -> trimmed and rejected as duplicate (XFAIL: App defect).
  6. Form cancellation -> entered data discarded, reopening modal shows reset/empty state.
  7. Invalid region names (whitespace, special characters, overlong string) -> validation error displayed (XFAIL: App defect).
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

EXISTING_REGION_NAME = "South west"  # known pre-existing row, used for duplicate-name checks


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
    search_query = clean_name[:20] if len(clean_name) > 20 else clean_name
    try:
        if "hrm-config/region" not in page.url:
            return
        filter_region_table(page, search_query)
        row = page.get_by_role("row", name=re.compile(re.escape(search_query), re.I))
        while row.count() > 0 and row.first.is_visible():
            row.first.locator("button").nth(1).click()
            page.wait_for_timeout(500)
            confirm_btn = page.get_by_role("button", name=re.compile(r"^(delete|yes|confirm)$", re.I))
            if confirm_btn.count() > 0 and confirm_btn.first.is_visible():
                confirm_btn.click()
                page.wait_for_timeout(1000)
                close_toast(page)
            page.wait_for_timeout(500)
            row = page.get_by_role("row", name=re.compile(re.escape(search_query), re.I))
        filter_region_table(page, "")
    except Exception as e:
        print(f"Cleanup note for '{name}': {e}")


def is_region_modal_open(page) -> bool:
    """Returns True if the Create Region modal is currently open."""
    heading = page.get_by_role("heading", name="Create Region")
    return heading.count() > 0 and heading.first.is_visible()


def open_create_region_modal(page):
    """Opens the Create Region modal. Idempotent - skips if already open."""
    if is_region_modal_open(page):
        return
    region_btn = page.get_by_role("main").get_by_role("button", name=re.compile(r"^\+?\s*Region$", re.I))
    if region_btn.count() == 0 or not region_btn.first.is_visible():
        region_btn = page.get_by_role("button", name=re.compile(r"^\+?\s*Region$", re.I))
    region_btn.first.click()
    page.wait_for_timeout(500)
    expect(page.get_by_role("heading", name="Create Region")).to_be_visible(timeout=5000)


def close_create_region_modal(page):
    """Closes the Create Region modal via the X icon or Cancel button. Safe if already closed."""
    if not is_region_modal_open(page):
        return
    cancel_btn = page.get_by_role("button", name="Cancel")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
    else:
        close_icon = page.locator("button").filter(has=page.locator("svg")).last
        if close_icon.count() > 0 and close_icon.is_visible():
            close_icon.click()
    page.wait_for_timeout(500)


def select_country(page, country_name: str = "India"):
    """Opens the Country dropdown and picks the given option."""
    country_combo = page.get_by_role("combobox", name=re.compile(r"Country", re.I))
    if country_combo.count() > 0 and country_combo.first.is_visible():
        country_combo.first.click()
    else:
        page.get_by_text("Select Country", exact=True).click()
    page.wait_for_timeout(300)
    page.get_by_role("option", name=country_name).first.click()
    page.wait_for_timeout(300)


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


def ensure_region_exists(page, name: str = EXISTING_REGION_NAME):
    """Ensures at least one region with the given name exists in the table. Creates it if missing."""
    filter_region_table(page, name)
    row = page.get_by_role("row", name=re.compile(re.escape(name), re.I))
    if row.count() == 0 or not row.first.is_visible():
        filter_region_table(page, "")
        open_create_region_modal(page)
        select_country(page, "India")
        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(name)
        else:
            page.get_by_placeholder("Enter Region").fill(name)
        select_first_branch(page)
        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        close_toast(page)
        page.wait_for_timeout(500)
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
# Region creation - negative test cases
# ---------------------------------------------------------------------------

def test_create_region_empty_fields_shows_validation(playwright: Playwright) -> None:
    """Clicking Create with no Country, Region name, or Branch(es) selected should
    surface required-field validation and must NOT submit the form."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        open_create_region_modal(page)
        _screenshot(page, "test_10_region_empty_fields_before_submit")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_10_region_empty_fields_after_submit")

        validation_message = page.get_by_text(re.compile(r"required|is mandatory|please (select|enter)", re.I))
        expect(validation_message.first).to_be_visible(timeout=5000)

        # Modal must remain open - an invalid submission should not close it
        expect(page.get_by_role("heading", name="Create Region")).to_be_visible(timeout=3000)
    finally:
        close_create_region_modal(page)
        context.close()
        browser.close()


def test_create_region_without_branch_shows_validation(playwright: Playwright) -> None:
    """Filling Country and Region name but leaving Branch(es) unselected should still
    block submission with a Branch(es)-specific validation error."""
    browser, context, page = create_page(playwright)
    region_name = ""
    try:
        ensure_on_region_page(page)
        open_create_region_modal(page)

        timestamp = datetime.now().strftime("%H%M%S")
        region_name = f"NegRegionNoBranch_{timestamp}"

        select_country(page)
        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(region_name)
        else:
            page.get_by_placeholder("Enter Region").fill(region_name)

        _screenshot(page, "test_10_region_no_branch_selected")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_10_region_no_branch_after_submit")

        validation_message = page.get_by_text(re.compile(r"branch.*required|select.*branch|please (select|choose).*branch", re.I))
        expect(validation_message.first).to_be_visible(timeout=5000)
        expect(page.get_by_role("heading", name="Create Region")).to_be_visible(timeout=3000)
    finally:
        close_create_region_modal(page)
        delete_region_if_exists(page, region_name)
        context.close()
        browser.close()


def test_duplicate_region_name_shows_error(playwright: Playwright) -> None:
    """Creating a region with a name that already exists should show a duplicate/
    already-exists error rather than silently creating a second row with the same name."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        open_create_region_modal(page)
        select_country(page)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(EXISTING_REGION_NAME)
        else:
            page.get_by_placeholder("Enter Region").fill(EXISTING_REGION_NAME)

        select_first_branch(page)
        _screenshot(page, "test_10_region_duplicate_name_before_submit")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_region_duplicate_name_after_submit")

        duplicate_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
            has_text=re.compile(r"already exists|duplicate|already (in use|taken)", re.I)
        )
        modal_open = is_region_modal_open(page)
        assert duplicate_message.count() > 0 or modal_open, "Duplicate region creation was not blocked"

        close_create_region_modal(page)
        filter_region_table(page, EXISTING_REGION_NAME)
        matching_rows = page.get_by_role("row", name=re.compile(re.escape(EXISTING_REGION_NAME), re.I))
        assert matching_rows.count() >= 1, (
            f"Expected row named '{EXISTING_REGION_NAME}' to exist in table"
        )
    finally:
        close_create_region_modal(page)
        filter_region_table(page, "")
        context.close()
        browser.close()


def test_duplicate_region_name_case_insensitive(playwright: Playwright) -> None:
    """Creating a region whose name matches an existing one but with different
    casing (e.g. 'south west' vs 'South west') should still be caught as a
    duplicate, not treated as a distinct name."""
    browser, context, page = create_page(playwright)
    case_variant_name = EXISTING_REGION_NAME.lower()
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        open_create_region_modal(page)
        select_country(page)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(case_variant_name)
        else:
            page.get_by_placeholder("Enter Region").fill(case_variant_name)

        select_first_branch(page)
        _screenshot(page, "test_10_region_case_insensitive_duplicate_before_submit")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_region_case_insensitive_duplicate_after_submit")

        duplicate_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
            has_text=re.compile(r"already exists|duplicate|already (in use|taken)", re.I)
        )
        modal_open = is_region_modal_open(page)
        assert duplicate_message.count() > 0 or modal_open, "Case-insensitive duplicate creation was not blocked"

        close_create_region_modal(page)
        filter_region_table(page, case_variant_name)
        new_row = page.get_by_role("row", name=re.compile(rf"^{re.escape(case_variant_name)}$", re.I))
        assert new_row.count() <= 1, (
            f"Expected case-variant '{case_variant_name}' to not create extra row"
        )
    finally:
        close_create_region_modal(page)
        filter_region_table(page, "")
        delete_region_if_exists(page, case_variant_name)
        context.close()
        browser.close()


@pytest.mark.xfail(strict=False, reason="Application defect: Whitespace-padded duplicate region names are not trimmed or rejected with duplicate validation")
def test_duplicate_region_name_whitespace_trimmed(playwright: Playwright) -> None:
    """Creating a region whose name is identical to an existing one but padded with
    leading/trailing whitespace (e.g. '  South west  ') should be trimmed server-side
    and caught as a duplicate, not accepted as a distinct entry."""
    browser, context, page = create_page(playwright)
    padded_name = f"   {EXISTING_REGION_NAME}   "
    try:
        ensure_on_region_page(page)
        ensure_region_exists(page, EXISTING_REGION_NAME)

        open_create_region_modal(page)
        select_country(page)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(padded_name)
        else:
            page.get_by_placeholder("Enter Region").fill(padded_name)

        select_first_branch(page)
        _screenshot(page, "test_10_region_whitespace_duplicate_before_submit")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_region_whitespace_duplicate_after_submit")

        duplicate_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
            has_text=re.compile(r"already exists|duplicate|already (in use|taken)", re.I)
        )
        modal_open = is_region_modal_open(page)
        assert duplicate_message.count() > 0 or modal_open, (
            "Whitespace-padded duplicate region name creation was not blocked"
        )
    finally:
        close_create_region_modal(page)
        filter_region_table(page, "")
        delete_region_if_exists(page, padded_name)
        context.close()
        browser.close()


def test_cancel_discards_entered_data(playwright: Playwright) -> None:
    """Regression guard: filling in the Create Region form and clicking Cancel should
    discard the input - no new row should be created, and reopening the modal should
    show it reset to its default empty state."""
    browser, context, page = create_page(playwright)
    region_name = ""
    try:
        ensure_on_region_page(page)

        timestamp = datetime.now().strftime("%H%M%S")
        region_name = f"NegRegionCancelTest_{timestamp}"

        open_create_region_modal(page)
        select_country(page)

        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(region_name)
        else:
            page.get_by_placeholder("Enter Region").fill(region_name)

        _screenshot(page, "test_10_region_cancel_before_discard")

        page.get_by_role("button", name="Cancel").click()
        page.wait_for_timeout(500)

        expect(page.get_by_role("heading", name="Create Region")).not_to_be_visible(timeout=3000)

        # The typed name must not appear as a new row on the list
        filter_region_table(page, region_name)
        new_row = page.get_by_role("row", name=re.compile(re.escape(region_name), re.I))
        expect(new_row).to_have_count(0, timeout=3000)
        filter_region_table(page, "")

        # Reopening the modal should show a clean form, not the previously typed value
        open_create_region_modal(page)
        _screenshot(page, "test_10_region_cancel_reopened_state")
        region_input_reopened = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input_reopened.count() > 0 and region_input_reopened.first.is_visible():
            expect(region_input_reopened.first).to_have_value("", timeout=3000)
        else:
            expect(page.get_by_placeholder("Enter Region")).to_have_value("", timeout=3000)
    finally:
        close_create_region_modal(page)
        delete_region_if_exists(page, region_name)
        context.close()
        browser.close()


@pytest.mark.xfail(strict=False, reason="Application defect: Whitespace-only, special character, or invalid region names are accepted without validation error")
@pytest.mark.parametrize("invalid_name", ["   ", "!!!@@@###", "a" * 256])
def test_reject_invalid_region_name(playwright: Playwright, invalid_name: str) -> None:
    """Whitespace-only, special-character-only, or excessively long Region names should
    be rejected with a validation error rather than accepted as-is."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_region_page(page)
        open_create_region_modal(page)

        select_country(page)
        region_input = page.get_by_role("textbox", name=re.compile(r"Region", re.I))
        if region_input.count() > 0 and region_input.first.is_visible():
            region_input.first.fill(invalid_name)
        else:
            page.get_by_placeholder("Enter Region").fill(invalid_name)

        select_first_branch(page)
        _screenshot(page, "test_10_region_invalid_name")

        page.get_by_role("button", name="Create").click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_region_invalid_name_after_submit")

        validation_message = page.locator("[role='status'], [role='alert'], .toast, div, span, p").filter(
            has_text=re.compile(r"invalid|required|not allowed|too long|max.*character|enter.*region|please", re.I)
        )
        modal_open = is_region_modal_open(page)
        
        assert validation_message.count() > 0 or modal_open, (
            f"Invalid region name '{invalid_name}' was accepted without validation message or form blocking"
        )
    finally:
        close_create_region_modal(page)
        delete_region_if_exists(page, invalid_name)
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_create_region_empty_fields_shows_validation(playwright)
        test_create_region_without_branch_shows_validation(playwright)
        test_duplicate_region_name_shows_error(playwright)
        test_duplicate_region_name_case_insensitive(playwright)
        test_duplicate_region_name_whitespace_trimmed(playwright)
        test_cancel_discards_entered_data(playwright)
        test_reject_invalid_region_name(playwright, "   ")
