import re
from playwright.sync_api import expect
from test_07_tracker_view import do_login_tracker
from config import _screenshot

def test_tracker_filters(page):
    do_login_tracker(page)
    
    # 1. Open date picker and change date
    page.locator(".lucide.lucide-chevron-down").click()
    # Click previous month button once
    page.locator(".rdrNextPrevButton").first.click()
    # Select day 1
    page.get_by_role("button", name="1", exact=True).nth(1).click(force=True)
    page.wait_for_load_state("networkidle")
    
    # 2. Click Filters button and toggle check box
    page.get_by_role("button", name="Filters").click()
    page.get_by_role("checkbox", name="Late Arrivals").click()
    page.get_by_role("checkbox", name="Web Check-in").click()
    
    _screenshot(page, "tracker_filtered_state")
    
    # 3. Reset filters
    page.get_by_role("button", name="Reset").click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "tracker_filters_reset")
    
    page.wait_for_timeout(3000)
