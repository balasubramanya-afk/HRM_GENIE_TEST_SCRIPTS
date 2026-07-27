import re
from playwright.sync_api import Playwright, sync_playwright, expect

from test_01_login import do_login
from config import login_as, _screenshot


def test_negative_employment_types(page):
    # Perform login and navigate to Employment Type page
    do_login(page)
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 1: Open Add Employment modal and Cancel without adding
    # =========================================================================
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "negative_01_cancel_add")

    # =========================================================================
    # NEGATIVE TEST CASE 2: Submit Add Employment form with empty/blank title
    # =========================================================================
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Add Employment").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "negative_02_empty_add_submit")

    # =========================================================================
    # NEGATIVE TEST CASE 3: Attempt adding duplicate Employment Type ("Full Time") and cancel
    # =========================================================================
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("textbox", name="e.g., Full Time").fill("Full Time")
    page.get_by_role("button", name="Add Employment").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "negative_03_duplicate_cancel")

    # =========================================================================
    # NEGATIVE TEST CASE 4: Add existing/duplicate title ("Full Time Employee")
    # =========================================================================
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("textbox", name="e.g., Full Time").fill("Full Time Employee")
    page.get_by_role("button", name="Add Employment").click()
    _screenshot(page, "negative_04_duplicate_submit")

    # =========================================================================
    # NEGATIVE TEST CASE 5: Edit Employment Type with blank title & click Update then Cancel
    # =========================================================================
    # Use dynamic table row selector instead of fragile hardcoded Radix IDs
    page.get_by_role("row").nth(1).get_by_role("button").click()
    page.get_by_role("menuitem", name="Edit").click()
    page.get_by_role("textbox", name="e.g., Full Time").click()
    page.get_by_role("textbox", name="e.g., Full Time").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="e.g., Full Time").fill("")
    page.get_by_role("button", name="Update Employment").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "negative_05_edit_empty_title")

    # =========================================================================
    # NEGATIVE TEST CASE 6: Delete Employment Type - Cancel confirmation dialog
    # =========================================================================
    page.get_by_role("row").nth(1).get_by_role("button").click()
    page.get_by_role("menuitem", name="Delete").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "negative_06_cancel_delete")

    # =========================================================================
    # NEGATIVE TEST CASE 7: Delete Employment Type - Confirm Deletion
    # =========================================================================
    page.get_by_role("row").nth(1).get_by_role("button").click()
    page.get_by_role("menuitem", name="Delete").click()
    page.get_by_role("button", name="Delete").click()
    _screenshot(page, "negative_07_confirm_delete")

    page.wait_for_timeout(3000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    test_negative_employment_types(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
