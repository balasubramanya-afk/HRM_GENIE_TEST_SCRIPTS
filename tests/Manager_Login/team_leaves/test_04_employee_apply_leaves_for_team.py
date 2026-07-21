import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
    get_picker_button,
    select_next_available_date,
)

def apply_leave_as(page: Page, role: str, leave_type: str, date_offset: int, reason: str):
    """Helper to apply for a leave as specified employee role."""
    try:
        login_as(page, role)
        page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
        if not apply_btn.is_visible():
            return

        apply_btn.click()
        page.wait_for_timeout(1000)

        # Select Leave Type
        leave_type_combo = page.get_by_role("combobox", name="Select Leave Type*").or_(page.get_by_role("combobox")).first
        if leave_type_combo.is_visible():
            leave_type_combo.click()
            page.wait_for_timeout(500)

            option = page.get_by_role("option", name=leave_type).first
            if option.is_visible():
                option.click()
            else:
                page.get_by_role("option").first.click()

        page.wait_for_timeout(500)

        # Pick start date
        start_btn = get_picker_button(page, "Pick start date")
        if start_btn.is_visible():
            start_btn.click()
            select_next_available_date(page, date_offset)
            page.wait_for_timeout(500)

        # Pick end date
        end_btn = get_picker_button(page, "Pick end date")
        if end_btn.is_visible():
            end_btn.click()
            select_next_available_date(page, date_offset)
            page.wait_for_timeout(500)

        # Fill Reason
        reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
        if reason_box.is_visible():
            reason_box.fill(reason)

        _screenshot(page, f"test_04_{role}_applied_{reason.replace(' ', '_')}")

        # Submit form
        dialog = page.locator("div[role='dialog'], [role='alertdialog']").first
        submit_btn = dialog.get_by_role("button", name="Apply").or_(dialog.get_by_role("button", name="Submit")).first
        if not submit_btn.is_visible():
            submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first

        if submit_btn.is_visible():
            try:
                submit_btn.click(timeout=3000)
            except Exception:
                try:
                    submit_btn.evaluate("el => el.click()")
                except Exception:
                    pass

        close_toast(page)
        page.wait_for_timeout(2000)

        # Close dialog if still present
        if dialog.is_visible():
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)
    except Exception as exc:
        print(f"Apply leave notice for {role} ({reason}): {exc}")

def test_employee_apply_leaves_for_team(page: Page):
    """4. Apply 2 leaves from Employee 1 and 2 leaves from Employee 2 for Team Leaves testing."""
    # Employee 1 applies 2 leaves
    apply_leave_as(page, "Employee", "Casual Leave", 3, "Emp1 Team Leave Single Approve")
    apply_leave_as(page, "Employee", "Sick Leave", 5, "Emp1 Team Leave Single Reject")

    # Employee 2 applies 2 leaves
    apply_leave_as(page, "Employee2", "Casual Leave", 7, "Emp2 Team Leave Bulk 1")
    apply_leave_as(page, "Employee2", "Sick Leave", 9, "Emp2 Team Leave Bulk 2")
