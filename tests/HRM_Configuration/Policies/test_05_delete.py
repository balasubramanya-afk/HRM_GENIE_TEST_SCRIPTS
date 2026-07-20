import re
import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_policies

def test_delete_policy(page):
    login_and_navigate_to_policies(page, role="HR")
    
    # Wait for policies to load
    page.wait_for_timeout(3000)
    
    # Read the exact policy name that was created in test_03_Create
    with open("created_policy_name.txt", "r") as f:
        policy_to_delete = f.read().strip()
    
    # 1. Search for it first to make sure it's on the screen
    page.get_by_placeholder("Search what you need").click()
    page.get_by_placeholder("Search what you need").fill(policy_to_delete)
    page.get_by_placeholder("Search what you need").press("Enter")
    page.wait_for_timeout(2000)
    
    # 2. Delete it
    page.get_by_role("button", name="Delete policy").click()
    page.get_by_role("button", name="Delete").click()
    page.wait_for_timeout(2000)
    
    # 3. Search for it again to verify it has been deleted
    page.get_by_placeholder("Search what you need").click()
    page.get_by_placeholder("Search what you need").fill(policy_to_delete)
    page.get_by_placeholder("Search what you need").press("Enter")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_05_delete")
    
    # Clear the search
    page.get_by_placeholder("Search what you need").fill("")
    page.wait_for_timeout(3000)