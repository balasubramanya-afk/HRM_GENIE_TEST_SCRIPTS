import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_view_team_leaves_default_filters(page: Page):
    """2. Verify Manager can view Team Leaves page with default filters and elements."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/team-leaves")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # 1. Verify URL
    expect(page).to_have_url(re.compile(r".*/team-leaves"))

    # 2. Verify search input is present
    search_input = page.get_by_role("textbox", name=re.compile(r"Search by name or ID", re.IGNORECASE)).or_(
        page.get_by_placeholder(re.compile(r"Search by name or ID", re.IGNORECASE))
    ).first
    expect(search_input).to_be_visible()

    # 3. Verify filter dropdowns exist
    filter_comboboxes = page.get_by_role("combobox")
    expect(filter_comboboxes.first).to_be_visible()

    # 4. Verify table container is displayed
    table_or_grid = page.locator("table").or_(page.locator(".table")).or_(page.get_by_role("table")).first
    expect(table_or_grid).to_be_visible()

    _screenshot(page, "test_02_view_team_leaves_default_filters")
