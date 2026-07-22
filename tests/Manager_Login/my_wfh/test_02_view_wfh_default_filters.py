import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_view_wfh_default_filters(page: Page):
    """2. Verify Manager can view My WFH page with default filters and elements."""
    login_as(page, "Manager")
    page.get_by_role("button").nth(3).click()
    page.get_by_role("button", name="Work From Home").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # Verify heading and tab
    expect(page.get_by_role("heading", name="Work From Home").first).to_be_visible()
    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    expect(my_wfh_tab.first).to_be_visible()
    my_wfh_tab.first.click()

    # Verify "Apply WFH" or "Request WFH" button is visible
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH"))
    expect(apply_wfh_btn.first).to_be_visible()

    # Verify status dropdown / filter combobox
    combobox = page.get_by_role("combobox").first
    expect(combobox).to_be_visible()

    _screenshot(page, "test_02_view_wfh_default_filters")
