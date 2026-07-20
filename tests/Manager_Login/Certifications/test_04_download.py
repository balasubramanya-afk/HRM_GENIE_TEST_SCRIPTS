import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications

def test_download_certification(page):
    # Read the created certification name
    cert_file = "created_certification_lifetime.txt"
    if not os.path.exists(cert_file):
        print(f"File {cert_file} not found. Skipping download test.")
        return
        
    with open(cert_file, "r") as f:
        cert_name = f.read().strip()
        
    login_and_navigate_to_certifications(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # Find the certification card that contains our specific certification name
    card = page.locator(".rounded-xl.border.bg-card").filter(has_text=cert_name)
    
    if card.count() == 0:
        card = page.locator("div.relative").filter(has_text=cert_name).last
        
    # Click the meatball menu button
    meatball_btn = card.locator("button[aria-haspopup='menu']")
    meatball_btn.click()
    page.wait_for_timeout(1000)
    
    # Wait for the download to start when clicking Download
    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Download").click()
    
    download = download_info.value
    
    # Remove previous download if it exists
    if os.path.exists("downloaded_certification.pdf"):
        os.remove("downloaded_certification.pdf")
    
    # Save the downloaded file
    download_path = "downloaded_certification.pdf"
    download.save_as(download_path)
    
    assert os.path.exists(download_path), "File was not downloaded successfully"
    print(f"Successfully downloaded: {download_path}")
    
    # Take screenshot of the page after download is initiated
    _screenshot(page, "test_04_download_success")
