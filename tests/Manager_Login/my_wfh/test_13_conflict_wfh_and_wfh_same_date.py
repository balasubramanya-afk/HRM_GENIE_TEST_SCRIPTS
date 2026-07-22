import re
from datetime import date, timedelta
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, select_next_available_date, get_picker_button, close_toast
)

# Use a fixed offset (days ahead) for BOTH WFH date checks.
_DATE_OFFSET = 7

def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

def test_conflict_wfh_and_wfh_same_date(page: Page):
    """13. Apply WFH first, then verify that the existing WFH date is blocked (disabled)
    on the WFH calendar picker when attempting to apply again."""
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

    login_as(page, "Manager")

    # ── Step 1: Navigate to WFH and apply first WFH ──────────────────────────
    page.goto("https://qa.hrmgenie.outstrive.co/work-from-home")
    page.wait_for_load_state("networkidle")
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

    # Pick WFH1 start date
    wfh_start_btn = get_picker_button(page, "Pick start date")
    expect(wfh_start_btn).to_be_visible()
    wfh_start_btn.click()
    assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
        f"Failed to select WFH1 start date (offset={_DATE_OFFSET})"
    page.wait_for_timeout(500)

    # Pick WFH1 end date
    wfh_end_btn = get_picker_button(page, "Pick end date")
    expect(wfh_end_btn).to_be_visible()
    wfh_end_btn.click()
    assert select_next_available_date(page, start_offset=_DATE_OFFSET), \
        f"Failed to select WFH1 end date (offset={_DATE_OFFSET})"
    page.wait_for_timeout(500)

    unique_reason = "Applying initial WFH to verify that date gets blocked on WFH date picker for second attempt."

    wfh_reason = (
        page.get_by_placeholder("Enter your reason for work from home")
        .or_(page.locator("textarea"))
        .or_(page.get_by_role("textbox", name="Reason *"))
        .first
    )
    expect(wfh_reason).to_be_visible()
    wfh_reason.fill(unique_reason)

    wfh_submit = page.get_by_role("button", name="Apply").first
    expect(wfh_submit).to_be_visible()
    wfh_submit.click()
    page.wait_for_timeout(4000)

    # Assert WFH modal is closed
    wfh_modal = page.locator("[role='dialog']").first
    expect(wfh_modal).not_to_be_visible(timeout=8000), (
        "First WFH modal is still open after clicking Apply."
    )
    close_toast(page)

    # ── Step 2: Open WFH form again and verify the WFH date is BLOCKED ───────
    wfh_apply_btn.click()
    page.wait_for_timeout(1000)

    # Open WFH2 start date picker
    wfh_start_btn = get_picker_button(page, "Pick start date")
    expect(wfh_start_btn).to_be_visible()
    wfh_start_btn.click()
    page.wait_for_timeout(500)

    # Find the day element for target date
    target_date = date.today() + timedelta(days=_DATE_OFFSET)
    month_name = target_date.strftime('%B')
    day = target_date.day
    suf = ordinal(day)
    pattern = re.compile(fr"{month_name}\s+{day}{suf}", re.IGNORECASE)

    day_button = page.get_by_role("button", name=pattern).first
    expect(day_button).to_be_visible()

    # Check if the date is blocked (disabled or data-disabled="true")
    td_container = page.locator(f"td[data-day='{target_date.strftime('%Y-%m-%d')}']").first
    
    is_disabled = (
        not day_button.is_enabled()
        or day_button.get_attribute("disabled") is not None
        or day_button.get_attribute("data-disabled") == "true"
        or (td_container.is_visible() and td_container.get_attribute("data-disabled") == "true")
    )

    assert is_disabled, (
        f"FAIL: Initial WFH date ({target_date}) is NOT blocked/disabled on WFH date picker."
    )

    _screenshot(page, "test_13_conflict_wfh_and_wfh_blocked_date")

    # ── Step 3: Cleanup ────────────────────────────────────────────────────────
    # Close WFH modal
    close_modal_btn = (
        page.get_by_role("button", name="Close")
        .or_(page.locator("[role='dialog'] button:has(svg.lucide-x)"))
        .first
    )
    if close_modal_btn.is_visible():
        close_modal_btn.click()
        page.wait_for_timeout(500)

    # Delete the initial WFH request we created
    wfh_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"Applying initial WFH to verify that date gets blocked", re.IGNORECASE)
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
