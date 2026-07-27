import re
# pyrefly: ignore [missing-import]
from playwright.sync_api import expect
from test_1_login import do_login_manager
from config import _screenshot

def test_team_attendance_filters(page):
    do_login_manager(page)
    
    # 1. Switch to Team Attendance tab
    page.get_by_role("tab", name="Team Attendance").click()
    page.wait_for_load_state("networkidle")
    
    # 2. Update date range filter
    page.locator(".lucide.lucide-chevron-down").click()
    page.locator(".rdrNextPrevButton").first.click()
    page.get_by_role("button", name="1", exact=True).nth(1).click(force=True)
    page.wait_for_load_state("networkidle")
    
    # 3. Use Search box
    page.get_by_role("textbox", name="Search by shift type & status").fill("1348")
    page.get_by_role("textbox", name="Search by shift type & status").press("Enter")
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "team_attendance_searched")
    
    # 4. Use checkbox filters
    page.get_by_role("button", name="Filters").click()
    page.get_by_role("checkbox", name="Late Arrivals").click(force=True)
    page.get_by_role("checkbox", name="Web Check-in").click(force=True)
    
    _screenshot(page, "team_attendance_filtered")
    
    # 5. Reset
    page.get_by_role("button", name="Reset").first.click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "team_attendance_reset")
    
    page.wait_for_timeout(3000)
