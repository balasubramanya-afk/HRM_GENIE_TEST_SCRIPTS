import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_leave_type_page_opens(page: Page):
    """HR setup - navigate to Leave Types."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)
    expect(page.get_by_role("heading", name="Leave Types").first).to_be_visible()
    _screenshot(page, "test_03_leave_type_page_opens")
