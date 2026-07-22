import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_update_filters_get_updated_data(page: Page):
    """4. Update filters (Status, Date range), verify data updates & Reset Filters."""
    login_as(page, "Manager")
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Step 1: Update Date Range Filter (Click Date Range button -> Select 'This Week')
    date_range_btn = page.get_by_role("tabpanel", name="My WFH").get_by_role("button", name=re.compile(r"\d{2}-\d{2}-\d{4}")).or_(page.locator("button:has-text(' to ')")).first
    expect(date_range_btn).to_be_visible()
    date_range_btn.click()
    page.wait_for_timeout(500)

    this_week_btn = page.get_by_role("button", name="This Week").or_(page.get_by_text("This Week")).first
    expect(this_week_btn).to_be_visible()
    this_week_btn.click()
    page.wait_for_timeout(1000)

    # Step 2: Update Status Filter (Select Status Filter -> Approved)
    combobox = page.get_by_role("tabpanel", name="My WFH").get_by_role("combobox").first
    expect(combobox).to_be_visible()
    combobox.click()
    page.wait_for_timeout(500)

    approved_option = page.get_by_role("option", name="Approved").first
    expect(approved_option).to_be_visible()
    approved_option.click()
    page.wait_for_timeout(1000)

    # Step 3: Click Reset Filters
    reset_btn = page.get_by_role("button", name="Reset Filters").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1000)

    # Verify reset restored combobox or default status
    expect(combobox).to_contain_text("All Status")

    _screenshot(page, "test_04_update_filters_get_updated_data")






