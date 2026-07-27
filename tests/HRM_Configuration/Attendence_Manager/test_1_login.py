import re
from playwright.sync_api import expect
from config import login_as, _screenshot

def do_login_manager(page):
    """Reusable login helper for Manager role."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/attendance-tracker-new")
    page.wait_for_load_state("networkidle")

def test_login(page):
    do_login_manager(page)
    _screenshot(page, "my_attendance_default")
    
    # Verify default headers or tabs
    expect(page.get_by_role("tab", name="My Attendance")).to_be_visible()
    
    page.wait_for_timeout(3000)
