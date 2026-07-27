import re
from playwright.sync_api import expect
from test_1_login import do_login_manager
from config import _screenshot

def test_my_attendance_filters(page):
    do_login_manager(page)
    
    # 1. Update date range filter
    page.locator(".lucide.lucide-chevron-down").click()
    # Click previous month button
    page.locator(".rdrNextPrevButton").first.click()
    # Select day 1
    page.get_by_role("button", name="1", exact=True).nth(1).click(force=True)
    page.wait_for_load_state("networkidle")
    
    # 2. Click Filters button and toggle check box
    page.get_by_role("button", name="Filters").click()
    page.get_by_role("checkbox", name="Late Arrivals").click(force=True)
    
    _screenshot(page, "my_attendance_filtered")
    
    # 3. Reset filters
    page.get_by_role("button", name="Reset").first.click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "my_attendance_reset")
    
    page.wait_for_timeout(3000)
