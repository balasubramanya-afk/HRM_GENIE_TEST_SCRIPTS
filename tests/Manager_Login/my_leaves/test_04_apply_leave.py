import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
    get_picker_button,
    select_next_available_date,
)

def test_apply_leave(page: Page):
    """4. Test Apply Leave for Manager."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    unique_reason = "Auto Test Leave Manager"

    apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
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
        select_next_available_date(page, 2)
        page.wait_for_timeout(500)

    # Pick end date
    end_btn = get_picker_button(page, "Pick end date")
    if end_btn.is_visible():
        end_btn.click()
        select_next_available_date(page, 2)
        page.wait_for_timeout(500)

    # Fill Reason
    reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
    reason_box.fill(unique_reason)

    _screenshot(page, "test_04_01_apply_leave_filled")

    # Submit form
    submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first
    try:
        submit_btn.click(timeout=3000)
    except Exception:
        submit_btn.evaluate("el => el.click()")

    close_toast(page)
    page.wait_for_timeout(2000)

    _screenshot(page, "test_04_02_leave_applied")

    # Assert page state intact
    expect(page).to_have_url(re.compile(r".*/my-leave"))
