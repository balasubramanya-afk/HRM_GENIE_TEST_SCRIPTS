import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_delete_announcement(page):
    do_login(page)
    page.wait_for_load_state("networkidle")

    # Click the 3-dot action menu specifically on the "Bhanu's Happy Birthday" card
    # We find the text, climb to the nearest ancestor div that actually contains a button, and click it
    page.get_by_text("Bhanu's Happy Birthday").locator("xpath=ancestor::div[count(.//button) > 0][1]").get_by_role("button").click()
    page.get_by_role("menuitem", name="Delete").click()
    page.get_by_role("button", name="Delete").click()
    _screenshot(page, "delete_announcement")
    
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
