import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_mark_attendance(page: Page):
    """11. Test Mark Attendance section headers and details."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Mark Attendance").click()
    page.get_by_role("heading", name="Your Shift Timings").click()
    
    expect(page.get_by_text("Check-In")).to_be_visible()
    expect(page.get_by_text("Check-Out")).to_be_visible()
    expect(page.get_by_text("Total Hours")).to_be_visible()
    
    _screenshot(page, "test_11_mark_attendance")
