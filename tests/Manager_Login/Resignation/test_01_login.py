import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation


def test_view_resignation(page):
    # 1. Login and navigate to resignation module
    login_and_navigate_to_resignation(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # 2. Verify "My Resignation" is selected by default
    # The active tab might have a specific class or we just verify its content is visible.
    expect(page.get_by_role("button", name="My Resignation")).to_be_visible()
    
    # 3. Check elements on "My Resignation" tab
    expect(page).to_have_url(re.compile(r".*/my-resignation"))
    
    # Check if resignation is already applied
    apply_btn = page.get_by_role("button", name="Apply Resignation")
    applied_badge = page.locator("text=Resignation Applied")
    
    if apply_btn.count() > 0:
        # Empty state
        expect(apply_btn).to_be_visible()
        expect(page.locator("text=No resignation requests found.")).to_be_visible()
    else:
        # Applied state
        expect(applied_badge).to_be_visible()
        expect(page.locator("text=Pending")).to_be_visible()
        
    # Verify the footer text is visible on the page
    expect(page.get_by_text("Outstrive © 2026. All Rights Reserved.")).to_be_visible()
    
    
    _screenshot(page, "test_01_login_my_resignation")
    
    # 4. Click on "Team Resignation" tab
    page.get_by_role("button", name="Team Resignation").click()
    page.wait_for_timeout(2000)
    
    # 5. Check elements on "Team Resignation" tab
    expect(page).to_have_url(re.compile(r".*/team-resignation"))
    expect(page.get_by_role("heading", name="Team Resignation")).to_be_visible()
    expect(page.get_by_placeholder("Search by name or ID")).to_be_visible()
    expect(page.get_by_text("Reset Filters")).to_be_visible()
    
    # Verify table headers
    table_headers = ["Employee ID", "Employee Name", "Reason for Leaving", "Manager Comment", "Status"]
    for header in table_headers:
        expect(page.locator("div").filter(has_text=re.compile(f"^{header}$")).first).to_be_visible()
    # Verify the footer text is visible on the page
    expect(page.get_by_text("Outstrive © 2026. All Rights Reserved.")).to_be_visible()
        
    _screenshot(page, "test_01_login_team_resignation")
