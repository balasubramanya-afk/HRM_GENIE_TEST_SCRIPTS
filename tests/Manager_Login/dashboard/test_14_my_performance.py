import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_my_performance(page: Page):
    """15. Test My Performance buttons and navigation."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="My Performance").click()
    
    # 1. Submit Self Assessment
    page.get_by_role("button", name="Submit Self Assessment").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_15_my_performance_submit_self")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. View Manager Feedback
    page.get_by_role("button", name="View Manager Feedback").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_15_my_performance_view_feedback")
    page.go_back()
    page.wait_for_timeout(1000)
