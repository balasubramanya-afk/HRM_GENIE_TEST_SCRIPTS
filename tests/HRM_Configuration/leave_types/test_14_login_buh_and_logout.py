import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_login_buh_and_logout(page: Page):
    """14. Login as BUH and then log out."""
    # Login as Business Unit Head
    login_as(page, "BUH")
    
    # Ensure dashboard is loaded
    page.wait_for_timeout(2000)
    _screenshot(page, "test_14_buh_logged_in")
    
    # Find the profile button (usually named something like 'GA Online', 'RA Online', etc.)
    # We use a regex to match any button ending with 'Online'
    profile_button = page.get_by_role("button", name=re.compile(r"Online$", re.IGNORECASE)).first
    profile_button.click()
    
    # Click Log out
    page.get_by_role("menuitem", name="Log out").click()
    page.wait_for_timeout(1000)
    
    # Verify we are successfully redirected back to the login page
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    
    _screenshot(page, "test_14_buh_logged_out")
