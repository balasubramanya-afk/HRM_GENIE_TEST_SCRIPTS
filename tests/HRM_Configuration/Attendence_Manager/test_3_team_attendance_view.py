import re
# pyrefly: ignore [missing-import]
from playwright.sync_api import expect
from test_1_login import do_login_manager
from config import _screenshot

def test_team_attendance_view(page):
    do_login_manager(page)
    
    # Switch to Team Attendance tab
    page.get_by_role("tab", name="Team Attendance").click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "team_attendance_default")
    
    # Verify Search textbox or other elements are visible
    expect(page.get_by_role("textbox", name="Search by shift type & status")).to_be_visible()
    
    page.wait_for_timeout(3000)
