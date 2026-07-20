import re
import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_download_policy(page):
    login_and_navigate_to_policies(page, role="HR")
    
    # Wait for the policies to load
    page.wait_for_timeout(3000)
    
    # Remove previous download if it exists
    if os.path.exists("downloaded_policy.pdf"):
        os.remove("downloaded_policy.pdf")
        
    
    with page.expect_download() as download_info:
        page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.h-10").first.click()
        
    page.wait_for_timeout(3000)
    _screenshot(page, "test_06_download")
    
    download = download_info.value
    
    
    # Save the downloaded file
    download.save_as("downloaded_policy.pdf")
    page.wait_for_timeout(2000)
    
    # Verify the file was actually saved to the computer!
    assert os.path.exists("downloaded_policy.pdf"), "The downloaded policy file was not found!"
