import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_logout(page: Page):
    """12. Test logging out from HR dashboard and verify browser Back button access is blocked."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    # Find the dynamic profile button and logout
    page.get_by_role("button", name=re.compile(r"Online$")).first.click()
    page.get_by_role("menuitem", name="Log out").click()
    page.wait_for_timeout(1000)
    
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    _screenshot(page, "test_12_logout_success")

    # Press browser Back button and verify dashboard is NOT accessible
    page.go_back()
    page.wait_for_timeout(1000)

    # Assert user remains blocked on Login page and Dashboard welcome header is NOT visible
    expect(page.get_by_role("button", name="Login")).to_be_visible()
    expect(page.get_by_role("heading", name=re.compile(r"Welcome", re.IGNORECASE))).not_to_be_visible()
    _screenshot(page, "test_12_logout_back_button_blocked")

