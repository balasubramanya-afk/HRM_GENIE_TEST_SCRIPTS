import re
import random
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_search_policies(page):
    login_and_navigate_to_policies(page, role="Manager")
    page.wait_for_timeout(3000)
    page.wait_for_timeout(3000)
    
    # Get all the headings on the page to find available policies
    headings = page.locator("h1, h2, h3, h4, h5, h6").all_inner_texts()
    
    # Filter out static headers like "Policies" and "Company Policy"
    available_policies = [h for h in headings if h not in ("Policies", "Company Policy") and h.strip()]
    
    if available_policies:
        # Dynamically select one random policy name
        random_policy = random.choice(available_policies)
        
        page.get_by_placeholder("Search what you need").click()
        page.get_by_placeholder("Search what you need").fill(random_policy)
        page.get_by_placeholder("Search what you need").press("Enter")
        
        # Wait to let the search results load and verify
        page.wait_for_timeout(2000)
        expect(page.get_by_text(random_policy).first).to_be_visible()
        
    _screenshot(page, "test_02_search")