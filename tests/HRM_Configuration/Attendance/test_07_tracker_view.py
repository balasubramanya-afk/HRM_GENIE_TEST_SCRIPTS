import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def do_login_tracker(page):
    """Reusable helper to log in and navigate to Attendance Tracker."""
    do_login(page)
    page.get_by_role("button", name="Attendance Tracker").click()
    page.wait_for_load_state("networkidle")

def test_view_attendance_tracker(page):
    do_login_tracker(page)
    _screenshot(page, "attendance_tracker_default")
    
    # Verify default headers in the tracker table
    expect(page.get_by_text("Employee Id").first).to_be_visible()
    expect(page.get_by_text("Employee Name").first).to_be_visible()
    
    page.wait_for_timeout(3000)
