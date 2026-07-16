import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_verify_sandwich_disabled(page: Page):
    """3a. Verify sandwich leave policy is disabled for Paid Leave."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    # Verify the global Sandwich Leave Policy toggle is off
    toggle = page.locator("#sandwich-policy")
    # Using explicit attribute check which is more resilient for custom toggle components
    expect(toggle).to_have_attribute("aria-checked", "false")
    _screenshot(page, "test_06_verify_sandwich_disabled")
