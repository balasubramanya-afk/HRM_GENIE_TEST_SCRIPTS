import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_leave_wfh(page: Page):
    """12. Test Leave & WFH navigation buttons."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_text("Leave & WFH").click()
    
    # 1. Apply For Leave
    page.get_by_role("button", name="Apply For Leave").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/my-leave"))
    _screenshot(page, "test_12_leave_wfh_apply_leave")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Request WFH
    page.get_by_role("button", name="Request WFH").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/work-from-home"))
    _screenshot(page, "test_12_leave_wfh_request_wfh")
    page.go_back()
    page.wait_for_timeout(1000)
