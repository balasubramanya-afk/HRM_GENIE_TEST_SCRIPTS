import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_view_my_leaves_default_filters(page: Page):
    """2. Verify Manager can view My Leaves page with default filters and elements."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Verify URL
    expect(page).to_have_url(re.compile(r".*/my-leave"))

    # Verify "Apply Leave" button is visible
    apply_leave_btn = page.get_by_role("button", name="Apply Leave").or_(page.get_by_role("button", name="Apply For Leave"))
    expect(apply_leave_btn.first).to_be_visible()

    # Verify filter dropdowns / controls exist on page
    filter_comboboxes = page.get_by_role("combobox")
    expect(filter_comboboxes.first).to_be_visible()

    # Verify table / list container is displayed
    table_or_list = page.locator("table").or_(page.locator(".table")).or_(page.get_by_role("table"))
    expect(table_or_list.first).to_be_visible()

    _screenshot(page, "test_02_view_my_leaves_default_filters")
