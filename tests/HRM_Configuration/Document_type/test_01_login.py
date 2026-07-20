from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type

def test_login(page):
    login_and_navigate_to_document_type(page, role="HR")
    
    # Verify key elements are visible
    expect(page.get_by_role("heading", name="Document Type")).to_be_visible()
    expect(page.get_by_role("button", name="+ Document Type")).to_be_visible()
    expect(page.get_by_placeholder("Search")).to_be_visible()
    expect(page.get_by_text("Actions", exact=True)).to_be_visible()
    
    # Verify the footer text is visible on the page
    expect(page.get_by_text("Outstrive © 2026. All Rights Reserved.")).to_be_visible()
    
    # Wait for 3 seconds to let you see the Document Type page before it closes
    page.wait_for_timeout(3000)
    _screenshot(page, "test_01_login")
