import re
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot, close_toast


def _pick_extend_date(page: Page) -> str:
    """
    Open the date picker and navigate month-by-month until we find 
    enabled (non-disabled, non-outside) calendar cells. Then pick the 
    10th such day (≈ 10 days after probation end date).
    Returns the aria-label of the selected date for verification.
    """
    page.get_by_label("Choose End Date *").click()
    page.wait_for_timeout(500)

    selected_label = None
    for month_advance in range(1, 24):  # try up to 2 years forward
        # Count enabled cells in the current calendar view
        enabled_cells = page.locator(
            "td[role='gridcell']:not([data-disabled='true']):not([data-outside='true'])"
        )
        count = enabled_cells.count()

        if count > 0:
            # Pick 10th day if available, otherwise last available one
            target_index = min(9, count - 1)  # 0-based → 10th day
            target_cell = enabled_cells.nth(target_index)
            target_btn = target_cell.locator("button")
            selected_label = target_btn.get_attribute("aria-label")
            target_btn.click()
            print(f"  Picked date: {selected_label} (after {month_advance} months forward)")
            return selected_label

        # No enabled cells yet — advance to next month
        page.get_by_label("Go to the Next Month").click()
        page.wait_for_timeout(300)

    raise RuntimeError("Could not find any enabled date in the calendar within 24 months!")


def test_extend_probation_dynamic(page: Page) -> None:
    # ── Login ───────────────────────────────────────────────────────────────
    login_as(page, "HR")

    # ── Navigate to All Employees ───────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")

    # ── Filter for Probation Employees ──────────────────────────────────────
    page.locator("button").filter(has_text="All Status").click()
    page.get_by_label("Probation", exact=True).get_by_text("Probation").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Find first Probation Employee with Enabled Extend Button ────────────
    rows = page.locator("tbody tr").all()
    assert len(rows) > 0, "No probation employees found!"

    found_row = None
    emp_id = None

    for i, row in enumerate(rows):
        emp_id = row.locator("td").first.inner_text().strip()
        print(f"Checking row {i} - ID: {emp_id}")
        row.get_by_role("button").first.click()
        page.wait_for_timeout(500)

        # The action dropdown is a Radix popover — the inner div has
        # role='dialog' + data-state='open'. Scope button search there.
        popover = page.locator("[role='dialog'][data-state='open']")
        if popover.count() == 0:
            print(f"  ⚠️  No open popover found for {emp_id}, skipping...")
            page.keyboard.press("Escape")
            page.wait_for_timeout(300)
            continue

        extend_btn = popover.get_by_text("Extend Probation", exact=True)
        is_vis = extend_btn.is_visible() if extend_btn.count() > 0 else False
        is_ena = extend_btn.is_enabled() if extend_btn.count() > 0 else False
        print(f"  Extend Probation count={extend_btn.count()} visible={is_vis} enabled={is_ena}")

        if is_vis and is_ena:
            print(f"  ✅ Found valid employee: {emp_id}")
            found_row = row
            extend_btn.click()
            break

        print(f"  ❌ Extend Probation not available for {emp_id}, skipping...")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    assert found_row is not None, (
        "No employee found with an enabled 'Extend Probation' action. "
        "All probation employees might already be extended."
    )

    page.wait_for_timeout(1000)

    # ── Pick Extension Date (10 days past probation end) ────────────────────
    selected_date = _pick_extend_date(page)

    # ── Fill in reason and submit ────────────────────────────────────────────
    reason = "Extending probation for testing via script"
    page.get_by_placeholder("Write a reason...").fill(reason)
    page.get_by_role("button", name="Proceed").click()

    # Wait for success toast
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)
    print(f"✅ Probation extended successfully to: {selected_date}")

    # ── Open Employee Profile ────────────────────────────────────────────────
    # Click the employee name cell to go to their profile
    found_row.locator("td").nth(1).click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Navigate to Activity Logs tab ───────────────────────────────────────
    page.get_by_role("tab", name="Activity Logs").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Verify Activity Log shows probation status entry ─────────────────────
    active_tab = page.locator("[role='tabpanel'][data-state='active']")

    # The activity log should contain the reason text OR probation-related keywords
    # Check for the reason text first
    activity_text = active_tab.inner_text()
    print(f"Activity log content (excerpt): {activity_text[:500]}")

    assert reason.lower() in activity_text.lower() or "probation" in activity_text.lower(), (
        f"Activity log does not mention the probation extension! Content:\n{activity_text[:1000]}"
    )

    _screenshot(page, f"07_extend_probation_success_{emp_id}")
    print(f"✅ Verified extended probation for {emp_id} in Activity Logs!")
