from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_login(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="HR")
    # Verify the footer text is visible on the page
    expect(page.get_by_text("Outstrive © 2026. All Rights Reserved.")).to_be_visible()
    
    # Verify Heading
    expect(page.get_by_role("heading", name="All Resignation")).to_be_visible()
    
    # Verify Export Button
    expect(page.get_by_role("button", name="Export")).to_be_visible()
    
    # Verify Search Input
    expect(page.get_by_placeholder("Search by name or ID")).to_be_visible()
    
    # Verify Reset Filters
    expect(page.get_by_text("Reset Filters")).to_be_visible()
    
    # Verify Table Headers (using text matching as they might not be standard <th> elements)
    for header in ["Employee ID", "Employee Name", "Department", "Designation", "Manager", "Manager Status"]:
        expect(page.get_by_text(header, exact=True)).to_be_visible()

    # Take a screenshot to verify successful navigation
    _screenshot(page, "test_01_login")
