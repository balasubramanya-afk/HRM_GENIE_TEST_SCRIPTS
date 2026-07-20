import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type, login_and_navigate_to_employee_documents

def test_edit_and_verify_document_type(page):
    # ==========================================
    # PART 1: HR Edits Document Type
    # ==========================================
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(3000)
    
    # Read the document name created by the previous script from the text file
    with open("created_document_type.txt", "r") as f:
        doc_name = f.read().strip()
            
    # Search for the document to ensure it's on the screen (more robust than going to page 2)
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(doc_name)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    # Click the edit button on that specific row
    page.get_by_role("row", name=doc_name).get_by_role("button").first.click()
    page.wait_for_timeout(1000)
    
    # Generate the new name
    new_doc_name = f"{doc_name}_Edited"
    
    # Change the name and update
    page.get_by_placeholder("Document Type").click()
    page.get_by_placeholder("Document Type").fill(new_doc_name)
    page.get_by_role("button", name="Update").click()
    page.wait_for_timeout(2000)
    
    _screenshot(page, "test_05_edit")
    
    # Save the newly edited name so the next script (e.g., delete) can find it
    with open("created_document_type.txt", "w") as f:
        f.write(new_doc_name)
        
    # ==========================================
    # PART 2: Employee Verifies Edited Document Type
    # ==========================================
    login_and_navigate_to_employee_documents(page, role="Employee")
    page.wait_for_timeout(3000)
    
    # Verify the edited document type is visible to the employee
    element = page.get_by_text(f"{new_doc_name}Upload").first
    expect(element).to_be_visible()
    
    # Scroll the element directly into the middle of the screen
    element.scroll_into_view_if_needed()
    
    # Highlight it with a red border so it's extremely obvious in the screenshot
    element.evaluate("el => el.style.border = '3px solid red'")
    
    page.wait_for_timeout(2000)
    _screenshot(page, "test_05_employee_view_edited")
