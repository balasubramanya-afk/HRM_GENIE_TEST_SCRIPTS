from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications

def test_login_and_navigate_to_certifications(page):
    login_and_navigate_to_certifications(page, role="Manager")
    
    # Verify key elements are visible
    expect(page.get_by_role("heading", name="Certifications").first).to_be_visible()
    expect(page.locator("button").filter(has_text="Add Certification")).to_be_visible()
    
    
    # Verify the footer text is visible on the page
    expect(page.get_by_text("Outstrive © 2026. All Rights Reserved.")).to_be_visible()
    
    # Wait for 3 seconds to let you see the Policies page before it closes
    page.wait_for_timeout(3000)
    _screenshot(page, "test_01_login")
   