import uuid
import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type, login_and_navigate_to_employee_documents, BASE_URL, ROLES

def test_create_and_verify_document_type(page):
    # ==========================================
    # PART 1: HR Creates Document Type
    # ==========================================
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(3000)
    
    # Generate a unique document type name
    unique_doc_name = f"DocType_{uuid.uuid4().hex[:8]}"
    
    # Click Create Document Type button
    page.get_by_role("main").get_by_role("button", name="Document Type").click()
    page.wait_for_timeout(1000)
    
    # Fill in the name and create
    page.get_by_placeholder("Document Type").click()
    page.get_by_placeholder("Document Type").fill(unique_doc_name)
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_create")
    
    # Search for it to verify creation in HR view
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(unique_doc_name)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_create_verify")
    
    # Save the dynamically created name to a text file for subsequent tests
    with open("created_document_type.txt", "w") as f:
        f.write(unique_doc_name)
    
    
    # ==========================================
    # PART 2: Employee Verifies Document Type
    # ==========================================
    login_and_navigate_to_employee_documents(page, role="Employee")
    page.wait_for_timeout(3000)
    
    # Verify the uniquely created document type is visible to the employee and click on it
    page.get_by_text(f"{unique_doc_name}Upload").first.click()
    
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_employee_view")
