import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, select_next_available_date, get_picker_button

def test_edit_wfh(page: Page):
    """5. Edit an existing pending Work From Home (WFH) request."""
    login_as(page, "Manager")
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Check if an enabled edit button exists in table for a pending request
    edit_btn = page.locator("tbody tr button.text-emerald-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-pencil):not([disabled])")).first
    if not edit_btn.is_visible():
        # Apply for WFH first so there is a pending request to edit
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
        reason_input.fill("Applying for work from home request to prepare edit test case.")

        submit_btn = page.get_by_role("button", name="Apply").first
        expect(submit_btn).to_be_visible()
        submit_btn.click()
        page.wait_for_timeout(2000)

    # Click edit button in table body for the pending WFH request
    edit_btn = page.locator("tbody tr button.text-emerald-500:not([disabled])").or_(page.locator("tbody tr button:has(svg.lucide-pencil):not([disabled])")).first
    expect(edit_btn).to_be_visible()
    edit_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal opened
    expect(page.locator("[role='dialog']").first).to_be_visible()

    # Update reason with 10+ words matching sample.py
    reason_input = page.get_by_role("textbox", name="Reason *").or_(page.get_by_placeholder(re.compile(r"Enter your reason", re.IGNORECASE))).or_(page.locator("textarea")).first
    expect(reason_input).to_be_visible()
    reason_input.click()
    reason_input.fill("test test test test test test test test test test update")

    # Click Apply
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(1000)

    # Verify toast notification message
    toast = page.get_by_text("Success!").or_(page.get_by_text("WFH request updated")).or_(page.get_by_text(re.compile(r"updated", re.IGNORECASE))).first
    expect(toast).to_be_visible()

    _screenshot(page, "test_05_edit_wfh")







