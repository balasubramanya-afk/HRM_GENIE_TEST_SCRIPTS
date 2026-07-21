import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_update_attendance_filters(page):
    do_login(page)
    
    # 1. Update Month Filter
    page.get_by_role("combobox").filter(has_text="Select month").click()
    page.get_by_role("option", name="Jun").click()
    page.wait_for_load_state("networkidle")
    
    # 2. Update Department Filter
    page.get_by_role("button", name="Department").click()
    # Click Testing department (using force=True to ensure it works with checkboxes)
    page.get_by_role("button", name="Testing").click(force=True)
    # Close the popover by pressing Escape
    page.keyboard.press("Escape")
    page.wait_for_load_state("networkidle")
    
    # Take screenshot of filtered state
    _screenshot(page, "attendance_filtered_june_testing")
    
    # 3. Reset Filters
    page.get_by_role("button", name="Reset").click()
    page.wait_for_load_state("networkidle")
    
    # Take screenshot of reset state
    _screenshot(page, "attendance_filters_reset")
    
    page.wait_for_timeout(3000)
