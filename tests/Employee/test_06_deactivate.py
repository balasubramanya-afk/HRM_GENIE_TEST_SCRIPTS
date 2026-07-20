import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot, close_toast


def test_deactivate_dynamic_employee(page: Page) -> None:
    # ── Login ───────────────────────────────────────────────────────────────
    login_as(page, "HR")

    # ── Navigate to All Employees ───────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")
    
    # ── Filter for Active Employees ─────────────────────────────────────────
    # Click on "All Status" filter and select "Active"
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_label("Active", exact=True).get_by_text("Active").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)  # Wait for table to update
    
    # ── Find first Active Employee ──────────────────────────────────────────
    first_row = page.locator("tbody tr").first
    
    # Ensure there's at least one active employee visible
    expect(first_row).to_be_visible(timeout=5000)
    
    # Extract the Employee ID from the first cell
    emp_id = first_row.locator("td").first.inner_text().strip()
    print(f"Dynamically selected Active Employee ID to deactivate: {emp_id}")
    
    # ── Deactivate the Employee ─────────────────────────────────────────────
    # Click the action button inside the first row
    first_row.get_by_role("button").first.click()
    page.wait_for_timeout(1000)
    
    # Click Deactivate from the dropdown menu
    page.get_by_text("Deactivate").click()
    page.wait_for_timeout(1000)
    
    # Click Deactivate in the confirmation modal
    page.get_by_role("button", name="Deactivate").click()
    
    # Wait for success toast to appear and dismiss it
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # ── Verify Deactivation ─────────────────────────────────────────────────
    # Clear the Active filter by clicking "Reset Filters"
    page.get_by_text("Reset Filters").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Search for the specific employee ID
    page.get_by_role("textbox", name="Search by Name & ID").click()
    page.get_by_role("textbox", name="Search by Name & ID").fill(emp_id)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    
    # Verify the status badge says "Deactived"
    search_row = page.locator("tbody tr").first
    expect(search_row).to_contain_text("Deactived")
    
    _screenshot(page, f"06_deactivate_success_{emp_id}")
    print(f"Successfully deactivated employee {emp_id}!")
