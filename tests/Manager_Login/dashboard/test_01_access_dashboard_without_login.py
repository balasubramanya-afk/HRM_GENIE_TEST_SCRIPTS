import re
from playwright.sync_api import expect, Page
from .config import _screenshot

def test_access_dashboard_without_login(page: Page):
    """1. Navigate to dashboard URL without logging in."""
    page.goto("https://qa.hrmgenie.outstrive.co/dashboard")
    page.wait_for_timeout(2000)
    
    # Verify redirected back to login page
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    _screenshot(page, "test_01_access_dashboard_without_login")
