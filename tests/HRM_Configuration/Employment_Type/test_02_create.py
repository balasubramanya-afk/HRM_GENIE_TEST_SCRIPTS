import re
# pyrefly: ignore [missing-import]
from playwright.sync_api import expect

from test_01_login import do_login
from config import _screenshot

def test_create_employment_type(page):
    do_login(page)
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Cancel").click()
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("textbox", name="e.g., Full Time").click()
    page.get_by_role("textbox", name="e.g., Full Time").fill("Full Time (Testing by AI team)")
    page.get_by_role("button", name="Add Employment").click()
    _screenshot(page, "create_employment_type")
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
