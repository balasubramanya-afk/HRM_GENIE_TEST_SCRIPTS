import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_verify_logo_navigation(page: Page):
    """2. Check HRM logo is present and clicking navigates to dashboard."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    logo = page.get_by_role("link", name="Outstrive")
    expect(logo).to_be_visible()
    
    # Navigate away to test the logo click
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_timeout(1000)
    
    # Click logo to return to dashboard
    logo.click()
    page.wait_for_timeout(2000)
    
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    _screenshot(page, "test_02_verify_logo_navigation")
