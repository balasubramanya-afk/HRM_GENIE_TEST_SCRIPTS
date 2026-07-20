import os
import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications

def delete_cert(page, cert_file):
    if not os.path.exists(cert_file):
        print(f"File {cert_file} not found. Skipping.")
        return
        
    with open(cert_file, "r") as f:
        cert_name = f.read().strip()
        
    # Find the certification card that contains our specific certification name
    card = page.locator(".rounded-xl.border.bg-card").filter(has_text=cert_name)
    
    if card.count() == 0:
        card = page.locator("div.relative").filter(has_text=cert_name).last
        
    if card.count() == 0:
        print(f"Certification '{cert_name}' not found on the page. It may have already been deleted.")
        return
        
    # Click the meatball menu button
    meatball_btn = card.locator("button[aria-haspopup='menu']")
    meatball_btn.click()
    page.wait_for_timeout(1000)
    
    # Click Delete
    page.get_by_role("menuitem", name="Delete").click()
    page.wait_for_timeout(1000)
    
    # Wait for the confirmation modal to appear
    delete_confirm_btn = page.get_by_role("button", name=re.compile(r"^(Delete|Yes|Confirm)$", re.IGNORECASE))
    
    delete_confirm_btn.click()
    page.wait_for_timeout(2000)
    
    # If the UI doesn't update automatically, reload the page to see the deletion
    page.reload()
    page.wait_for_timeout(3000)
    
    # Verify the certification is no longer on the page
    card_after_delete = page.locator(".rounded-xl.border.bg-card").filter(has_text=cert_name)
    expect(card_after_delete).to_have_count(0)
    print(f"Successfully deleted {cert_name}")

def test_delete_certification(page):
    login_and_navigate_to_certifications(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # 1. Delete the edited one (Lifetime)
    delete_cert(page, "created_certification_lifetime.txt")
    _screenshot(page, "test_05_delete_success_lifetime")
    
    # Reload the page to ensure any lingering modals or toast messages are cleared
    page.reload()
    page.wait_for_timeout(3000)
    
    # 2. Delete the unedited one (Dated)
    delete_cert(page, "created_certification_dated.txt")
    _screenshot(page, "test_05_delete_success_dated")
