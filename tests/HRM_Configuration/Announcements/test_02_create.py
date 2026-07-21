import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_create_announcement(page):
    do_login(page)
    page.get_by_role("button", name="Add announcement").click()
    page.get_by_role("textbox", name="Title *").click()
    page.get_by_role("textbox", name="Title *").fill("Bhanu's Birthday")
    page.get_by_role("button", name="Select date").click()
    page.get_by_role("button", name="Friday, July 31st,").click()
    page.get_by_role("button", name="Select date").click()
    page.get_by_role("button", name="Friday, July 31st,").click()
    page.get_by_role("button", name="Select reminder date").click()
    page.get_by_role("button", name="Friday, July 31st,").click()
    # Click the Title input field to safely close the date picker popover without closing the whole drawer
    page.get_by_role("textbox", name="Title *").click()

    # Select location - click dropdown, then force-click the checkbox (it has pointer-events:none)
    page.locator("div").filter(has_text="Select locations").nth(4).click()
    page.get_by_label("VIJAYAWADA").click(force=True)
    # Click outside the dropdown to close it
    page.get_by_role("textbox", name="Title *").click()

    # Select department - click dropdown, then force-click the checkbox
    page.locator("div").filter(has_text="Select departments").nth(4).click()
    page.get_by_label("Testing").click(force=True)
    # Click outside the dropdown to close it
    page.get_by_role("textbox", name="Title *").click()

    page.get_by_role("textbox", name="Description*").click()
    page.get_by_role("textbox", name="Description*").fill("Please join us for birthday party for Bhanu")
    page.get_by_role("button", name="Create").click()
    _screenshot(page, "create_announcement")

    # Verify the announcement was actually created
    expect(page.get_by_text("Bhanu's Birthday")).to_be_visible(timeout=5000)
    
    # Wait for a moment to let you see the result before it closes
    page.wait_for_timeout(3000)
