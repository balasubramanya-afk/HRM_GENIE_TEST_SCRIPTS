import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_access_team_leaves_as_employee(page: Page):
    """1. Verify Employee role cannot access Team Leaves page."""
    login_as(page, "Employee")
    page.wait_for_load_state("networkidle")
    
    # Attempt navigation to team-leaves
    page.goto("https://qa.hrmgenie.outstrive.co/team-leaves")
    page.wait_for_timeout(2000)

    # Verify Employee is redirected away from /team-leaves or restricted
    current_url = page.url
    is_redirected = "/team-leaves" not in current_url or page.get_by_text(re.compile(r"404|Forbidden|Not Found|Unauthorized", re.IGNORECASE)).count() > 0 or not page.get_by_role("button", name=re.compile(r"Approve Selected|Approve|Reject", re.IGNORECASE)).is_visible()
    
    assert is_redirected, f"Employee was able to access Team Leaves! Current URL: {current_url}"

    _screenshot(page, "test_01_access_team_leaves_as_employee")
