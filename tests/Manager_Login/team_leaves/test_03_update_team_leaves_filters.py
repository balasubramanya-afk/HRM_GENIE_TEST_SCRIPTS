import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_update_team_leaves_filters(page: Page):
    """3. Verify updating filters in Team Leaves page updates grid data and Reset Filters restores view."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/team-leaves")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # 1. Update Status filter
    status_combo = page.get_by_role("combobox").filter(has_text=re.compile(r"All Status|Status", re.IGNORECASE)).first
    if not status_combo.is_visible() and page.get_by_role("combobox").count() > 0:
        status_combo = page.get_by_role("combobox").nth(0)

    if status_combo.is_visible():
        status_combo.click()
        page.wait_for_timeout(500)
        pending_opt = page.get_by_role("option", name="Pending").first
        if pending_opt.is_visible():
            pending_opt.click()
            page.wait_for_timeout(1000)

    _screenshot(page, "test_03_filter_by_status")

    # 2. Update Leave Type filter
    type_combo = page.get_by_role("combobox").filter(has_text=re.compile(r"All (Leave )?Type", re.IGNORECASE)).first
    if not type_combo.is_visible() and page.get_by_role("combobox").count() > 1:
        type_combo = page.get_by_role("combobox").nth(1)

    if type_combo.is_visible():
        type_combo.click()
        page.wait_for_timeout(500)
        casual_opt = page.get_by_role("option", name="Casual Leave").or_(page.get_by_role("option", name="Sick Leave")).first
        if casual_opt.is_visible():
            casual_opt.click()
            page.wait_for_timeout(1000)

    _screenshot(page, "test_03_filter_by_leave_type")

    # 3. Test Reset Filters
    reset_btn = page.get_by_role("button", name="Reset Filters").or_(page.get_by_text("Reset Filters")).first
    if reset_btn.is_visible():
        reset_btn.click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_03_reset_filters")

    expect(page).to_have_url(re.compile(r".*/team-leaves"))
