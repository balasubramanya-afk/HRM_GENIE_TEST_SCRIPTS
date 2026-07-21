import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_edit_announcement(page):
    do_login(page)
    page.wait_for_load_state("networkidle")

    # Optional: Click to view details and close (from recording)
    page.get_by_text("Bhanu's Birthday").first.click()
    page.get_by_role("button", name="Close").click()
    
    # Click the 3-dot action menu specifically on the "Bhanu's Birthday" card
    # We find the text, climb to the nearest ancestor div that actually contains a button, and click it
    page.get_by_text("Bhanu's Birthday").locator("xpath=ancestor::div[count(.//button) > 0][1]").get_by_role("button").click()
    page.get_by_role("menuitem", name="Edit").click()
    
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("Bhanu's Happy Birthday")
    page.get_by_role("button", name="Update").click()
    _screenshot(page, "edit_announcement")
    
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
