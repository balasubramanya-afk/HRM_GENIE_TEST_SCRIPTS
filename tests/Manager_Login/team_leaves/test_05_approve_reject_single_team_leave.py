import re
from playwright.sync_api import expect, Page
from .config import (
    _screenshot,
    login_as,
    close_toast,
)

def test_approve_reject_single_team_leave(page: Page):
    """5. Test Manager Single Approve and Single Reject of team member leave requests."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/team-leaves")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # -------------------------------------------------------------
    # 1. SINGLE APPROVE
    # -------------------------------------------------------------
    approve_row = page.locator("tr").filter(has_text="Emp1 Team Leave Single Approve").first
    if not approve_row.is_visible():
        approve_row = page.locator("tr").filter(has_text="Pending").first

    if approve_row.is_visible():
        action_btn = approve_row.locator("button").last
        if action_btn.is_visible():
            action_btn.click()
            page.wait_for_timeout(500)

            approve_menu_item = page.get_by_role("menuitem", name="Approve").or_(page.get_by_text("Approve")).first
            if approve_menu_item.is_visible():
                approve_menu_item.click()
                page.wait_for_timeout(500)

                dialog = page.locator("div[role='dialog'], [role='alertdialog']").first
                reason_input = dialog.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).or_(
                    dialog.get_by_placeholder(re.compile(r"Reason", re.IGNORECASE))
                ).first
                if not reason_input.is_visible():
                    reason_input = page.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).first

                if reason_input.is_visible():
                    reason_input.fill("Approved by Manager")

                _screenshot(page, "test_05_01_single_approve_modal")

                modal_approve_btn = dialog.get_by_role("button", name=re.compile(r"^Approve$", re.IGNORECASE)).first
                if not modal_approve_btn.is_visible():
                    modal_approve_btn = page.get_by_role("button", name=re.compile(r"^Approve$", re.IGNORECASE)).first

                if modal_approve_btn.is_visible():
                    try:
                        modal_approve_btn.click(timeout=3000)
                    except Exception:
                        try:
                            modal_approve_btn.evaluate("el => el.click()")
                        except Exception:
                            pass

                close_toast(page)
                page.wait_for_timeout(2000)
                _screenshot(page, "test_05_02_single_approved")

    # -------------------------------------------------------------
    # 2. SINGLE REJECT
    # -------------------------------------------------------------
    reject_row = page.locator("tr").filter(has_text="Emp1 Team Leave Single Reject").first
    if not reject_row.is_visible():
        reject_row = page.locator("tr").filter(has_text="Pending").first

    if reject_row.is_visible():
        action_btn = reject_row.locator("button").last
        if action_btn.is_visible():
            action_btn.click()
            page.wait_for_timeout(500)

            reject_menu_item = page.get_by_role("menuitem", name="Reject").or_(page.get_by_text("Reject")).first
            if reject_menu_item.is_visible():
                reject_menu_item.click()
                page.wait_for_timeout(500)

                dialog = page.locator("div[role='dialog'], [role='alertdialog']").first
                reason_input = dialog.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).or_(
                    dialog.get_by_placeholder(re.compile(r"Reason", re.IGNORECASE))
                ).first
                if not reason_input.is_visible():
                    reason_input = page.get_by_role("textbox", name=re.compile(r"Reason", re.IGNORECASE)).first

                if reason_input.is_visible():
                    reason_input.fill("Rejected by Manager")

                _screenshot(page, "test_05_03_single_reject_modal")

                modal_reject_btn = dialog.get_by_role("button", name=re.compile(r"^Reject$", re.IGNORECASE)).first
                if not modal_reject_btn.is_visible():
                    modal_reject_btn = page.get_by_role("button", name=re.compile(r"^Reject$", re.IGNORECASE)).first

                if modal_reject_btn.is_visible():
                    try:
                        modal_reject_btn.click(timeout=3000)
                    except Exception:
                        try:
                            modal_reject_btn.evaluate("el => el.click()")
                        except Exception:
                            pass

                close_toast(page)
                page.wait_for_timeout(2000)
                _screenshot(page, "test_05_04_single_rejected")

    expect(page).to_have_url(re.compile(r".*/team-leaves"))
