import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, navigate_to_my_onduty

def test_cancel_apply_onduty_modal(page: Page):
    """8. Negative: Open Apply On Duty modal, enter details, and cancel modal without saving."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # Open Apply modal
    apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
    expect(apply_btn).to_be_visible()
    apply_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal dialog is open
    modal_dialog = page.locator("[role='dialog']").first
    expect(modal_dialog).to_be_visible()

    # Fill partial reason
    reason_input = page.get_by_role("textbox", name="Reason *").or_(page.locator("textarea")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("Testing cancel action")

    # Close modal (via Cancel button)
    close_btn = page.get_by_role("button", name="Cancel").or_(page.locator("button[aria-label='Close']")).first
    expect(close_btn).to_be_visible()
    close_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal dialog is dismissed
    expect(modal_dialog).not_to_be_visible()

    _screenshot(page, "test_08_cancel_apply_onduty_modal")
