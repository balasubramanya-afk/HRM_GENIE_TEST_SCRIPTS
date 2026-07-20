import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot, close_toast


def test_activate_first_inactive_employee(page: Page) -> None:
    # ── Login ───────────────────────────────────────────────────────────────
    login_as(page, "HR")

    # ── Navigate to All Employees ───────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")

    # ── Filter for Inactive Employees ───────────────────────────────────────
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_text("Inactive", exact=True).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Wait for table to update

    # ── Sort by Employee ID (descending) ────────────────────────────────────
    # Double-click the Employee ID header to sort by newest first.
    # This ensures we pick a valid, recently deactivated employee.
    try:
        emp_id_header = page.locator("th").filter(has_text="Employee ID").first
        emp_id_header.wait_for(state="visible", timeout=5000)
        emp_id_header.click() # Sort Ascending
        page.wait_for_timeout(1000)
        emp_id_header.click() # Sort Descending
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
    except Exception:
        print("Warning: Could not sort by Employee ID – using default table order.")

    # ── Pick the First Inactive Employee ────────────────────────────────────
    first_row = page.locator("tbody tr").first
    expect(first_row).to_be_visible(timeout=5000)

    # Extract the Employee ID from the first cell for logging / verification
    emp_id = first_row.locator("td").first.inner_text().strip()
    print(f"Activating first inactive employee: {emp_id}")

    # ── Activate the Employee ───────────────────────────────────────────────
    # The Inactive view shows an inline "Activate" button per row.
    first_row.get_by_role("button", name="Activate").click()
    page.wait_for_timeout(1000)

    # Wait for the confirmation dialog to be visible before confirming
    page.get_by_role("heading", name="Activate Employee").wait_for(state="visible", timeout=5000)

    # Click the Activate confirm button scoped to the dialog overlay
    dialog = page.locator("[role='dialog']")
    dialog.get_by_role("button", name="Activate").click()
    
    # Wait for the dialog to close, indicating the activation request was successful
    dialog.wait_for(state="hidden", timeout=5000)
    page.wait_for_timeout(500)

    # Dismiss success toast
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Refresh Page as Requested ───────────────────────────────────────────
    print("Refreshing the page to fetch updated lists...")
    page.reload()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)

    # ── Verify Employee is removed from Inactive list ───────────────────────
    # Since we reloaded the page, we must re-apply the Inactive filter
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_text("Inactive", exact=True).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    page.get_by_role("textbox", name="Search by Name & ID").click()
    page.get_by_role("textbox", name="Search by Name & ID").fill(emp_id)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # The table should no longer show the employee (either "No Data Found" or emp_id is missing)
    tbody = page.locator("tbody")
    expect(tbody).not_to_contain_text(emp_id)

    # ── Verify Employee appears in Active list ──────────────────────────────
    # Reset filters so we can search across all statuses
    page.get_by_text("Reset Filters").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Search for the employee we just activated
    page.get_by_role("textbox", name="Search by Name & ID").click()
    page.get_by_role("textbox", name="Search by Name & ID").fill(emp_id)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # The status badge should now show an active state
    search_row = page.locator("tbody tr").first
    expect(search_row).to_contain_text(re.compile(r"Active|Probation|Confirmed"))

    _screenshot(page, f"12_activate_success_{emp_id}")
    print(f"Successfully activated employee {emp_id}!")
