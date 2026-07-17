import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_my_information(page: Page):
    """7. Test My Information section details."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="My Information").click()
    
    expect(page.get_by_text("Employee Id")).to_be_visible()
    expect(page.get_by_text("Name")).to_be_visible()
    expect(page.get_by_text("Job title")).to_be_visible()
    expect(page.get_by_text("Department")).to_be_visible()
    
    _screenshot(page, "test_07_my_information_overview")
    
    complete_profile = page.locator("button:has-text('Complete Your Profile')")
    if complete_profile.is_visible():
        complete_profile.click()
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/(my-profile|employee/general).*"))
        _screenshot(page, "test_07_complete_profile_page")
        page.go_back()
        page.wait_for_timeout(1000)
