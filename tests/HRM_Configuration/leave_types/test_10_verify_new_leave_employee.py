from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_verify_new_leave_employee(page: Page):
    """7. Verify the created leave type appears on the Employee Leave page."""
    login_as(page, "Employee")
    updated_leave_name = "Automation Master Leave Updated"
    
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Apply Leave").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    
    expect(page.get_by_role("option", name=updated_leave_name)).to_be_visible()
    _screenshot(page, "test_09_verify_new_leave_employee")
    
    page.locator("body").click() # Close dropdown
    page.keyboard.press("Escape") # Close modal
