import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_next_available_date, select_dropdown_option, select_time_option,
)

def test_apply_my_onduty(page: Page):
    """4. Apply for On Duty with date, time range, and reason."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # Open Apply modal
    apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
    expect(apply_btn).to_be_visible()
    apply_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal dialog is visible
    expect(page.locator("[role='dialog']").first).to_be_visible()

    # Pick Start Date
    start_date_btn = page.get_by_role("button", name="Pick start date").or_(page.locator("button:has-text('Pick start date')")).first
    expect(start_date_btn).to_be_visible()
    start_date_btn.click()
    assert select_next_available_date(page, start_offset=1), "Failed to select start date"

    # Pick End Date
    end_date_btn = page.get_by_role("button", name="Pick end date").or_(page.locator("button:has-text('Pick end date')")).first
    expect(end_date_btn).to_be_visible()
    end_date_btn.click()
    assert select_next_available_date(page, start_offset=1), "Failed to select end date"

    # Select Start & End Time
    select_time_option(page, "Start Time *", "9:15 AM")
    select_time_option(page, "End Time *", "10:15 AM")

    # Fill Reason
    reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("test test test test test test test test test test")

    # Click Apply
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Verify success toast — must show a success keyword, not just any table row
    success_toast = page.get_by_text(re.compile(r"success|applied|created|submitted", re.IGNORECASE))
    expect(success_toast.first).to_be_visible(timeout=5000)

    _screenshot(page, "test_04_apply_my_onduty")
