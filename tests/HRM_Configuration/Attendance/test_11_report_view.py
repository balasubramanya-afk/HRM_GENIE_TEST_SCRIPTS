import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def do_login_report(page):
    """Reusable helper to log in and navigate to Attendance Report page."""
    do_login(page)
    page.get_by_role("button", name="Report").click()
    page.wait_for_load_state("networkidle")

def test_view_attendance_report(page):
    do_login_report(page)
    _screenshot(page, "attendance_report_default")
    
    # Verify default headers in the report list
    expect(page.get_by_text("Employee Id").first).to_be_visible()
    expect(page.get_by_text("Employee Name").first).to_be_visible()
    expect(page.get_by_text("Manager Name").first).to_be_visible()
    
    page.wait_for_timeout(3000)
