import re
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot, load_last_employee

def test_employee_default_filters(page: Page) -> None:
    login_as(page, "HR")
    
    # Navigate to All Employees
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")
    page.get_by_role("textbox", name="Search by Name & ID").click()
    employee_name = load_last_employee()
    page.get_by_role("textbox", name="Search by Name & ID").fill(employee_name)
    page.get_by_role("combobox").filter(has_text="All Designations").click()
    page.get_by_role("textbox", name="Search...").fill("ai de")
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").click()
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_label("Active", exact=True).get_by_text("Active").click()
    page.get_by_role("combobox").filter(has_text="Active").click()
    page.get_by_text("Inactive", exact=True).click()
    page.get_by_role("combobox").filter(has_text="Inactive").click()
    page.get_by_text("Probation", exact=True).click()
    page.get_by_role("combobox").filter(has_text="All Managers").click()
    page.get_by_role("textbox", name="Search...").fill("band")
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").fill("")
    page.locator("button").filter(has_text="All Locations").click()
    page.get_by_role("textbox", name="Search...").fill("goa")
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").fill("")
    page.locator("button").filter(has_text="All Departments").click()
    page.get_by_role("textbox", name="Search...").fill("IT")
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").fill("")
    page.get_by_text("Reset Filters").click()
    page.get_by_role("combobox").filter(has_text="All Designations").click()
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_label("Active", exact=True).get_by_text("Active").click()
    page.get_by_role("button", name="Reset Filters").click()
    _screenshot(page, "04_employee_search_filters")


