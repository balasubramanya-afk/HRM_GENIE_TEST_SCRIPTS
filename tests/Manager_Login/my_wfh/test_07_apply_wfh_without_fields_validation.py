import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_apply_wfh_without_fields_validation(page: Page):
    """7. Negative: Try submitting Apply WFH form without required fields and verify validation."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/work-from-home")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Open Apply modal
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH")).first
    expect(apply_wfh_btn).to_be_visible()
    apply_wfh_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal is open
    expect(page.locator("[role='dialog']").first).to_be_visible()

    # Click Apply / Submit without filling fields
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(1000)

    # Verify validation messages or modal is still visible
    expect(page.get_by_text(re.compile(r"Start date is required|required|select", re.IGNORECASE)).first).to_be_visible()

    _screenshot(page, "test_07_apply_wfh_without_fields_validation")


