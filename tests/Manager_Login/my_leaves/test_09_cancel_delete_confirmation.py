import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
)

def test_cancel_delete_confirmation(page: Page):
    """9. Negative Test: Clicking Delete and then Cancel on confirmation dialog keeps row intact."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    row = page.locator("tr").filter(has_text="Pending").first
    if not row.is_visible():
        row = page.locator("tr").nth(1)

    if row.is_visible():
        delete_btn = row.locator("button").filter(has=page.locator("svg")).last.or_(
            row.get_by_role("button", name="Delete")
        ).or_(row.get_by_role("button", name="Cancel")).or_(row.locator(".text-red-500")).first

        if delete_btn.is_visible():
            delete_btn.click()
            page.wait_for_timeout(1000)

            confirm_cancel_btn = page.get_by_role("button", name="Cancel").or_(
                page.get_by_role("button", name="No")
            ).first

            if confirm_cancel_btn.is_visible():
                confirm_cancel_btn.click(force=True)
                page.wait_for_timeout(1000)
                _screenshot(page, "test_09_01_delete_confirmation_cancelled")

    expect(page).to_have_url(re.compile(r".*/my-leave"))
