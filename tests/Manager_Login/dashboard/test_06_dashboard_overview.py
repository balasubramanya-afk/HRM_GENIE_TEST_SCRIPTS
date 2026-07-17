import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_dashboard_overview(page: Page):
    """6. Test dashboard quick metric links."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    # 1. Leave Balance
    page.get_by_role("link", name=re.compile(r"Leave Balance")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/my-leave"))
    _screenshot(page, "test_06_overview_leave_balance")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Next Review
    page.get_by_role("link", name=re.compile(r"Next Review")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_06_overview_next_review")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3. Pending Leave Requests
    page.get_by_role("link", name=re.compile(r"Pending Leave Requests")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/my-leave.*"))
    _screenshot(page, "test_06_overview_pending_leave_requests")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 4. Attendance Overview
    page.get_by_role("link", name=re.compile(r"Attendance Overview")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/attendance-tracker-new.*"))
    _screenshot(page, "test_06_overview_attendance_overview")
    page.go_back()
    page.wait_for_timeout(1000)
