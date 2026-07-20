import re
import time
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_create_policy(page):
    login_and_navigate_to_policies(page, role="HR")
    page.wait_for_timeout(3000)
    page.get_by_role("button", name="Create new Policy").click()
    page.get_by_label("Policy Name *").click()
    unique_policy_name = f"POSH_NEW_{int(time.time())}"
    page.get_by_label("Policy Name *").fill(unique_policy_name)
    page.get_by_placeholder("Enter policy description...").click()
    page.get_by_placeholder("Enter policy description...").fill("Revised version of POSH")
    with page.expect_file_chooser() as fc_info:
        page.locator("label").filter(has_text="Upload attachment").click()
    file_chooser = fc_info.value
    file_chooser.set_files("POSH_NEW.pdf")
    
    # Click preview and wait for the new tab to open
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="Preview (").click()
    page1 = page1_info.value
    
    page.wait_for_timeout(3000)
    # Close the preview tab
    page1.close()
    
    page.get_by_role("button", name="Create").click()
    
    # Save the name to a file so test_05_delete can read it!
    with open("created_policy_name.txt", "w") as f:
        f.write(unique_policy_name)
        
    # Test ends here, policy is created successfully!
    page.wait_for_timeout(3000)
    _screenshot(page, "test_03_create")
 