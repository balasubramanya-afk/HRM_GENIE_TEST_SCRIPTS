import re
from playwright.sync_api import expect, Page
from .config import _screenshot, close_toast, login_as

def test_create_leave_type(page: Page):
    """5. Create a leave type successfully."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    leave_name = "Automation Master Leave"
    
    page.get_by_role("button", name="+Add Type").click()
    page.get_by_role("textbox", name="Leave *").fill(leave_name)
    page.get_by_role("combobox", name="Type *").click()
    page.get_by_role("option", name="Paid", exact=True).click()
    page.get_by_role("spinbutton", name="Days *").fill("15")
    page.get_by_role("spinbutton", name="Monthly *").fill("2")
    page.get_by_role("spinbutton", name="Half Year *").fill("7")
    page.get_by_label("Create Leave Type").get_by_text("Carry Forward", exact=True).click()
    page.get_by_role("spinbutton", name="No of leaves that can be Carry Forward *").fill("5")
    page.get_by_role("button", name="Create").click()
    close_toast(page)
    page.wait_for_timeout(2000)

    # Find the created record
    page.get_by_role("textbox", name="Search by leave type name...").fill(leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    
    expect(page.get_by_role("cell", name=leave_name).first).to_be_visible()
    
    _screenshot(page, "test_08_create_leave_type")
