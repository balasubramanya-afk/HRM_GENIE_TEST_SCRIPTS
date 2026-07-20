import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_logout(page: Page):
    """17. Test logging out from dashboard."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    # Find the dynamic profile button
    page.get_by_role("button", name=re.compile(r"Online$")).first.click()
    page.get_by_role("menuitem", name="Log out").click()
    
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    _screenshot(page, "test_17_logout")
