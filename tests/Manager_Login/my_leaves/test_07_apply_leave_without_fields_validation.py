import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
)

def test_apply_leave_without_fields_validation(page: Page):
    """7. Negative Test: Click Apply in modal without selecting/filling any fields."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Click Apply Leave button to open modal
    apply_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave")).first
    apply_btn.click()
    page.wait_for_timeout(1000)

    # DO NOT fill any fields (leave Leave Type, Dates, Reason empty)
    # Directly click "Apply" / "Submit" button
    submit_btn = page.get_by_role("button", name="Apply").or_(page.get_by_role("button", name="Submit")).first
    submit_btn.click()
    page.wait_for_timeout(1000)

    _screenshot(page, "test_07_apply_without_fields_validation")

    # Assert modal remains open / submission is blocked
    dialog = page.locator("div[role='dialog']").or_(page.locator(".sheet-content")).first
    expect(dialog).to_be_visible()

    # Close modal clean up
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)
