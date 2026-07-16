import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_verify_mandatory_fields(page: Page):
    """4. Verify mandatory field validation during creation."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    page.get_by_role("button", name="+Add Type").click()
    page.get_by_role("button", name="Create").click()
    
    # Expect validation error messages to appear in the modal
    expect(page.get_by_text("Required").first).to_be_visible()
    _screenshot(page, "test_07_verify_mandatory_fields")
