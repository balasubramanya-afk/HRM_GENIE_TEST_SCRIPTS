import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
    get_picker_button,
    select_next_available_date,
)

def test_half_day_leave(page: Page):
    """12. Test applying for half day leave request."""
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

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

    # Enable Half Day checkbox / toggle if present
    half_day_toggle = (
        page.get_by_label("Half Day")
        .or_(page.locator("label:has-text('Half Day') input"))
        .or_(page.locator("button[role='checkbox']:has-text('Half Day')"))
        .or_(page.get_by_text("Half Day"))
        .first
    )
    if half_day_toggle.is_visible():
        half_day_toggle.click()
        page.wait_for_timeout(500)

    # Pick start date
    start_btn = get_picker_button(page, "Pick start date")
    if start_btn.is_visible():
        start_btn.click()
        select_next_available_date(page, 2)
        page.wait_for_timeout(500)

    # Pick end date if enabled
    end_btn = get_picker_button(page, "Pick end date")
    if end_btn.is_visible() and end_btn.is_enabled():
        end_btn.click()
        select_next_available_date(page, 2)
        page.wait_for_timeout(500)

    # Select session / half day period (First Half / Second Half) if available
    session_select = page.get_by_role("combobox", name="Session").or_(page.locator("[placeholder*='Session' i], [placeholder*='Half' i]")).first
    if session_select.is_visible():
        session_select.click()
        page.wait_for_timeout(300)
        opt = page.get_by_role("option").first
        if opt.is_visible():
            opt.click()

    unique_reason = "Applying Half Day Leave Test Request"

    reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
    expect(reason_box).to_be_visible()
    reason_box.fill(unique_reason)

    _screenshot(page, "test_12_01_half_day_leave_filled")

    submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first
    submit_btn.click()
    page.wait_for_timeout(4000)

    # Assert leave modal closed
    leave_modal = page.locator("[role='dialog']").first
    expect(leave_modal).not_to_be_visible(timeout=8000), (
        "Leave modal is still open after submitting half day leave."
    )
    close_toast(page)

    _screenshot(page, "test_12_02_half_day_leave_submitted")

    # Verify created leave request row and total duration of 0.5 days
    leave_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"Applying Half Day Leave Test Request", re.IGNORECASE)
    ).first
    expect(leave_row).to_be_visible()

    # Assert total column shows 0.5
    total_cell = leave_row.locator("td").nth(2).or_(leave_row.get_by_text("0.5")).first
    expect(total_cell).to_contain_text("0.5")

    if leave_row.is_visible():
        del_btn = leave_row.locator(
            "button.text-red-500:not([disabled]), button:has(svg.lucide-trash-2):not([disabled])"
        ).or_(leave_row.locator("button").filter(has=page.locator("svg.lucide-trash-2"))).first
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
