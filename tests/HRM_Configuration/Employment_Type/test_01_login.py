import re
# pyrefly: ignore [missing-import]
from playwright.sync_api import expect
from config import login_as, _screenshot

def do_login(page):
    """Reusable login helper. Not a test itself."""
    login_as(page, "HR")
    page.locator("div:nth-child(9) > .inline-flex").click()
    page.get_by_role("button", name="Employment Type").click()

def test_login(page):
    do_login(page)
    _screenshot(page, "login_success")
    # Wait for 3 seconds to let you see the Policies page before it closes
    page.wait_for_timeout(3000)