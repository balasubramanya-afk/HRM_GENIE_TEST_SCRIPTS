import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, select_next_available_date, get_picker_button

def test_delete_wfh(page: Page):
    """6. Delete a pending WFH request and verify confirmation toast."""
    login_as(page, "Manager")
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Check if an enabled trash button exists in table for a pending request
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    if not delete_btn.is_visible():
        # Apply for WFH first so there is a pending request to delete
        apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).first
        expect(apply_wfh_btn).to_be_visible()
        apply_wfh_btn.click()
        page.wait_for_timeout(1000)

        start_date_btn = get_picker_button(page, "Pick start date")
        expect(start_date_btn).to_be_visible()
        start_date_btn.click()
        assert select_next_available_date(page, start_offset=1), "Failed to select start date"
        page.wait_for_timeout(500)

        end_date_btn = get_picker_button(page, "Pick end date")
        expect(end_date_btn).to_be_visible()
        end_date_btn.click()
        assert select_next_available_date(page, start_offset=1), "Failed to select end date"
        page.wait_for_timeout(500)

        reason_input = page.get_by_placeholder(re.compile(r"Enter your reason", re.IGNORECASE)).or_(page.locator("textarea")).or_(page.get_by_role("textbox", name="Reason *")).first
        expect(reason_input).to_be_visible()
        reason_input.fill("Applying for work from home request to prepare delete test case.")

        submit_btn = page.get_by_role("button", name="Apply").first
        expect(submit_btn).to_be_visible()
        submit_btn.click()
        page.wait_for_timeout(2000)

    # Click delete button in table body for the pending WFH request
    delete_btn = page.locator("tbody tr button.text-red-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-trash-2):not([disabled])")).first
    expect(delete_btn).to_be_visible()
    delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify confirmation dialog text from sample.py
    expect(page.get_by_text("You are cancelling your WFH").or_(page.get_by_text("Delete")).first).to_be_visible()

    # Click Delete in confirmation dialog
    confirm_delete_btn = page.get_by_role("button", name="Delete").last
    expect(confirm_delete_btn).to_be_visible()
    confirm_delete_btn.click()
    page.wait_for_timeout(1000)

    # Verify deletion toast notification from sample.py
    toast = page.get_by_text("WFH request deleted").or_(page.get_by_text("Your request has been")).or_(page.get_by_text("deleted")).first
    expect(toast).to_be_visible()

    _screenshot(page, "test_06_delete_wfh")

