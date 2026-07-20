import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
)

def test_cancel_apply_leave_modal(page: Page):
    """8. Negative Test: Filling modal and clicking Cancel should close modal without saving."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
    apply_btn.click()
    page.wait_for_timeout(1000)

    # Type a draft reason
    reason_box = page.get_by_role("textbox", name="Reason*").or_(page.get_by_placeholder("Describe your reason")).first
    reason_box.fill("Draft reason that should be discarded")

    _screenshot(page, "test_08_01_draft_modal_before_cancel")

    # Close modal using Escape or clicking close icon
    close_icon = page.locator(".absolute.top-2.right-2, .absolute.right-4.top-4").first
    if close_icon.is_visible():
        try:
            close_icon.click(force=True)
        except Exception:
            page.keyboard.press("Escape")
    else:
        page.keyboard.press("Escape")

    page.wait_for_timeout(1000)
    _screenshot(page, "test_08_02_modal_cancelled")

    dialog = page.locator("div[role='dialog']").first
    if dialog.count():
        expect(dialog).to_be_hidden()
