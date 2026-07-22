import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_next_available_date, select_time_option,
)

def test_delete_my_onduty(page: Page):
    """6. Delete an On Duty request and verify confirmation toast."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    if not delete_btn.is_visible():
        apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
        expect(apply_btn).to_be_visible()
        apply_btn.click()
        page.wait_for_timeout(1000)

        start_date_btn = page.get_by_role("button", name="Pick start date").or_(page.locator("button:has-text('Pick start date')")).first
        expect(start_date_btn).to_be_visible()
        start_date_btn.click()
        assert select_next_available_date(page, start_offset=1), "Failed to select start date"

        end_date_btn = page.get_by_role("button", name="Pick end date").or_(page.locator("button:has-text('Pick end date')")).first
        expect(end_date_btn).to_be_visible()
        end_date_btn.click()
        assert select_next_available_date(page, start_offset=1), "Failed to select end date"

        try:
            select_time_option(page, "Start Time *", "9:15 AM")
            select_time_option(page, "End Time *", "10:15 AM")
        except Exception:
            pass

        reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
        expect(reason_input).to_be_visible()
        reason_input.fill("test test test test test test test test test test")

        submit_btn = page.get_by_role("button", name="Apply").first
        expect(submit_btn).to_be_visible()
        submit_btn.click()
        page.wait_for_timeout(2000)

    # Click delete button in table for pending request
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation dialog
    confirm_dialog = page.locator("[role='dialog']").or_(page.get_by_text(re.compile(r"Delete|cancelling|remove", re.IGNORECASE))).first
    expect(confirm_dialog).to_be_visible()

    # Click Delete in confirmation dialog
    confirm_delete_btn = page.get_by_role("button", name="Delete").last
    expect(confirm_delete_btn).to_be_visible()
    confirm_delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify toast or notification message
    toast = page.get_by_text(re.compile(r"deleted|removed|success", re.IGNORECASE)).first
    expect(toast).to_be_visible()

    _screenshot(page, "test_06_delete_my_onduty")

