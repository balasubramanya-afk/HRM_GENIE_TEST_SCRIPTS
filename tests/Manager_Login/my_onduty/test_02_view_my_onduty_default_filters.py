import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, navigate_to_my_onduty

def test_view_my_onduty_default_filters(page: Page):
    """2. Verify Manager can view My On Duty page with default filters and elements."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # Verify heading and tab
    expect(page.get_by_role("heading", name="On Duty").first).to_be_visible()
    my_onduty_tab = page.get_by_role("tab", name="My On Duty")
    expect(my_onduty_tab).to_be_visible()

    # Verify "Apply On Duty" button is visible
    apply_btn = page.get_by_role("button", name="Apply On Duty").or_(page.get_by_role("button", name="Request On Duty")).first
    expect(apply_btn).to_be_visible()

    # Verify status dropdown / combobox exist
    filter_combobox = page.get_by_role("tabpanel", name="My On Duty").get_by_role("combobox").or_(page.get_by_role("combobox")).first
    expect(filter_combobox).to_be_visible()

    _screenshot(page, "test_02_view_my_onduty_default_filters")

