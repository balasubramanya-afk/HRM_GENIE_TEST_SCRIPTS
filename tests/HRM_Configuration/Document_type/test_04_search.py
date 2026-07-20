from playwright.sync_api import expect
import os
from config import _screenshot, login_and_navigate_to_document_type

def test_search_document(page):
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(3000)
    
    # Read the document name created by the create script from the text file
    with open("created_document_type.txt", "r") as f:
        doc_name = f.read().strip()
    # Search for the newly created document
    page.get_by_placeholder("Search", exact=True).click()
    page.get_by_placeholder("Search", exact=True).fill(doc_name)
    page.get_by_placeholder("Search", exact=True).press("Enter")
    page.wait_for_timeout(2000)
    
    _screenshot(page, "test_04_search")



