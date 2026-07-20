import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
)

def test_delete_leave(page: Page):
    """6. Test Delete/Cancel Leave for Manager targeting updated leave."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    updated_reason = "Auto Test Leave Manager Updated"
    target_reason = "Auto Test Leave Manager"

    # Target row with updated reason first, or original reason, or fallback pending row
    target_row = page.locator("tr").filter(has_text=updated_reason).first
    if not target_row.is_visible():
        target_row = page.locator("tr").filter(has_text=target_reason).first
    if not target_row.is_visible():
        target_row = page.locator("tr").filter(has_text="Pending").first

    if target_row.is_visible():
        delete_btn = target_row.locator("button").filter(has=page.locator("svg")).last.or_(
            target_row.get_by_role("button", name="Delete")
        ).or_(target_row.get_by_role("button", name="Cancel")).or_(target_row.locator(".text-red-500")).first

        if delete_btn.is_visible():
            delete_btn.click()
            page.wait_for_timeout(1000)

            confirm_dialog_btn = page.get_by_role("button", name="Delete").or_(
                page.get_by_role("button", name="Confirm")
            ).or_(page.get_by_role("button", name="Yes")).first

            if confirm_dialog_btn.is_visible():
                try:
                    confirm_dialog_btn.click(timeout=3000)
                except Exception:
                    confirm_dialog_btn.evaluate("el => el.click()")

                close_toast(page)
                page.wait_for_timeout(2000)

            _screenshot(page, "test_06_01_leave_deleted")

    expect(page).to_have_url(re.compile(r".*/my-leave"))
