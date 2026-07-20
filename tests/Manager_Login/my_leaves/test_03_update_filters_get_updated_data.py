import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_update_filters_get_updated_data(page: Page):
    """3. Verify updating filters to Casual Leave updates grid data to show only Casual Leave."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # 1. Select "Casual Leave" in Leave Type filter dropdown
    leave_type_combo = page.get_by_role("combobox").filter(has_text=re.compile(r"All (Leave )?Type", re.IGNORECASE)).first
    if not leave_type_combo.is_visible():
        leave_type_combo = page.get_by_role("combobox").nth(0)

    expect(leave_type_combo).to_be_visible()
    leave_type_combo.click()
    page.wait_for_timeout(500)

    casual_leave_option = page.get_by_role("option", name="Casual Leave").first
    expect(casual_leave_option).to_be_visible()
    casual_leave_option.click()
    page.wait_for_timeout(1000)

    # Verify dropdown filter now displays "Casual Leave"
    selected_filter = page.get_by_role("combobox").filter(has_text="Casual Leave").first
    expect(selected_filter).to_be_visible()

    # Verify UI table records show only Casual Leave
    rows = page.locator("tbody tr")
    row_count = rows.count()
    if row_count > 0:
        for i in range(row_count):
            row_text = rows.nth(i).inner_text()
            # If the row has content (not an empty state placeholder row)
            if "No " not in row_text and "no " not in row_text:
                expect(rows.nth(i)).to_contain_text("Casual Leave")

    _screenshot(page, "test_03_filter_by_casual_leave")

    # 2. Update Status filter
    status_combo = page.get_by_role("combobox").filter(has_text=re.compile(r"All Status|Status", re.IGNORECASE)).first
    if not status_combo.is_visible() and page.get_by_role("combobox").count() > 1:
        status_combo = page.get_by_role("combobox").nth(1)

    if status_combo.is_visible():
        status_combo.click()
        page.wait_for_timeout(500)
        pending_option = page.get_by_role("option", name="Pending").first
        if pending_option.is_visible():
            pending_option.click()
            page.wait_for_timeout(1000)

    _screenshot(page, "test_03_filter_by_status")

    # 3. Test "Reset Filters" button
    reset_btn = page.get_by_role("button", name="Reset Filters").or_(page.get_by_text("Reset Filters")).first
    if reset_btn.is_visible():
        reset_btn.click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_03_reset_filters")

    expect(page).to_have_url(re.compile(r".*/my-leave"))
