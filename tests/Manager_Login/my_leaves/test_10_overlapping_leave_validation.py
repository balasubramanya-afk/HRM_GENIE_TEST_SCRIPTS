import re
from datetime import date, timedelta
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
    get_picker_button,
    select_next_available_date,
)

def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

def test_overlapping_leave_validation(page: Page):
    """10. Apply Leave first, then verify that the existing Leave date is blocked (disabled)
    on the calendar picker when attempting to apply again."""
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    _DATE_OFFSET = 2

    # ── Step 1: Apply initial leave request ───────────────────────────────────
    apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
    expect(apply_btn).to_be_visible()
    apply_btn.click()
    page.wait_for_timeout(1000)

    # Select Leave Type
    leave_type_combo = page.get_by_role("combobox", name="Select Leave Type*").or_(page.get_by_role("combobox")).first
    leave_type_combo.click()
    page.wait_for_timeout(500)

    casual_opt = page.get_by_role("option", name="Casual Leave")
    if casual_opt.is_visible():
        casual_opt.first.click()
    else:
        page.get_by_role("option").first.click()

    page.wait_for_timeout(500)

    # Pick start date
    start_btn = get_picker_button(page, "Pick start date")
    if start_btn.is_visible():
        start_btn.click()
        select_next_available_date(page, _DATE_OFFSET)
        page.wait_for_timeout(500)

    # Pick end date
    end_btn = get_picker_button(page, "Pick end date")
    if end_btn.is_visible():
        end_btn.click()
        select_next_available_date(page, _DATE_OFFSET)
        page.wait_for_timeout(500)

    unique_reason = "Initial Leave Request to verify date gets blocked on second attempt"

    reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
    expect(reason_box).to_be_visible()
    reason_box.fill(unique_reason)

    submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first
    try:
        submit_btn.click(timeout=3000)
    except Exception:
        submit_btn.evaluate("el => el.click()")
    page.wait_for_timeout(4000)

    # Assert leave modal closed
    leave_modal = page.locator("[role='dialog']").first
    expect(leave_modal).not_to_be_visible(timeout=8000), (
        "First Leave modal is still open after clicking Apply."
    )
    close_toast(page)

    # ── Step 2: Open Leave form again & verify the date is BLOCKED ────────────
    apply_btn.click()
    page.wait_for_timeout(1000)

    leave_type_combo = page.get_by_role("combobox", name="Select Leave Type*").or_(page.get_by_role("combobox")).first
    leave_type_combo.click()
    page.wait_for_timeout(500)

    casual_opt = page.get_by_role("option", name="Casual Leave")
    if casual_opt.is_visible():
        casual_opt.first.click()
    else:
        page.get_by_role("option").first.click()

    page.wait_for_timeout(500)

    # Open start date picker
    start_btn = get_picker_button(page, "Pick start date")
    expect(start_btn).to_be_visible()
    start_btn.click()
    page.wait_for_timeout(500)

    # Find day element for target date
    target_date = date.today() + timedelta(days=_DATE_OFFSET)
    month_name = target_date.strftime('%B')
    day = target_date.day
    suf = ordinal(day)
    pattern = re.compile(fr"{month_name}\s+{day}{suf}", re.IGNORECASE)

    day_button = page.get_by_role("button", name=pattern).first
    expect(day_button).to_be_visible()

    td_container = page.locator(f"td[data-day='{target_date.strftime('%Y-%m-%d')}']").first

    is_disabled = (
        not day_button.is_enabled()
        or day_button.get_attribute("disabled") is not None
        or day_button.get_attribute("data-disabled") == "true"
        or (td_container.is_visible() and td_container.get_attribute("data-disabled") == "true")
    )

    assert is_disabled, (
        f"FAIL: Applied leave date ({target_date}) is NOT blocked/disabled on calendar picker when applying again."
    )

    _screenshot(page, "test_10_overlapping_leave_date_blocked")

    # ── Step 3: Cleanup ────────────────────────────────────────────────────────
    if leave_modal.is_visible():
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

    # Delete the initial leave request
    leave_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"Initial Leave Request to verify date gets blocked", re.IGNORECASE)
    ).first
    if leave_row.is_visible():
        del_btn = leave_row.locator(
            "button.text-red-500:not([disabled]), button:has(svg.lucide-trash-2):not([disabled])"
        ).or_(leave_row.locator("button").filter(has=page.locator("svg.lucide-trash-2"))).first
        if del_btn.is_visible():
            try:
                del_btn.click(timeout=3000)
            except Exception:
                del_btn.evaluate("el => el.click()")
            page.wait_for_timeout(500)
            confirm_btn = (
                page.get_by_role("button", name="Delete")
                .or_(page.get_by_role("button", name=re.compile(r"Confirm|Yes", re.I)))
                .last
            )
            if confirm_btn.is_visible():
                confirm_btn.click()
                page.wait_for_timeout(1500)
