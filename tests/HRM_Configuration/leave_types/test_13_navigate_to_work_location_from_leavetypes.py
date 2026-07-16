import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_navigate_to_work_location_from_leavetypes(page: Page):
    """9. Navigate from Leave Types to Work Location."""
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    page.get_by_role("textbox", name="Search by leave type name...").fill("") # Clear search
    page.get_by_text("Work Location", exact=True).first.click()
    
    expect(page.get_by_role("heading", name="Work Location").first).to_be_visible(timeout=10000)
    _screenshot(page, "test_13_navigate_to_work_location_from_leavetypes")
