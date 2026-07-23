from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type

def test_document_type_negative_scenarios(page):
    # ==========================================
    # Pre-requisite: Login and Navigate
    # ==========================================
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(2000)

    # ==========================================
    # Negative Test 1: Fill name, click Cancel, verify not created
    # ==========================================
    page.get_by_role("main").get_by_role("button", name="Document Type").click()
    page.get_by_placeholder("Document Type").fill("Sample_Not_Created")
    page.get_by_role("button", name="Cancel").click()
    
    # Verify the item is not created by searching for it
    page.get_by_placeholder("Search", exact=True).fill("Sample_Not_Created")
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    expect(page.get_by_text("Sample_Not_Created")).not_to_be_visible()
    _screenshot(page, "test_07_negative_1_cancel_create")
    
    # Clear Search
    page.get_by_placeholder("Search", exact=True).fill("")
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 2: Leave empty, click Create, verify validation
    # ==========================================
    page.get_by_role("main").get_by_role("button", name="Document Type").click()
    page.get_by_placeholder("Document Type").fill("")
    page.get_by_role("button", name="Create").click()
    
    # The modal should still be open due to validation
    page.wait_for_timeout(500)
    _screenshot(page, "test_07_negative_2_empty_create")
    
    page.get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 3: Edit existing name, click Cancel, verify not changed
    # ==========================================
    # Click the Edit button (first button in the row)
    page.get_by_role("row", name="PAN CARD").get_by_role("button").first.click()
    page.get_by_placeholder("Document Type").fill("PAN CARD_MODIFIED")
    page.get_by_role("button", name="Cancel").click()
    
    # Search for the modified name to verify it was NOT saved
    page.get_by_placeholder("Search", exact=True).fill("PAN CARD_MODIFIED")
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    expect(page.get_by_text("PAN CARD_MODIFIED")).not_to_be_visible()
    _screenshot(page, "test_07_negative_3_cancel_edit")
    
    # Clear Search
    page.get_by_placeholder("Search", exact=True).fill("")
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 4: Delete item, click Cancel, verify not deleted
    # ==========================================
    # Click the Delete button (second button in the row)
    page.get_by_role("row", name="PAN CARD").get_by_role("button").nth(1).click()
    page.get_by_role("button", name="Cancel").click()
    
    # Search for it again to verify it is not deleted
    page.get_by_placeholder("Search", exact=True).fill("PAN CARD")
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    expect(page.get_by_role("row", name="PAN CARD").first).to_be_visible()
    _screenshot(page, "test_07_negative_4_cancel_delete")
    
    # Final cleanup
    page.get_by_placeholder("Search", exact=True).fill("")
    page.get_by_placeholder("Search", exact=True).press("Enter")
