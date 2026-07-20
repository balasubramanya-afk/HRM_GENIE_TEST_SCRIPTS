import re
import uuid
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications

def helper_create_certification(page, is_lifetime=True):
    # Click Add Certification button
    page.locator("button").filter(has_text="Add Certification").click()
    page.wait_for_timeout(1000)
    
    # Select from combobox
    page.get_by_role("combobox").click()
    options = page.get_by_role("option").all()
    if options:
        options[0].click()
    else:
        # Fallback to the user's specific locator if role="option" fails
        page.locator(".p-1 > div").nth(1).click()

    # Generate unique values
    unique_suffix = str(uuid.uuid4())[:8]
    cert_type = "Lifetime" if is_lifetime else "Dated"
    cert_name = f"Test Cert {cert_type} {unique_suffix}"
    cert_id = f"CERT-{unique_suffix.upper()}"

    # Fill Certificate Name
    page.get_by_role("textbox", name="Certificate name").fill(cert_name)
    
    # Fill Certificate ID
    page.get_by_role("textbox", name="e.g., ID12345X").fill(cert_id)
    
    if is_lifetime:
        # Select Lifetime (often the first radio button, or named "Life time")
        lifetime_label = page.locator("label").filter(has_text=re.compile(r"life\s*time", re.IGNORECASE))
        if lifetime_label.count() > 0:
            lifetime_label.first.click()
        else:
            page.get_by_role("radio").first.click()
        page.wait_for_timeout(500)
    else:
        # Select date
        page.get_by_role("radio", name="Select date").click()
        page.wait_for_timeout(500)
        
        # From Date
        page.get_by_role("button", name="Select from date").click()
        page.wait_for_timeout(500)
        # Click a day in the calendar grid (assuming it's a table of buttons)
        page.locator("table button").nth(10).click() 
        
        # To Date
        page.get_by_role("button", name="Select to date").click()
        page.wait_for_timeout(500)
        # Go to next month
        page.get_by_role("button", name="Go to the Next Month").click()
        page.wait_for_timeout(500)
        page.locator("table button").nth(20).click()
    
    # Upload attachment (Don't click, just use set_input_files directly)
    page.get_by_label("Upload attachment").set_input_files("dummy_cert.pdf")
    page.wait_for_timeout(1000)
    
    # Take screenshot of the filled form
    _screenshot(page, f"test_02_create_form_{cert_type.lower()}")
    
    # Submit / Upload
    page.get_by_role("button", name="Upload").click()
    page.wait_for_timeout(2000)
    
    # Take screenshot of the newly added certification
    _screenshot(page, f"test_02_create_success_{cert_type.lower()}")
    
    # Save the certification name to a file
    if is_lifetime:
        with open("created_certification_lifetime.txt", "w") as f:
            f.write(cert_name)
    else:
        with open("created_certification_dated.txt", "w") as f:
            f.write(cert_name)


def test_create_certifications_both_types(page):
    login_and_navigate_to_certifications(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # Create a certification with Lifetime
    helper_create_certification(page, is_lifetime=True)
    
    # Wait before creating the next one
    page.wait_for_timeout(2000)
    
    # Create a certification with Selected Dates
    helper_create_certification(page, is_lifetime=False)
