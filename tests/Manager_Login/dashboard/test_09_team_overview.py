import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_team_overview(page: Page):
    """10. Test Team Overview tab buttons."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Team Overview").click()
    
    buttons = ["On Leave", "Probation", "Who is in", "Late Arrival"]
    for btn_name in buttons:
        page.get_by_role("button", name=btn_name).click()
        page.wait_for_timeout(500)
        expect(page).to_have_url(re.compile(r".*/dashboard"))
        
        # Verify either "No team members to display" or team member details with "BITECOS" is visible
        expect(
            page.get_by_text(re.compile(r"(No team members to display|BITECOS)", re.IGNORECASE)).first
        ).to_be_visible()
        
        # If BITECOS is displayed, test "View Profile" link/button navigation
        bitecos_locator = page.get_by_text(re.compile(r"BITECOS", re.IGNORECASE)).first
        if bitecos_locator.is_visible():
            view_profile = page.get_by_role("link", name="View Profile").or_(page.get_by_role("button", name="View Profile")).or_(page.get_by_text("View Profile")).first
            if view_profile.is_visible():
                view_profile.click()
                page.wait_for_timeout(1000)
                expect(page).to_have_url(re.compile(r".*/employee/details/.*"))
                _screenshot(page, f"test_09_team_overview_{btn_name.lower().replace(' ', '_')}_profile")
                page.go_back()
                page.wait_for_timeout(1000)
        
        _screenshot(page, f"test_09_team_overview_{btn_name.lower().replace(' ', '_')}")
