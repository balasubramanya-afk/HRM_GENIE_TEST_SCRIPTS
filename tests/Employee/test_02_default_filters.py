import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot

def test_employee_default_filters(page: Page) -> None:
    login_as(page, "HR")
    
    # Navigate to All Employees
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")

    # Filter interactions
    page.get_by_role("button", name="Add New").click()
    page.get_by_role("heading", name="Onboard Employee").get_by_role("link").click()
    
    # Back to All Employees or similar (if the test expects it)
    # The generated script seemed to just click around the filters
    page.get_by_role("textbox", name="Search by Name & ID").click()
    
    page.get_by_role("combobox").filter(has_text="All Designations").click()
    page.get_by_role("textbox", name="Search...").click()
    
    page.locator("button").filter(has_text="All Status").click()
    page.locator("button").filter(has_text="All Status").click()
    
    page.get_by_role("combobox").filter(has_text="All Managers").click()
    page.get_by_role("textbox", name="Search...").click()
    
    page.locator("button").filter(has_text="All Locations").click()
    page.get_by_role("textbox", name="Search...").click()
    
    page.locator("button").filter(has_text="All Departments").click()
    page.get_by_role("textbox", name="Search...").click()
    page.locator("button").filter(has_text="All Departments").click()

    _screenshot(page, "02_employee_filters")
