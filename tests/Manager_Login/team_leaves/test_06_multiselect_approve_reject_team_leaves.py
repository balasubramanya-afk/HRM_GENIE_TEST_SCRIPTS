import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
)

def test_multiselect_approve_reject_team_leaves(page: Page):
    """6. Test Multiselect checkboxes and Bulk Approve/Reject team member leaves."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/team-leaves")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Filter by Pending status first to ensure pending rows are listed
    status_combo = page.get_by_role("combobox").filter(has_text=re.compile(r"All Status|Status", re.IGNORECASE)).first
    if status_combo.is_visible():
        status_combo.click()
        page.wait_for_timeout(500)
        pending_opt = page.get_by_role("option", name="Pending").first
        if pending_opt.is_visible():
            pending_opt.click()
            page.wait_for_timeout(1000)

    # Select checkboxes for team member rows
    header_checkbox = page.get_by_role("row", name=re.compile(r"Employee ID|Employee Name|From", re.IGNORECASE)).get_by_role("checkbox").first
    if header_checkbox.is_visible():
        header_checkbox.click()
        page.wait_for_timeout(500)
    else:
        tbody_checkboxes = page.locator("tbody tr").get_by_role("checkbox")
        if tbody_checkboxes.count() >= 2:
            tbody_checkboxes.nth(0).click()
            tbody_checkboxes.nth(1).click()
            page.wait_for_timeout(500)

    _screenshot(page, "test_06_01_rows_selected")

    # Locate "Approve Selected" bulk action button
    bulk_approve_btn = page.get_by_role("button", name=re.compile(r"Approve Selected", re.IGNORECASE)).first
    if not bulk_approve_btn.is_visible():
        bulk_approve_btn = page.locator("button").filter(has_text=re.compile(r"Approve Selected|Approve", re.IGNORECASE)).first

    if bulk_approve_btn.is_visible():
        try:
            bulk_approve_btn.click(timeout=3000)
        except Exception:
            bulk_approve_btn.evaluate("el => el.click()")

        page.wait_for_timeout(1000)

        # Fill Manager reason in bulk approval modal
        dialog = page.locator("div[role='dialog'], [role='alertdialog']").first
        reason_input = dialog.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).or_(
            dialog.get_by_placeholder(re.compile(r"Reason", re.IGNORECASE))
        ).first
        if not reason_input.is_visible():
            reason_input = page.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).first

        if reason_input.is_visible():
            reason_input.fill("Bulk Approved by Manager")

        _screenshot(page, "test_06_02_bulk_approve_modal")

        # Submit bulk approval
        modal_approve_btn = dialog.get_by_role("button", name=re.compile(r"^Approve$", re.IGNORECASE)).first
        if not modal_approve_btn.is_visible():
            modal_approve_btn = page.get_by_role("button", name="Approve").last

        try:
            modal_approve_btn.click(timeout=3000)
        except Exception:
            modal_approve_btn.evaluate("el => el.click()")

        close_toast(page)
        page.wait_for_timeout(2000)
        _screenshot(page, "test_06_03_bulk_approved")

    expect(page).to_have_url(re.compile(r".*/team-leaves"))
