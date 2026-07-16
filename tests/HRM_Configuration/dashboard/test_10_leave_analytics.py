import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_leave_analytics(page: Page):
    """10. Test Leave Analytics section."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Leave Analytics").click()
    
    # Click the date filter for Leave Analytics and select "Last 7 days"
    page.get_by_role("button", name=re.compile(r"\d{4}")).nth(1).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Last 7 days").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_10_leave_analytics_filtered")
    
    # Selecting leave portions from analytics chart
    page.get_by_text("Sick Leave").first.click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_10_sick_leave_analytics")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_text("Paternity Leave").first.click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_10_paternity_leave_analytics")
    page.go_back()
    page.wait_for_timeout(1000)
