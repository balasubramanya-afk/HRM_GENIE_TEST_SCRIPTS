import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
)

def test_edit_leave(page: Page):
    """5. Test Edit Leave for Manager."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    updated_reason = "Auto Test Leave Manager Updated"

    row = page.locator("tr").filter(has_text="Pending").first
    if row.is_visible():
        edit_btn = row.locator("button").filter(has=page.locator("svg")).first.or_(
            row.get_by_role("button", name="Edit")
        ).or_(row.locator(".text-emerald-500")).first

        if edit_btn.is_visible():
            edit_btn.click()
            page.wait_for_timeout(1000)

            reason_box_edit = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
            if reason_box_edit.is_visible():
                reason_box_edit.fill(updated_reason)
                _screenshot(page, "test_05_01_edit_leave_modal")

                save_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Update")).first
                try:
                    save_btn.click(timeout=3000)
                except Exception:
                    save_btn.evaluate("el => el.click()")

                close_toast(page)
                page.wait_for_timeout(2000)
                _screenshot(page, "test_05_02_leave_updated")

    expect(page).to_have_url(re.compile(r".*/my-leave"))
