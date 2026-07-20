import os
import re

BASE_URL = "https://qa.hrmgenie.outstrive.co/login"

ROLES = {
    "HR": ("hr@out-strive.com", "HR@dmin06"),
}

def login_and_navigate_to_resignation(page, role="HR"):
    page.goto(BASE_URL)
    credentials = ROLES.get(role)
    if not credentials:
        raise ValueError(f"No credentials found for role: {role}")

    email, password = credentials

    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill(email)
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill(password)
    page.get_by_role("button", name="Login").click()
    
    # Navigate to Resignation
    page.locator("div").filter(has_text=re.compile(r"^Resignation$")).get_by_role("button").click()
    page.wait_for_timeout(1000)
    
    # Ensure we are on All Employees / hr-resignation
    all_employees = page.get_by_role("button", name="All Employees")
    if all_employees.count() > 0:
        all_employees.first.click()
    elif page.get_by_text("All Employees", exact=True).count() > 0:
        page.get_by_text("All Employees", exact=True).first.click()
        
    page.wait_for_timeout(2000)

def _screenshot(page, test_name):
    os.makedirs("screenshot", exist_ok=True)
    page.screenshot(path=f"screenshot/{test_name}.png", full_page=True)