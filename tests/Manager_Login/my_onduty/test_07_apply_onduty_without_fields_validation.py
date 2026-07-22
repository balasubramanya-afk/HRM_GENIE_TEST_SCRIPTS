import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, navigate_to_my_onduty

def test_apply_onduty_without_fields_validation(page: Page):
    """7. Negative: Try submitting Apply On Duty form without required fields and verify validation."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # Open Apply modal
    apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
    expect(apply_btn).to_be_visible()
    apply_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal is open
    expect(page.locator("[role='dialog']").first).to_be_visible()

    # Click Apply without filling mandatory fields
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(1000)

    # Verify validation errors / modal remains visible
    expect(page.locator("[role='dialog']").first).to_be_visible()

    _screenshot(page, "test_07_apply_onduty_without_fields_validation")
