from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_policies_negative_scenarios(page):
    # ==========================================
    # Pre-requisite: Login and Navigate to Policies
    # ==========================================
    login_and_navigate_to_policies(page, role="HR")
    
    # Give the page a moment to load
    page.wait_for_timeout(2000)

    # ==========================================
    # Negative Test 1: Empty Fields
    # ==========================================
    page.get_by_role("button", name="Create new Policy").click()
    page.get_by_role("button", name="Create").click()
    
    # Take a screenshot to capture the validation error
    page.wait_for_timeout(500)
    _screenshot(page, "test_07_negative_empty_fields")
    
    # Close to reset state
    page.get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 2: Existing Name or Invalid Data
    # ==========================================
    page.get_by_role("button", name="Create new Policy").click()
    page.get_by_label("Policy Name *").fill("Employee Guidelines")
    page.get_by_placeholder("Enter policy description...").fill("dfguyergf")
    
    # Fix for Locator.set_input_files error by using expect_file_chooser
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Upload attachment").click()
    fc_info.value.set_files("POSH_NEW.pdf")
    
    page.get_by_role("button", name="Create").click()
    
    # Take a screenshot to capture the toast error message
    page.wait_for_timeout(500)
    _screenshot(page, "test_07_negative_existing_name")
    
    page.get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 3: Fill Mandatory Fields and Cancel
    # ==========================================
    page.get_by_role("button", name="Create new Policy").click()
    page.get_by_label("Policy Name *").fill("Temp Name")
    page.get_by_placeholder("Enter policy description...").fill("Temp desc")
    
    page.wait_for_timeout(500)
    _screenshot(page, "test_07_negative_cancel_after_filling")
    
    # Close out of the modal to simulate cancel
    page.get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)
    
    # Search for the cancelled policy to confirm it was not created
    page.get_by_placeholder("Search what you need").click()
    page.get_by_placeholder("Search what you need").fill("Temp Name")
    page.get_by_placeholder("Search what you need").press("Enter")
    page.wait_for_timeout(2000)
    
    # Verify the 'Temp Name' policy is NOT visible
    expect(page.get_by_text("Temp Name")).not_to_be_visible()
    
    _screenshot(page, "test_07_negative_cancel_verified")
