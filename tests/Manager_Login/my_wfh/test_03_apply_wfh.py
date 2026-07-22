import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, select_next_available_date, get_picker_button

def test_create_wfh_request(page: Page):
    """3. Create a new Work From Home (WFH) request."""
    login_as(page, "Manager")
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Open Apply WFH modal
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH")).first
    expect(apply_wfh_btn).to_be_visible()
    apply_wfh_btn.click()
    page.wait_for_timeout(1000)

    # Verify modal is open
    modal_title = page.get_by_role("heading", name="Apply WFH").or_(page.get_by_text("Monthly WFH Balance:")).first
    expect(modal_title).to_be_visible()

    # Pick Start Date
    start_date_btn = get_picker_button(page, "Pick start date")
    expect(start_date_btn).to_be_visible()
    start_date_btn.click()
    assert select_next_available_date(page, start_offset=1), "Failed to select start date"
    page.wait_for_timeout(500)

    # Pick End Date
    end_date_btn = get_picker_button(page, "Pick end date")
    expect(end_date_btn).to_be_visible()
    end_date_btn.click()
    assert select_next_available_date(page, start_offset=1), "Failed to select end date"
    page.wait_for_timeout(500)

    # Fill Reason (10+ words)
    reason_input = page.get_by_placeholder("Enter your reason for work from home").or_(page.locator("textarea")).or_(page.get_by_role("textbox", name="Reason *")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("I am applying for work from home to perform automated test.")

    # Click Apply / Submit
    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Verify success toast or created entry
    success_indicator = page.get_by_text(re.compile(r"success|applied|created|submitted", re.IGNORECASE)).or_(page.locator("tbody tr")).first
    expect(success_indicator).to_be_visible()

    _screenshot(page, "test_03_create_wfh_request")



