import random
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_resignation_details(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="HR")
    
    # Give the table a moment to fully render
    page.wait_for_timeout(2000)
    
    # Locate all rows in the table
    rows = page.locator("tbody tr")
    count = rows.count()
    assert count > 0, "No rows found in the table to click!"
    
    # Pick a random row and click it
    random_index = random.randint(0, count - 1)
    random_row = rows.nth(random_index)
    
    random_row.click()
    page.wait_for_timeout(2000) # Wait for the side panel to slide in
    
    # Locate the panel to avoid strict mode violations with background elements
    panel = page.locator("div[role='dialog'], [aria-label='Employee Detail']").first
    
    # Verify the side panel opens with the "Employee Detail" header
    expect(panel.get_by_role("heading", name="Employee Detail")).to_be_visible()
    
    # Verify all expected labels/elements are present in the details panel
    expected_labels = [
        "Reason For Leaving",
        "Employee Performance",
        "Position",
        "Work Information",
        "Role",
        "Department",
        "Manager",
        "Employment Status",
        "Phone",
        "Joining Date",
        "Resignation Date",
        "Manager Comments"
    ]
    
    for label in expected_labels:
        expect(panel.get_by_text(label, exact=True).first).to_be_visible()
        
    # Verify text area and action buttons
    deny_button = panel.get_by_role("button", name="Deny").first
    approve_button = panel.get_by_role("button", name="Approve").first
    
    # Scroll down to ensure buttons are visible in the viewport
    approve_button.scroll_into_view_if_needed()
    page.wait_for_timeout(500) # Small wait to allow scrolling animation to finish
    
    expect(panel.get_by_placeholder("Write your comments here...").first).to_be_visible()
    expect(deny_button).to_be_visible()
    expect(approve_button).to_be_visible()
    
    # Take a screenshot of the details panel with buttons visible
    _screenshot(page, "test_03_view_row")
    
    # Close the panel (top right close button)
    panel.get_by_role("button", name="Close").first.click()
    page.wait_for_timeout(1000) # Wait for the panel to slide out
