from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_leave_types_unauthorized_employee(page: Page):
    """1. Verify unauthorized users (Employee) cannot access the Leave Types page."""
    login_as(page, "Employee")
    page.goto("https://qa.hrmgenie.outstrive.co/hrm-config/leave-types")
    page.wait_for_timeout(2000)
    # Check if redirect happened or unauthorized message is visible
    assert "/hrm-config/leave-types" not in page.url or page.get_by_text("Unauthorized").is_visible()
    _screenshot(page, "test_01_unauthorized_employee")
