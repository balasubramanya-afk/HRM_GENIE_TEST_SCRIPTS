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

    # Step 1: Update Status Filter (Select Status Filter -> Approved)
    combobox = page.get_by_role("tabpanel", name="My WFH").get_by_role("combobox").first
    expect(combobox).to_be_visible()
    combobox.click()
    page.wait_for_timeout(500)

    approved_option = page.get_by_role("option", name="Approved").first
    expect(approved_option).to_be_visible()
    approved_option.click()
    page.wait_for_timeout(2000)

    expect(combobox).to_contain_text("Approved")

    # Verify no row in the table has "Pending" status when Approved filter is active
    pending_rows_in_approved_filter = page.locator("tbody tr").filter(
        has_text=re.compile(r"\bPending\b", re.IGNORECASE)
    )
    assert pending_rows_in_approved_filter.count() == 0, (
        "Filter by 'Approved' is not working — Pending rows are still visible in the table."
    )

    # Step 2: Click Reset Filters
    reset_btn = page.get_by_role("button", name="Reset Filters").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1000)

    # Verify reset restored combobox or default status
    expect(combobox).to_contain_text("All Status")

    _screenshot(page, "test_04_update_filters_get_updated_data")
