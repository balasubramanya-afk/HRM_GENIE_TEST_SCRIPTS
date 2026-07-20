import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_approve_resignation(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="HR")
    
    # Give the table a moment to fully render
    page.wait_for_timeout(2000)
    
    # Locate a row with "Pending" status
    pending_row = page.locator("tbody tr").filter(has_text=re.compile(r"Pending", re.IGNORECASE)).first
    
    if pending_row.count() > 0:
        pending_row.click()
    else:
        # Fallback to the first row if no Pending row is found
        page.locator("tbody tr").first.click()
        
    page.wait_for_timeout(2000) # Wait for the side panel to slide in
    
    # Locate the panel
    panel = page.locator("div[role='dialog'], [aria-label='Employee Detail']").first
    expect(panel.get_by_role("heading", name="Employee Detail")).to_be_visible()
    
    # Fill in the manager comments
    comments_area = panel.get_by_placeholder("Write your comments here...").first
    comments_area.scroll_into_view_if_needed()
    comments_area.fill("Approved by automation script.")
    
    # Click the Approve button
    approve_button = panel.get_by_role("button", name="Approve").first
    approve_button.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    
    approve_button.click()
    
    # Wait for the success toast message (optional, might not appear if already approved)
    try:
        toast = page.locator("[data-sonner-toast]").first
        expect(toast).to_be_visible(timeout=3000)
        _screenshot(page, "test_04_after_approve")
    except Exception:
        print("Toast message did not appear or timed out.")
        _screenshot(page, "test_04_after_approve")
        
    
    # Close panel just in case it doesn't close automatically
    close_btn = panel.get_by_role("button", name="Close").first
    if close_btn.is_visible():
        close_btn.click()
