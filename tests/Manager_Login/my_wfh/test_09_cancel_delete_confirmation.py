import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_cancel_delete_confirmation(page: Page):
    """9. Negative: Click delete on WFH request but cancel confirmation dialog."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/work-from-home")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Find delete button, apply if needed
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    if not delete_btn.is_visible():
        apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).first
        if apply_wfh_btn.is_visible():
            apply_wfh_btn.click()
            page.wait_for_timeout(1000)

            start_date_btn = page.get_by_role("button", name="Pick start date").first
            if start_date_btn.is_visible():
                start_date_btn.click()
                page.get_by_role("button", name=re.compile(r"July 2[89]|July 30", re.I)).first.click()

            end_date_btn = page.get_by_role("button", name="Pick end date").first
            if end_date_btn.is_visible():
                end_date_btn.click()
                page.get_by_role("button", name=re.compile(r"July 2[89]|July 30", re.I)).first.click()

            reason_input = page.get_by_placeholder(re.compile(r"Enter your reason", re.IGNORECASE)).or_(page.locator("textarea")).or_(page.get_by_role("textbox", name="Reason *")).first
            if reason_input.is_visible():
                reason_input.fill("Applying for work from home request for cancel delete test case.")

            submit_btn = page.get_by_role("button", name="Apply").first
            if submit_btn.is_visible():
                submit_btn.click()
                page.wait_for_timeout(2000)

    # Expect delete button to be visible
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation modal is visible
    confirm_modal = page.locator("[role='dialog']").or_(page.get_by_text("You are cancelling your WFH")).first
    expect(confirm_modal).to_be_visible()

    # Click Cancel in confirmation modal
    cancel_btn = page.get_by_role("button", name="Cancel").or_(page.locator("button:has-text('Cancel')")).first
    expect(cancel_btn).to_be_visible()
    cancel_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation dialog is dismissed
    expect(confirm_modal).not_to_be_visible()

    _screenshot(page, "test_09_cancel_delete_confirmation")
