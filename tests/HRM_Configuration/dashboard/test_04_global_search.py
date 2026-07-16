import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_global_search(page: Page):
    """4. Test the global search functionality."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("textbox", name="Search anything...").click()
    page.get_by_role("textbox", name="Search anything...").fill("all employees")
    page.get_by_text("All Employees").first.click()
    page.wait_for_timeout(2000)
    
    _screenshot(page, "test_04_global_search")
