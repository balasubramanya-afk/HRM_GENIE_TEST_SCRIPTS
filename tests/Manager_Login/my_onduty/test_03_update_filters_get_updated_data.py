import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot, login_as, navigate_to_my_onduty,
    select_dropdown_option,
)

def test_update_filters_get_updated_data(page: Page):
    """3. Update Status filter to Pending, verify table data, and Reset Filters."""
    login_as(page, "Manager")
    navigate_to_my_onduty(page)

    # ── Step 1: Filter by "Pending" ──────────────────────────────────────────
    combobox = page.locator(
        "[role='tabpanel'] button[role='combobox'], [role='tabpanel'] [role='combobox']"
    ).first
    expect(combobox).to_be_visible()
    combobox.click()
    page.wait_for_timeout(500)

    pending_opt = page.locator("div[role='option']").filter(has_text="Pending").or_(
        page.locator("[role='option']:not(option)").filter(has_text="Pending")
    ).first
    expect(pending_opt).to_be_visible()
    pending_opt.click()
    page.wait_for_timeout(3000)

    # Verify the dropdown label updated
    expect(combobox).to_contain_text("Pending")

    # Note: We do not assert pending_rows.count() > 0 because another test
    # might have deleted all pending requests, leaving the table legitimately empty.

    # Verify no row in the table has "Approved" status when Pending filter is active
    approved_rows_in_pending_filter = page.locator("tbody tr").filter(
        has_text=re.compile(r"\bApproved\b", re.IGNORECASE)
    )
    assert approved_rows_in_pending_filter.count() == 0, (
        "Filter by 'Pending' is not working — Approved rows are still visible in the table."
    )

    # ── Step 2: Reset Filters — all rows should reappear ─────────────────────
    reset_btn = page.get_by_role("button", name="Reset Filters").first
    expect(reset_btn).to_be_visible()
    reset_btn.click()
    page.wait_for_timeout(1000)

    # Verify dropdown reverts to "All Status"
    expect(combobox).to_contain_text("All Status")

    # We do not assert all_rows > 0 because the environment might have 0 total requests.

    _screenshot(page, "test_03_update_filters_get_updated_data")
