import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_global_search(page: Page):
    """4. Test the global search functionality."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("textbox", name="Search anything...").click()
    page.get_by_role("textbox", name="Search anything...").fill("work")
    page.get_by_role("banner").get_by_text("Work From Home").click()
    page.wait_for_timeout(2000)
    
    expect(page).to_have_url(re.compile(r".*/work-from-home"))
    _screenshot(page, "test_04_global_search")
