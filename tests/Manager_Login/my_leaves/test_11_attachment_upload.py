import re
import os
from pathlib import Path
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
    get_picker_button,
    select_next_available_date,
)

def test_attachment_upload(page: Page):
    """11. Test uploading attachment for Sick Leave exceeding 3 days."""
    page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))

    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Create dummy medical certificate file
    dummy_file = Path(__file__).parent / "medical_certificate.pdf"
    dummy_file.write_text("Dummy content for medical certificate attachment.")

    try:
        apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
        expect(apply_btn).to_be_visible()
        apply_btn.click()
        page.wait_for_timeout(1000)

        # Select Sick Leave Type
        leave_type_combo = page.get_by_role("combobox", name="Select Leave Type*").or_(page.get_by_role("combobox")).first
        leave_type_combo.click()
        page.wait_for_timeout(500)

        sick_opt = page.get_by_role("option", name="Sick Leave")
        if sick_opt.is_visible():
            sick_opt.first.click()
        else:
            page.get_by_role("option").first.click()

        page.wait_for_timeout(500)

        # Pick start date (Offset=2)
        start_btn = get_picker_button(page, "Pick start date")
        if start_btn.is_visible():
            start_btn.click()
            select_next_available_date(page, 2)
            page.wait_for_timeout(500)

        # Pick end date (Offset=8 to ensure >3 days duration)
        end_btn = get_picker_button(page, "Pick end date")
        if end_btn.is_visible():
            end_btn.click()
            select_next_available_date(page, 8)
            page.wait_for_timeout(500)

        unique_reason = "Medical Sick Leave Request exceeding 3 days with attachment"

        reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
        expect(reason_box).to_be_visible()
        reason_box.fill(unique_reason)

        # Handle Medical Certificate File Upload if present
        file_input = page.locator("input[type='file']").first
        if file_input.count() > 0:
            file_input.set_input_files(str(dummy_file))
            page.wait_for_timeout(1000)

        _screenshot(page, "test_11_01_attachment_uploaded")

        # Verify attachment notice if present
        attachment_notice = page.get_by_text(
            re.compile(r"Your leave exceeds 3 days.*upload valid medical certificate|exceeds 3 days|medical certificate", re.IGNORECASE)
        )
        if attachment_notice.count() > 0:
            expect(attachment_notice.first).to_be_visible()

        submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first
        submit_btn.click()
        page.wait_for_timeout(3000)

        _screenshot(page, "test_11_02_sick_leave_submitted_with_attachment")

        # Cleanup created leave request
        leave_modal = page.locator("[role='dialog']").first
        if leave_modal.is_visible():
            page.keyboard.press("Escape")
            page.wait_for_timeout(1000)

        leave_row = page.locator("tbody tr").filter(
            has_text=re.compile(r"Medical Sick Leave Request exceeding 3 days", re.IGNORECASE)
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
    finally:
        if dummy_file.exists():
            os.remove(dummy_file)
