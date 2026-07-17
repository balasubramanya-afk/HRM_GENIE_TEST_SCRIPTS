import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_teams_performance_reviews(page: Page):
    """14. Test Team's Performance Reviews section."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Team's Performance Reviews").click()
    page.get_by_role("button", name="Reviews due").click()
    page.wait_for_timeout(1000)
    
    expect(page).to_have_url(re.compile(r".*/internal-performance/review-team-member.*"))
    _screenshot(page, "test_14_teams_performance_reviews")
    
    page.go_back()
    page.wait_for_timeout(1000)
