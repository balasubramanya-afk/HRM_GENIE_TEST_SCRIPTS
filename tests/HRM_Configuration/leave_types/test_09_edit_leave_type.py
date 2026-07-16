import re
from playwright.sync_api import expect, Page
from .config import _screenshot, close_toast, login_as

def test_edit_leave_type(page: Page):
    """6. Edit a leave type."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    leave_name = "Automation Master Leave"
    page.get_by_role("textbox", name="Search by leave type name...").fill(leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)

    page.locator(".text-emerald-500").first.click()
    page.wait_for_timeout(1000) # Wait for React to finish populating the Edit modal
    
    updated_leave_name = f"{leave_name} Updated"
    leave_input = page.get_by_role("textbox", name="Leave *")
    leave_input.click() # Click to ensure focus
    leave_input.fill(updated_leave_name)
    
    page.get_by_role("button", name="Update").click()
    close_toast(page)
    page.wait_for_timeout(2000)

    # Find the updated record
    page.get_by_role("textbox", name="Search by leave type name...").fill(updated_leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    
    expect(page.get_by_role("cell", name=updated_leave_name).first).to_be_visible()
    
    _screenshot(page, "test_09_edit_leave_type")
