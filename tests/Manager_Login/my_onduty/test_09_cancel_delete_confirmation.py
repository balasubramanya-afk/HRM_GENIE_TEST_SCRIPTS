import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_next_available_date, select_time_option,
)

def test_cancel_delete_confirmation(page: Page):
    """9. Negative: Click delete on On Duty request but cancel confirmation dialog."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # Find delete button, apply if needed
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    if not delete_btn.is_visible():
        apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
        if apply_btn.is_visible():
            apply_btn.click()
            page.wait_for_timeout(1000)

            start_date_btn = page.get_by_role("button", name="Pick start date").or_(page.locator("button:has-text('Pick start date')")).first
            if start_date_btn.is_visible():
                start_date_btn.click()
                select_next_available_date(page, start_offset=1)

            end_date_btn = page.get_by_role("button", name="Pick end date").or_(page.locator("button:has-text('Pick end date')")).first
            if end_date_btn.is_visible():
                end_date_btn.click()
                select_next_available_date(page, start_offset=1)

            try:
                select_time_option(page, "Start Time *", "9:15 AM")
                select_time_option(page, "End Time *", "10:15 AM")
            except Exception:
                pass

            reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
            if reason_input.is_visible():
                reason_input.fill("Applying for On Duty request for cancel delete test case.")

            submit_btn = page.get_by_role("button", name="Apply").first
            if submit_btn.is_visible():
                submit_btn.click()
                page.wait_for_timeout(2000)

    # Expect delete button to be visible
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation modal is visible
    confirm_modal = page.locator("[role='dialog']").first
    expect(confirm_modal).to_be_visible()

    # Click Cancel in confirmation modal
    cancel_btn = page.get_by_role("button", name="Cancel").or_(page.locator("button:has-text('Cancel')")).first
    expect(cancel_btn).to_be_visible()
    cancel_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation dialog is dismissed
    expect(confirm_modal).not_to_be_visible()

    _screenshot(page, "test_09_cancel_delete_confirmation")
