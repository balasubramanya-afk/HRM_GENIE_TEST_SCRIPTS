import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_quick_action_onboard(page: Page):
    """7. Test Quick Action dropdown -> Onboard and Leaves."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    # 1. Click Quick Action -> Onboard
    page.get_by_role("heading", name="Quick Action").click()
    page.get_by_role("link", name="Onboard").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/on-board.*"))
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Click Quick Action -> Leaves
    page.get_by_role("heading", name="Quick Action").click()
    page.get_by_role("link", name="Leaves").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/all-employees-leaves.*"))
    page.go_back()
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_07_quick_action")
