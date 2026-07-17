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
        _screenshot(page, f"test_10_team_overview_{btn_name.lower().replace(' ', '_')}")
