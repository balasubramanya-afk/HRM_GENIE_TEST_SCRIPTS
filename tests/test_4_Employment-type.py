import re
import time
from typing import Optional

from playwright.sync_api import expect


def test_Employment_type_flow(logged_in_page, save_step) -> None:
    page = logged_in_page
    print("Prepare to record Employment type flow.")

    # Navigate to dashboard to ensure clean page state
    page.goto("https://qa.hrmgenie.outstrive.co/")
    page.wait_for_load_state("networkidle")
    
    # use a unique employment type name so row selection is deterministic
    emp_name = f"Testing-{int(time.time())}"


    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).click()
    save_step("hrm_configuration_open")
    page.get_by_role("button", name="Employment Type").click()
    save_step("employment_type_selected")
    page.get_by_role("button", name="+ Add Type").click()
    save_step("add_type_dialog_open")
    page.get_by_role("textbox", name="e.g., Full Time").fill(emp_name)
    page.get_by_role("switch").click()
    page.get_by_role("switch").click()
    page.get_by_role("button", name="Add Employment").click()
    save_step("employment_type_submitted")
    if page.locator(".absolute.right-2").count() > 0:
        page.locator(".absolute.right-2").click()
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Cancel").click()
    page.get_by_role("button", name="+ Add Type").click()
    page.get_by_role("button", name="Add Employment").click()
    page.get_by_role("button", name="Close").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # helper: click the action button for a row by text or index
    def click_row_action(text: Optional[str] = None, index: int = 0):
        # If text is provided, prefer row lookup by text (deterministic)
        if text:
            row = page.locator(f'tr:has-text("{text}")').first
            action = row.locator('button[aria-haspopup="menu"]')
            action.wait_for(state="visible", timeout=1000)
            action.click()
            return

        # Otherwise wait for the table to have enough rows, then try the indexed row.
        timeout_ms = 1000
        start = time.time()
        while (time.time() - start) * 1000 < timeout_ms:
            rows_count = page.locator('table tbody tr').count()
            if rows_count > index:
                row = page.locator('table tbody tr').nth(index)
                action = row.locator('button[aria-haspopup="menu"]')
                if action.count() > 0:
                    try:
                        action.wait_for(state="visible", timeout=1000)
                        action.click()
                        return
                    except Exception:
                        # continue waiting/retrying until timeout
                        pass
            page.wait_for_timeout(200)

        # Final fallback: try the last row's action button
        last_row = page.locator('table tbody tr').last
        action = last_row.locator('button[aria-haspopup="menu"]')
        action.wait_for(state="visible", timeout=5000)
        action.click()

    # Open Edit for the row containing the newly added entry
    click_row_action(text=emp_name)
    page.get_by_role("menuitem", name="Edit").wait_for(state="visible", timeout=1000)
    page.get_by_role("menuitem", name="Edit").click()
    save_step("edit_dialog_open_for_new_type")
    page.get_by_role("button", name="Close").click()

    # Re-open and cancel
    click_row_action(text=emp_name)
    page.get_by_role("menuitem", name="Edit").click()
    page.get_by_role("button", name="Cancel").click()

    # Open, toggle switch and update
    click_row_action(text=emp_name)
    page.get_by_role("menuitem", name="Edit").click()
    save_step("edit_dialog_open_before_toggle")
    page.get_by_role("switch").click()
    page.get_by_role("button", name="Update Employment").click()
    save_step("employment_type_updated")
    page.wait_for_timeout(500)
    if page.locator(".absolute.right-2").count() > 0:
        page.locator(".absolute.right-2").click()

    # Edit the second row by index and update text
    click_row_action(index=1)
    page.get_by_role("menuitem", name="Edit").click()
    page.get_by_role("switch").click()
    page.get_by_role("textbox", name="e.g., Full Time").click()
    page.get_by_role("textbox", name="e.g., Full Time").fill("Testing QA Task")
    page.get_by_role("button", name="Update Employment").click()
    page.wait_for_timeout(500)
    if page.locator(".absolute.right-2").count() > 0:
        page.locator(".absolute.right-2").click()

    # Delete the third row (safe flows)
    click_row_action(index=2)
    page.get_by_role("menuitem", name="Delete").click()
    try:
        page.get_by_role("button", name="Close").click()
    except Exception:
        pass
    click_row_action(index=2)
    page.get_by_role("menuitem", name="Delete").click()
    try:
        page.get_by_role("button", name="Cancel").click()
    except Exception:
        pass
    click_row_action(index=2)
    page.get_by_role("menuitem", name="Edit").click()
    page.get_by_role("button", name="Close").click()
    click_row_action(index=2)
    page.get_by_role("menuitem", name="Delete").click()
    page.get_by_role("button", name="Delete").click()
    page.wait_for_timeout(500)
    if page.locator(".absolute.right-2").count() > 0:
        page.locator(".absolute.right-2").click()
