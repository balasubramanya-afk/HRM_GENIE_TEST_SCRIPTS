import re
from playwright.sync_api import expect, Page
from .config import _screenshot, close_toast, login_as

def test_delete_leave_type(page: Page):
    """8. Delete a leave type."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    updated_leave_name = "Automation Master Leave Updated"
    page.get_by_role("textbox", name="Search by leave type name...").fill(updated_leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)

    page.locator(".text-red-500").first.click()
    page.get_by_role("button", name="Delete").click()
    close_toast(page)
    page.wait_for_timeout(2000)
    
    # Verify the record is no longer visible
    page.get_by_role("textbox", name="Search by leave type name...").fill(updated_leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("cell", name=updated_leave_name)).not_to_be_visible()
    
    _screenshot(page, "test_12_delete_leave_type")
