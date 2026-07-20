import os
import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications

def test_edit_certification(page):
    # Read the created certification name
    cert_file = "created_certification_lifetime.txt"
    if not os.path.exists(cert_file):
        print(f"File {cert_file} not found. Skipping edit test.")
        return
        
    with open(cert_file, "r") as f:
        cert_name = f.read().strip()
        
    login_and_navigate_to_certifications(page, role="Manager")
    page.wait_for_timeout(3000)
    
    # Locate the row with our specific certification name
    # Dump HTML for debugging
    with open("page_html.txt", "w") as f:
        f.write(page.content())
    
    # Find the certification card that contains our specific certification name
    card = page.locator(".rounded-xl.border.bg-card").filter(has_text=cert_name)
    
    if card.count() == 0:
        # Fallback if card class changes
        card = page.locator("div.relative").filter(has_text=cert_name).last
        
    # Click the meatball menu button (usually has aria-haspopup="menu")
    meatball_btn = card.locator("button[aria-haspopup='menu']")
    meatball_btn.click()
    page.wait_for_timeout(1000)
    
    # Click Edit
    page.get_by_role("menuitem", name="Edit").click()
    page.wait_for_timeout(2000)
    
    # Edit the brand
    page.get_by_role("combobox").click()
    page.wait_for_timeout(500)
    options = page.get_by_role("option").all()
    if len(options) > 1:
        # Try to select the second option if available
        options[1].click()
    elif len(options) == 1:
        options[0].click()
    else:
        # Fallback
        page.locator(".p-1 > div").nth(2).click()
    page.wait_for_timeout(500)
    
    # Edit the form: Change to Dated
    page.get_by_role("radio", name="Select date").click()
    page.wait_for_timeout(500)
    
    # Select from date (Using button with calendar icon, or fallback to class/position)
    # The form usually has two buttons with calendar icons for the dates
    date_buttons = page.locator("button").filter(has=page.locator("svg.lucide-calendar"))
    if date_buttons.count() >= 2:
        date_buttons.nth(0).click()
    else:
        # Fallback if svg class differs
        page.locator("button.justify-start").nth(0).click()
    page.wait_for_timeout(500)
    page.locator("table button").nth(5).click() 
    
    # Select to date
    if date_buttons.count() >= 2:
        date_buttons.nth(1).click()
    else:
        page.locator("button.justify-start").nth(1).click()
    page.wait_for_timeout(500)
    # The 'Go to the Next Month' button should still have the same name
    page.get_by_role("button", name="Go to the Next Month").click()
    page.wait_for_timeout(500)
    page.locator("table button").nth(15).click()
    
    # Append to name
    name_field = page.get_by_role("textbox", name=re.compile(r"Certificat(?:e|ion)\s+Name", re.IGNORECASE))
    current_name = name_field.input_value()
    new_name = current_name + " - Edited"
    name_field.fill(new_name)
    
    # Upload new file (using dummy_cert.pdf)
    # The label might just be "Upload attachment"
    page.get_by_label("Upload attachment").set_input_files("dummy_cert.pdf")
    page.wait_for_timeout(1000)
    
    # Submit / Update
    # Usually the button is "Upload", "Submit", or "Update"
    submit_btn = page.get_by_role("button", name=re.compile(r"^(Upload|Update|Submit)$", re.IGNORECASE))
    submit_btn.click()
    
    page.wait_for_timeout(2000)
    
    # Take screenshot of the success page
    _screenshot(page, "test_03_edit_success")
    
    # Save the updated name back to the file so delete test can find it
    with open(cert_file, "w") as f:
        f.write(new_name)
