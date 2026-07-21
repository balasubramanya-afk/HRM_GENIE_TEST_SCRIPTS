import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_download_announcement(page):
    do_login(page)
    page.wait_for_load_state("networkidle")

    # Click the 3-dot action menu specifically on the "XYZ" card
    # We find the text, climb to the nearest ancestor div that actually contains a button, and click it
    page.get_by_text("XYZ").locator("xpath=ancestor::div[count(.//button) > 0][1]").get_by_role("button").click()
    
    # Expect the download and click download menuitem
    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Download").click()
    download = download_info.value
    
    # Save the download (optional, but good practice to verify)
    # path = download.path()
    
    _screenshot(page, "download_announcement")
    
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
