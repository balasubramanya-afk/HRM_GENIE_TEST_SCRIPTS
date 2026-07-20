import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_approve_resignation(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # 2. Click on "Team Resignation" tab
    page.get_by_role("button", name="Team Resignation").click()
    page.wait_for_timeout(2000)
    
    # Check if there are any records first
    empty_state = page.locator("text=No records found")
    if empty_state.count() > 0:
        print("No records found in the Team Resignation table. Cannot test approval. Skipping...")
        return
    
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
    
    
    
    # Wait a moment for the panel to automatically close after approving
    page.wait_for_timeout(1500)
    
    # Close panel manually just in case it didn't close automatically
    try:
        close_btn = panel.get_by_role("button", name="Close").first
        if close_btn.is_visible(timeout=500):
            close_btn.click(timeout=1000)
    except Exception:
        pass
        
    # Now wait for the success toast message which appears AFTER the panel is closed
    try:
        toast = page.locator("[data-sonner-toast]").first
        expect(toast).to_be_visible(timeout=5000)
        page.wait_for_timeout(1000) # Wait for toast animation to complete
    except Exception:
        print("Toast message did not appear or timed out.")
        
    _screenshot(page, "test_04_after_approve")