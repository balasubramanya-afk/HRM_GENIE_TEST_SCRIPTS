import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_dashboard_overview(page: Page):
    """6. Test dashboard quick metric links."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("link", name="New Joinees").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_06_dashboard_overview_new_joinees")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_role("link", name="Total check-Ins").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/new-hr-attendance.*"))
    _screenshot(page, "test_06_dashboard_overview_total_checkins")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_role("link", name="Late check-Ins").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/attendance-tracker-new.*"))
    _screenshot(page, "test_06_dashboard_overview_late_checkins")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_role("link", name="On Leave").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/all-employees-leaves.*"))
    _screenshot(page, "test_06_dashboard_overview_on_leave")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # Click the date filter (matching the date range button) and select "Today"
    page.get_by_role("button", name=re.compile(r"\d{4}")).first.click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Today", exact=True).click()
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_06_dashboard_overview_date_today")