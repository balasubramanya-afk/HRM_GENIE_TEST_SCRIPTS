import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_view_policy(page):
    login_and_navigate_to_policies(page, role="HR")
    
    # Wait for the policies to load
    page.wait_for_timeout(3000)
    
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="View policy").first.click()
    page1 = page1_info.value
    
    # Wait a bit to actually see the preview
    page1.wait_for_timeout(3000)
    _screenshot(page1, "test_04_view")
    page1.close()
