import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_my_tasks(page: Page):
    """Merged Test: My Tasks, Team's Performance Reviews, and My Performance sections."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    # 1. My Tasks Section
    
    heading = page.get_by_role("heading", name="My Tasks")
    expect(heading).to_be_visible()
    heading.click()
    _screenshot(page, "test_12_my_tasks")
    
    # 2. Team's Performance Reviews Section
    page.get_by_role("heading", name="Team's Performance Reviews").click()
    page.get_by_role("button", name="Reviews due").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance/review-team-member.*"))
    _screenshot(page, "test_12_teams_performance_reviews")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3. My Performance Section 
    page.get_by_role("heading", name="My Performance").click()
    
    # 3a. Submit Self Assessment
    page.get_by_role("button", name="Submit Self Assessment").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_12_my_performance_submit_self")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3b. View Manager Feedback
    page.get_by_role("button", name="View Manager Feedback").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_12_my_performance_view_feedback")
    page.go_back()
    page.wait_for_timeout(1000)
