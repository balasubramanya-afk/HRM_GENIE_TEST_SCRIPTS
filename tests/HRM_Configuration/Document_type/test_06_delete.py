import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type, login_and_navigate_to_employee_documents

def test_delete_and_verify_document_type(page):
    # ==========================================
    # PART 1: HR Deletes Document Type
    # ==========================================
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(3000)
    
    # Read the document name modified by the edit script from the text file
    with open("created_document_type.txt", "r") as f:
        doc_name = f.read().strip()
            
    # Search for the document to delete
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(doc_name)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    # Click the delete button (the 2nd button) on that specific row
    page.get_by_role("row", name=doc_name).get_by_role("button").nth(1).click()
    page.wait_for_timeout(1000)
    
    # Confirm the deletion in the popup
    page.get_by_role("button", name="Delete").click()
    page.wait_for_timeout(2000)
    
    _screenshot(page, "test_06_delete")
    
    # ==========================================
    # PART 2: HR Verifies Deletion (No results found)
    # ==========================================
    # Search for it again
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(doc_name)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    # Verify the row is completely gone from the HR view
    expect(page.get_by_role("row", name=doc_name)).not_to_be_visible()
    _screenshot(page, "test_06_delete_hr_verify")
    
    # ==========================================
    # PART 3: Employee Verifies Deletion
    # ==========================================
    login_and_navigate_to_employee_documents(page, role="Employee")
    page.wait_for_timeout(3000)
    
    # Verify the deleted document type is NO LONGER visible to the employee
    expect(page.get_by_text(f"{doc_name}Upload")).not_to_be_visible()
    
    # Forcefully scroll any internal scrollable containers to the absolute bottom
    page.evaluate("""
        const elements = document.querySelectorAll('*');
        for (const el of elements) {
            if (el.scrollHeight > el.clientHeight) {
                el.scrollTop = el.scrollHeight;
            }
        }
    """)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_06_employee_verify_delete")
