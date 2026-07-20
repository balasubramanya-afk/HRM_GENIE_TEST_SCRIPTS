import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_announcements_and_holidays(page: Page):
    """16. Test Announcements and current month's holidays sections."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name=re.compile(r"^Announcements")).click()
    page.get_by_role("heading", name=re.compile(r"Current Month's Holidays$")).click()
    
    _screenshot(page, "test_15_announcements_and_holidays")
