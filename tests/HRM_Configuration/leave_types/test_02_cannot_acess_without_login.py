from playwright.sync_api import expect, Page
from .config import _screenshot

def test_leave_types_unauthorized_anon(page: Page):
    """10. Verify unauthenticated users cannot access the Leave Types page."""
    page.goto("https://qa.hrmgenie.outstrive.co/hrm-config/leave-types")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_cannot_acess_without_login")
    
    # Depending on frontend logic, it may redirect to login or just show an Unauthorized page.
    assert "login" in page.url or page.get_by_text("Unauthorized").is_visible(), f"SECURITY BUG: Unauthenticated user was able to access {page.url}!"
