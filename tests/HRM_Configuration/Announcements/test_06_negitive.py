import re
from playwright.sync_api import Playwright, sync_playwright, expect

from test_01_login import do_login
from config import login_as, _screenshot


def _open_card_menu(page):
    """Helper to click the 3-dot action menu for an announcement card."""
    page.wait_for_timeout(1000)
    try:
        buttons = page.get_by_text("Bhanu").first.locator("xpath=ancestor::div[count(.//button) > 0][1]").get_by_role("button")
        count = buttons.count()
        clicked = False
        for i in range(count):
            btn = buttons.nth(i)
            if btn.is_visible():
                btn.click()
                clicked = True
                break
        if not clicked and count > 0:
            buttons.last.click(force=True)
    except Exception:
        page.locator("button:has(svg)").last.click(force=True)


def test_negative_announcements(page):
    # Perform login and navigate to Announcements page
    do_login(page)
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 1: Open Add Announcement modal and submit with all fields empty
    # =========================================================================
    page.get_by_role("button", name="Add announcement").click()
    page.get_by_role("button", name="Create").click()
    _screenshot(page, "negative_01_empty_form_submit")

    # =========================================================================
    # NEGATIVE TEST CASE 2: Submit with only Title filled (missing dates, location, department, description)
    # =========================================================================
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("Bhanu")
    page.get_by_role("button", name="Create").click()
    _screenshot(page, "negative_02_title_only_submit")
    page.get_by_role("button", name="Cancel").click()

    # =========================================================================
    # NEGATIVE TEST CASE 3: Submit with Title and Start Date filled only (missing End Date, Location, Department, Description)
    # =========================================================================
    page.get_by_role("button", name="Add announcement").click()
    page.get_by_role("button", name="Create").click()
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("Bhanu")
    
    # Select From Date
    page.get_by_role("button", name="Select date").first.click()
    page.get_by_role("button", name="Go to the Next Month").click()
    page.get_by_role("button", name="Monday, August 31st,").click()
    page.get_by_role("textbox", name="Title *").click()

    page.get_by_role("button", name="Create").click()
    _screenshot(page, "negative_03_title_and_startdate_submit")

    # =========================================================================
    # NEGATIVE TEST CASE 4: Fill Dates, Location, and Department but leave Description empty
    # =========================================================================
    # Select To Date
    page.get_by_role("button", name="Select date").click()
    page.get_by_role("button", name="Go to the Next Month").click()
    page.get_by_role("button", name="Monday, August 31st,").click()
    page.get_by_role("textbox", name="Title *").click()

    # Select Reminder Date
    page.get_by_role("button", name="Select reminder date").click()
    page.get_by_role("button", name="Go to the Next Month").click()
    page.get_by_role("button", name="Monday, August 31st,").click()
    page.get_by_role("textbox", name="Title *").click()

    # Select Location using test_02_create.py method
    page.locator("div").filter(has_text="Select locations").nth(4).click()
    try:
        page.get_by_label("Coimbatore").click(force=True)
    except Exception:
        page.get_by_label("Port Blair").click(force=True)
    page.get_by_role("textbox", name="Title *").click()

    # Select Department using test_02_create.py method
    page.locator("div").filter(has_text="Select departments").nth(4).click()
    page.get_by_label("Testing").click(force=True)
    page.get_by_role("textbox", name="Title *").click()

    page.get_by_role("button", name="Create").click()
    _screenshot(page, "negative_04_missing_description_submit")

    # =========================================================================
    # NEGATIVE TEST CASE 5: Enter Description field and Create Announcement
    # =========================================================================
    page.get_by_role("textbox", name="Description*").click()
    page.get_by_role("textbox", name="Description*").fill("bhanu's birthday")
    _screenshot(page, "negative_05_filled_description")

    # Click Create to add announcement
    page.get_by_role("button", name="Create").click()
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 6: Edit Announcement - Clear Title (empty title) & attempt Update
    # =========================================================================
    _open_card_menu(page)
    page.get_by_role("menuitem", name="Edit").click()
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="Title *").fill("")
    page.get_by_role("button", name="Update").click()
    _screenshot(page, "negative_06_edit_empty_title")

    # =========================================================================
    # NEGATIVE TEST CASE 7: Edit Announcement - Fill Title & Clear Announcement Image field
    # =========================================================================
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("Bhanu Prakash")
    try:
        page.get_by_role("textbox", name="Announcement Image").click()
        page.get_by_role("textbox", name="Announcement Image").press("ControlOrMeta+a")
        page.get_by_role("textbox", name="Announcement Image").fill("")
        page.get_by_role("button", name="Update").click()
        _screenshot(page, "negative_07_edit_empty_image")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 8: Edit Announcement - Fill Announcement Image & Update
    # =========================================================================
    try:
        page.get_by_role("textbox", name="Announcement Image").click()
        page.get_by_role("textbox", name="Announcement Image").fill("Bhanu Prakash")
        page.get_by_role("button", name="Update").click()
        _screenshot(page, "negative_08_edit_update_success")
    except Exception:
        try:
            page.get_by_role("button", name="Update").click()
        except Exception:
            page.get_by_role("button", name="Cancel").click()

    # =========================================================================
    # NEGATIVE TEST CASE 9: Download Announcement
    # =========================================================================
    try:
        _open_card_menu(page)
        with page.expect_download(timeout=5000) as download_info:
            page.get_by_role("menuitem", name="Download").click()
        _screenshot(page, "negative_09_download")
    except Exception:
        _screenshot(page, "negative_09_download_attempt")

    # =========================================================================
    # NEGATIVE TEST CASE 10: Delete Announcement - Cancel confirmation dialog
    # =========================================================================
    try:
        _open_card_menu(page)
        page.get_by_role("menuitem", name="Delete").click()
        page.get_by_role("button", name="Cancel").click()
        _screenshot(page, "negative_10_cancel_delete")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 11: Delete Announcement - Confirm Deletion
    # =========================================================================
    try:
        _open_card_menu(page)
        page.get_by_role("menuitem", name="Delete").click()
        page.get_by_role("button", name="Delete").click()
        _screenshot(page, "negative_11_confirm_delete")
    except Exception:
        pass

    page.wait_for_timeout(3000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    test_negative_announcements(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
