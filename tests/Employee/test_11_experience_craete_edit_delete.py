"""
test_11_experience_craete_edit_delete.py
=========================================
Tests the **Experience** tab inside an employee's Edit view:

  1. CREATE  – Add a new experience entry (Manipal / AI Engineer,
               Jan 07 2025 – May 11 2025)
  2. EDIT    – Update the entry (Manipal Hospital / AI Engineer Role,
               change start date to Jan 08)
  3. DELETE  – Remove the entry and confirm via the Delete dialog

The test always picks the **top-most (first) row** from the All Employees table so
it targets the most recently created employee without any randomness.

Single login, single session – follows the project's existing pattern.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot, close_toast


# ---------------------------------------------------------------------------
# Fixed experience data (based on the recorded codegen session)
# ---------------------------------------------------------------------------
CREATE1 = {
    "organization": "Manipal",
    "work_type": "AI Engineer",
    # Start: Jan 07 2025
    # End  : May 11 2025
}


EDIT = {
    "organization": "Manipal Hospital",
    "work_type": "AI Engineer Role",
    # Start date changed to Jan 08 (one day forward from original Jan 07)
}


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------
def test_experience_create_edit_delete(page: Page) -> None:
    """Experience CREATE -> EDIT -> DELETE lifecycle on the top employee."""

    # -- Login ----------------------------------------------------------------
    login_as(page, "HR")

    # -- Navigate to All Employees --------------------------------------------
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # -- Pick the FIRST (top-most) employee row --------------------------------
    rows = page.locator("tbody tr")
    assert rows.count() > 0, "No employees found in the table"

    first_row = rows.first
    emp_id = first_row.locator("td").first.inner_text().strip()
    print(f"Top employee row selected: ID = {emp_id}")

    # Click the view/eye action icon on that row
    first_row.locator(
        ".inline-flex.items-center.justify-center.whitespace-nowrap"
        ".text-sm.font-medium.transition-colors"
        ".focus-visible\\:outline-none.focus-visible\\:ring-1"
        ".focus-visible\\:ring-ring"
        ".disabled\\:pointer-events-none.disabled\\:opacity-50"
        ".\\[\\&_svg\\]\\:pointer-events-none"
        ".\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0"
        ".hover\\:bg-accent.hover\\:text-accent-foreground"
        ".px-4.py-2.w-max"
    ).first.click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # -- Enter Edit mode -------------------------------------------------------
    page.get_by_role("button", name="Edit").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # -- Switch to Experience tab ----------------------------------------------
    page.get_by_role("tab", name="Documents").click()
    page.wait_for_timeout(500)
    page.get_by_role("tab", name="Education").click()
    page.wait_for_timeout(300)
    page.get_by_role("tab", name="Experience").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "11_experience_tab_opened")
    print("Experience tab opened.")

    # =========================================================================
    # 1. CREATE -- Manipal / AI Engineer  (Jan 07 2025 - May 11 2025)
    # =========================================================================
    print(f"\n-- CREATE 1: {CREATE1}")

    # Click the "+" (plus / add) icon inside the Experience header
    page.get_by_label("Experience").get_by_role("img").click()
    page.wait_for_timeout(500)

    # Organization name
    page.get_by_placeholder("Enter organization name").click()
    page.get_by_placeholder("Enter organization name").fill(CREATE1["organization"])

    # Work type
    page.get_by_placeholder("Enter work type").click()
    page.get_by_placeholder("Enter work type").fill(CREATE1["work_type"])

    # -- Start Date: Jan 07 2025 ----------------------------------------------
    page.get_by_role("button", name="Start Date").click()
    page.wait_for_timeout(500)
    # Click the month-year header to open year-picker
    page.get_by_role("button", name="July 2026").click()
    page.wait_for_timeout(300)
    page.get_by_role("button", name="2025").click()
    page.wait_for_timeout(300)
    # Calendar opens at Jan 2025 - click Jan 07 directly
    page.get_by_label("Tuesday, January 7th,").click()
    page.wait_for_timeout(300)

    # -- End Date: May 11 2025 ------------------------------------------------
    page.get_by_role("button", name="End Date").click()
    page.wait_for_timeout(500)
    # Navigate back 2 months (Jul -> May)
    page.get_by_label("Go to the Previous Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Previous Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Monday, May 11th,").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "11_experience_created_1")
    print("✅ Experience entry 1 created (Manipal / AI Engineer).")

    # =========================================================================
    # 2. EDIT -- Update entry: Manipal Hospital / AI Engineer Role
    #            Change start date from Jan 07 -> Jan 08
    # =========================================================================
    print(f"\n-- EDIT: {EDIT}")

    # Click the pencil (edit) icon on the first experience entry
    page.get_by_label("Experience").get_by_role("button").first.click()
    page.wait_for_timeout(1000)

    # Organization name (edit form)
    org_input = page.get_by_role("textbox", name="Enter organization name")
    org_input.click()
    org_input.fill(EDIT["organization"])

    # Work type
    work_input = page.get_by_role("textbox", name="Enter work type")
    work_input.click()
    work_input.fill(EDIT["work_type"])

    # Change start date from Jan 07 -> Jan 08.
    # In edit mode the calendar opens at the stored date (Jan 2025), so
    # Jan 08 should be immediately visible.
    page.get_by_role("button", name=re.compile(r"Jan 07")).click()
    page.wait_for_timeout(800)

    jan_08 = page.get_by_label(re.compile(r"January 8"))
    try:
        # Fast path: calendar already at Jan 2025, click directly
        jan_08.first.click(timeout=3000)
    except Exception:
        # Slow path: navigate via year-picker
        header_btn = page.get_by_role("button", name=re.compile(
            r"(January|February|March|April|May|June|July|August|September"
            r"|October|November|December)\s+20\d\d"
        ))
        if header_btn.first.is_visible():
            header_btn.first.click()
            page.wait_for_timeout(300)
        for _ in range(5):
            if page.get_by_role("button", name="2025").is_visible():
                break
            page.get_by_label("Go to the previous 12 years").click()
            page.wait_for_timeout(300)
        page.get_by_role("button", name="2025").click()
        page.wait_for_timeout(300)
        page.get_by_label(re.compile(r"January 8")).first.click()
    page.wait_for_timeout(300)

    # Save -- click the first button in the Experience group (green check)
    page.get_by_label("Experience").get_by_role("button").first.click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "11_experience_edited")
    print("✅ Experience entry 1 edited (Manipal Hospital / AI Engineer Role).")

    # =========================================================================
    # 4. DELETE -- Remove the first experience entry
    # =========================================================================
    print("\n-- DELETE first experience entry")

    # Click the trash (delete) icon -- second button in the Experience label group
    page.get_by_label("Experience").get_by_role("button").nth(1).click()
    page.wait_for_timeout(1000)

    # Confirm deletion in the dialog
    page.get_by_role("button", name="Delete").click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "11_experience_deleted")
    print("✅ Experience entry deleted.")

    # -- Final verification: confirm the deleted organization name is gone -----
    deleted_text = page.get_by_text(EDIT["organization"])
    expect(deleted_text).to_have_count(0)

    _screenshot(page, "11_experience_final_verification")
    print(
        f"\n✅ Experience CREATE -> EDIT -> DELETE lifecycle PASSED "
        f"for employee ID {emp_id}."
    )
