import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_search_nonexisting_leave(page: Page):
    """3. Search for a non-existent leave type."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    page.get_by_role("textbox", name="Search by leave type name...").fill("XYZNonExistent")
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    
    expect(page.get_by_role("cell", name="XYZNonExistent")).not_to_be_visible()
    
    # Verify that a "no records found" message is displayed
    expect(page.get_by_text(re.compile(r"no records found", re.IGNORECASE)).first).to_be_visible()
    
    _screenshot(page, "test_05_search_nonexisting_leave")
