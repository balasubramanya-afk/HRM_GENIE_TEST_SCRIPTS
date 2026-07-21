import re
from playwright.sync_api import expect
from config import login_as, _screenshot

def do_login(page):
    """Reusable login helper for Attendance tests."""
    login_as(page, "HR")
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")

def test_view_attendance_overview(page):
    do_login(page)
    _screenshot(page, "attendance_overview_default")
    
    # Verify default page elements are loaded (covering Overview View Page with default filters)
    expect(page.get_by_text("Total Employees")).to_be_visible(timeout=10000)
    expect(page.get_by_text("Daily Attednance")).to_be_visible()
    
    page.wait_for_timeout(3000)
