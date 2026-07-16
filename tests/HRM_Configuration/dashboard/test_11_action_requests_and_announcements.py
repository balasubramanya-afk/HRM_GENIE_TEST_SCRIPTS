import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_action_requests_and_announcements(page: Page):
    """11. Test Action Requests, Announcements, and Holidays."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Action Request").click()
    
    # Click on the Action Request 'Due' selector and then select 'Due' option
    page.locator("div").filter(has_text=re.compile(r"^Due$")).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Due").click()
    page.wait_for_timeout(1000)
    
    # Once selected, it navigates away. We verify and go back to dashboard.
    _screenshot(page, "test_11_action_request_due")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # Click Announcements and Holidays
    page.get_by_role("heading", name=re.compile(r"^Announcements")).click()
    page.get_by_role("heading", name="Current Month Holidays").click()
    _screenshot(page, "test_11_announcements_and_holidays")
