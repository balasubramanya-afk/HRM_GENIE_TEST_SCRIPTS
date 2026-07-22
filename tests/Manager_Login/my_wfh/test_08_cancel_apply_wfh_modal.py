import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_cancel_apply_wfh_modal(page: Page):
    """8. Negative: Open Apply WFH modal, enter details, and cancel modal without saving."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/leaves/work-from-home")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Open Apply modal
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH")).first
    expect(apply_wfh_btn).to_be_visible()
    apply_wfh_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal dialog is open
    modal_dialog = page.locator("[role='dialog']").first
    expect(modal_dialog).to_be_visible()

    # Enter partial data
    reason_input = page.get_by_placeholder("Enter your reason for work from home").or_(page.locator("textarea")).or_(page.get_by_role("textbox", name="Reason *")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("Testing cancel action modal verification for work from home form request.")

    # Close modal using Cancel button
    cancel_btn = page.get_by_role("button", name="Cancel").first
    expect(cancel_btn).to_be_visible()
    cancel_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal is dismissed
    expect(modal_dialog).not_to_be_visible()

    _screenshot(page, "test_08_cancel_apply_wfh_modal")

