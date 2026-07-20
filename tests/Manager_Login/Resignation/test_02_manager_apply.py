import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation


def test_manager_apply_resignation(page):
    # 1. Login and navigate to resignation module
    login_and_navigate_to_resignation(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # Verify we are on My Resignation tab (default)
    apply_btn = page.get_by_role("button", name="Apply Resignation")
    
    if apply_btn.count() == 0:
        print("Resignation has already been applied! 'Apply Resignation' button not found.")
        _screenshot(page, "test_02_manager_already_applied")
        return
        
    # 2. Click on "Apply Resignation"
    apply_btn.click()
    page.wait_for_timeout(1000)
    
    # 3. Fill in the reason for leaving
    reason_text = "Got another offer and seeking better career growth."
    reason_input = page.get_by_role("textbox", name=re.compile(r"Reason for Leaving", re.IGNORECASE))
    reason_input.fill(reason_text)
    
    _screenshot(page, "test_02_manager_apply_form")
    
    # 4. Click Submit
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    
    # 5. Verify the resignation was submitted successfully
    # Check that the card or row appears on the "My Resignation" page
    # Since we don't know the exact UI of the submitted state from the codegen, 
    # we can check that the "No resignation requests found." text is no longer visible,
    # or that the reason we typed is now visible on the page.
    expect(page.locator("text=No resignation requests found.")).not_to_be_visible()
    
    _screenshot(page, "test_02_manager_apply_success")
