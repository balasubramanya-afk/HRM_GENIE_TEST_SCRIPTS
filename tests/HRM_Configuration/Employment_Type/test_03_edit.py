import re
# pyrefly: ignore [missing-import]
from playwright.sync_api import expect

from test_01_login import do_login
from config import _screenshot

def test_edit_employment_type(page):
    do_login(page)
    page.wait_for_load_state("networkidle")

    # Click the 3-dot action button inside the first data row of the table
    page.get_by_role("row").nth(1).get_by_role("button").click()
    page.get_by_role("menuitem", name="Edit").click()
    
    page.get_by_role("textbox", name="e.g., Full Time").click()
    # I have removed the redundant arrow key presses here and just kept the fill command.
    page.get_by_role("textbox", name="e.g., Full Time").fill("Full time employment")
    page.get_by_role("switch").click()
    page.get_by_role("button", name="Update Employment").click()
    _screenshot(page, "edit_employment_type")
    
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
