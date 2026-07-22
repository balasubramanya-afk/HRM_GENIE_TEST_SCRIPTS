import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_next_available_date, select_time_option,
    get_picker_button, close_toast,
)

# Use a fixed offset (days ahead) for BOTH WFH and OnDuty date picks.
# Using the same offset guarantees both calendars target the same date.
# offset=3 = 3 days from today — avoids weekends in most cases.
# Change this value if that day is a public holiday or already has a request.
_DATE_OFFSET = 3

def test_conflict_wfh_and_onduty_same_date(page: Page):
    """10. Apply WFH and On Duty on the same date and verify
    'WFH request already exists' error message when applying On Duty."""
    login_as(page, "Manager")

    # ── Step 1: Navigate to WFH and apply WFH ────────────────────────────────
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    wfh_apply_btn = (
        page.get_by_role("button", name="Apply WFH")
        .or_(page.get_by_role("button", name="Request WFH"))
        .or_(page.get_by_role("button", name="Apply For WFH"))
        .first
    )
    expect(wfh_apply_btn).to_be_visible()
    wfh_apply_btn.click()
    page.wait_for_timeout(1000)

    # Pick WFH start date using _DATE_OFFSET
    wfh_start_btn = get_picker_button(page, "Pick start date")
    expect(wfh_start_btn).to_be_visible()
    wfh_start_btn.click()
    assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
        f"Failed to select WFH start date (offset={_DATE_OFFSET})"
    page.wait_for_timeout(500)

    # Pick WFH end date — same _DATE_OFFSET so it's the same day
    wfh_end_btn = get_picker_button(page, "Pick end date")
    expect(wfh_end_btn).to_be_visible()
    wfh_end_btn.click()
    assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
        f"Failed to select WFH end date (offset={_DATE_OFFSET})"
    page.wait_for_timeout(500)

    # Fill reason — must be at least 10 words or the app will reject it
    wfh_reason = (
        page.get_by_placeholder("Enter your reason for work from home")
        .or_(page.locator("textarea"))
        .or_(page.get_by_role("textbox", name="Reason *"))
        .first
    )
    expect(wfh_reason).to_be_visible()
    wfh_reason.fill(
        "Applying WFH for the same date to verify the conflict validation test case."
    )

    wfh_submit = page.get_by_role("button", name="Apply").first
    expect(wfh_submit).to_be_visible()
    wfh_submit.click()
    page.wait_for_timeout(4000)  # wait for API call + modal close animation

    # ── Assert WFH was actually submitted before continuing ───────────────────
    # Wait for the modal to fully close — successful submit dismisses it.
    # If it stays open (validation error, short reason, duplicate date, etc.)
    # this will time out and fail the test with a clear message.
    wfh_modal = page.locator("[role='dialog']").first
    expect(wfh_modal).not_to_be_visible(timeout=8000), (
        "WFH modal is still open after clicking Apply — "
        "the WFH form was NOT submitted successfully. "
        "Check reason length, date availability, or existing requests on that date."
    )
    close_toast(page)

    # ── Step 2: Navigate to On Duty and apply On Duty on THE SAME DATE ────────
    # We use the identical _DATE_OFFSET so both calendars target the same date.
    navigate_to_my_onduty(page)

    onduty_apply_btn = (
        page.get_by_role("button", name="Apply On Duty")
        .or_(page.get_by_role("button", name="Request On Duty"))
        .first
    )
    expect(onduty_apply_btn).to_be_visible()
    onduty_apply_btn.click()
    page.wait_for_timeout(1000)

    # Pick OnDuty start date — same _DATE_OFFSET as WFH
    onduty_start_btn = (
        page.get_by_role("button", name="Pick start date")
        .or_(page.locator("button:has-text('Pick start date')"))
        .first
    )
    expect(onduty_start_btn).to_be_visible()
    onduty_start_btn.click()
    page.wait_for_timeout(500)
    assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
        f"Failed to select OnDuty start date (offset={_DATE_OFFSET})"
    page.wait_for_timeout(500)

    # Pick OnDuty end date — same _DATE_OFFSET
    onduty_end_btn = (
        page.get_by_role("button", name="Pick end date")
        .or_(page.locator("button:has-text('Pick end date')"))
        .first
    )
    if onduty_end_btn.is_visible():
        onduty_end_btn.click()
        page.wait_for_timeout(500)
        assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
            f"Failed to select OnDuty end date (offset={_DATE_OFFSET})"
        page.wait_for_timeout(500)

    select_time_option(page, "Start Time *", "9:15 AM")
    select_time_option(page, "End Time *", "10:15 AM")

    onduty_reason = (
        page.get_by_role("textbox", name="Reason *")
        .or_(page.locator("textarea"))
        .first
    )
    expect(onduty_reason).to_be_visible()
    onduty_reason.fill(
        "Applying On Duty on the same date as WFH to test conflict validation message."
    )

    onduty_submit = page.get_by_role("button", name="Apply").first
    expect(onduty_submit).to_be_visible()
    onduty_submit.click()
    page.wait_for_timeout(3000)

    # ── Step 3: Verify conflict error — STRICT check, no dialog fallback ──────
    # The app must show an error mentioning WFH conflict.
    # We do NOT use .or_(dialog) because the dialog stays open even on a
    # successful submit, which would cause a false pass.
    conflict_error = page.get_by_text(
        re.compile(
            r"WFH request already exists for the selected dates",
            re.IGNORECASE,
        )
    )
    assert conflict_error.count() > 0, (
        "FAIL: Expected a conflict error message "
        "(e.g. 'WFH request already exists') but none was found. "
        "The On Duty may have been submitted successfully — no conflict was raised."
    )
    expect(conflict_error.first).to_be_visible(timeout=5000)

    _screenshot(page, "test_10_conflict_wfh_and_onduty_same_date")

    # ── Step 4: Cleanup ────────────────────────────────────────────────────────
    # Close the OnDuty modal if still open
    close_modal_btn = (
        page.get_by_role("button", name="Close")
        .or_(page.locator("[role='dialog'] button:has(svg.lucide-x)"))
        .first
    )
    if close_modal_btn.is_visible():
        close_modal_btn.click()
        page.wait_for_timeout(500)

    # Go back to WFH and delete the WFH request we created
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_timeout(1000)

    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    wfh_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"conflict validation test", re.IGNORECASE)
    ).first
    if wfh_row.is_visible():
        del_btn = wfh_row.locator(
            "button.text-red-500:not([disabled]), button:has(svg.lucide-trash-2):not([disabled])"
        ).first
        if del_btn.is_visible():
            del_btn.click()
            page.wait_for_timeout(500)
            confirm_btn = (
                page.get_by_role("button", name="Delete")
                .or_(page.get_by_role("button", name=re.compile(r"Confirm|Yes", re.I)))
                .last
            )
            if confirm_btn.is_visible():
                confirm_btn.click()
                page.wait_for_timeout(1500)
