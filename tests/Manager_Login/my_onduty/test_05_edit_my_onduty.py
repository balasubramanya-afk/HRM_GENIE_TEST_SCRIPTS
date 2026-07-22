import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_next_available_date, select_dropdown_option, select_time_option,
)

def test_edit_my_onduty(page: Page):
    """5. Edit an existing pending On Duty request."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    edit_btn = page.locator("tbody tr button.text-emerald-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-pencil):not([disabled])")).first
    if not edit_btn.is_visible():
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

        select_time_option(page, "Start Time *", "9:15 AM")
        select_time_option(page, "End Time *", "10:15 AM")

        reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
        expect(reason_input).to_be_visible()
        reason_input.fill("test test test test test test test test test test")

        submit_btn = page.get_by_role("button", name="Apply").first
        expect(submit_btn).to_be_visible()
        submit_btn.click()
        page.wait_for_timeout(2000)

    # Click Edit button for pending request
    edit_btn = page.locator("tbody tr button.text-emerald-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-pencil):not([disabled])")).first
    expect(edit_btn).to_be_visible()
    edit_btn.click()
    page.wait_for_timeout(1000)

    # Verify Edit modal is visible
    modal_dialog = page.locator("[role='dialog']").first
    expect(modal_dialog).to_be_visible()

    # Update reason
    reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("test test test test test test test test test test updated")

    # Update Start Time & End Time
    select_time_option(page, "Start Time *", "10:00 AM")
    select_time_option(page, "End Time *", "11:30 AM")

    # Click Apply
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Verify success toast notification
    toast = page.get_by_text(re.compile(r"updated|success", re.IGNORECASE)).first
    expect(toast).to_be_visible()

    _screenshot(page, "test_05_edit_my_onduty")
