"""
test_10_education_craete_edit_delete.py
=======================================
Tests the **Education** tab inside an employee's Edit view:

  1. CREATE  – Add a new education entry (QIS College / B.Tech, Apr 12 2022 – May 11 2022)
  2. CREATE2 – Add a second education entry (Govt junior college / Intermediate,
               Jul 14 2020 – May 17 2022)  ← recorded in the codegen session
  3. EDIT    – Update the first entry (QIS College of Engineering / B.Tech in AIML,
               change start date to Apr 13)
  4. DELETE  – Remove the first entry and confirm via the Delete dialog

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
# Fixed education data (exactly as recorded in the codegen session)
# ---------------------------------------------------------------------------
CREATE1 = {
    "school": "QIS College",
    "qualification": "B.Tech",
    # Start: 2022 → April 12
    # End  : 2 months back from current → May 11 (recorded navigation)
}

CREATE2 = {
    "school": "Govt junior college",
    "qualification": "Intermediate",
    # Start: 2020 → July 14
    # End  : 2022 → May 17
}

EDIT = {
    "school": "QIS College of engineering",
    "qualification": "B.Tech in AIML",
    # Start date changed to April 13 (one day forward from original Apr 12)
}


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------
def test_education_create_edit_delete(page: Page) -> None:
    """Education CREATE → CREATE → EDIT → DELETE lifecycle on the top employee."""

    # ── Login ────────────────────────────────────────────────────────────────
    login_as(page, "HR")

    # ── Navigate to All Employees ─────────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Pick the FIRST (top-most) employee row ────────────────────────────────
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

    # ── Enter Edit mode ───────────────────────────────────────────────────────
    page.get_by_role("button", name="Edit").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    # ── Switch to Education tab ───────────────────────────────────────────────
    page.get_by_role("tab", name="Documents").click()
    page.wait_for_timeout(500)
    page.get_by_role("tab", name="Education").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "10_education_tab_opened")
    print("Education tab opened.")

    # =========================================================================
    # 1. CREATE – QIS College / B.Tech  (Apr 12 2022 – May 11 2022)
    # =========================================================================
    print(f"\n── CREATE 1: {CREATE1}")

    # Click the "+" (plus / add) icon inside the Education header
    # Use the div-filter locator with .first to avoid strict-mode violation
    # (the label also matches pencil + trash SVGs)
    page.locator("div").filter(has_text=re.compile(r"^Education$")).get_by_role("img").first.click()
    page.wait_for_timeout(500)

    # School
    page.get_by_placeholder("Enter your school/university").click()
    page.get_by_placeholder("Enter your school/university").fill(CREATE1["school"])

    # Qualification
    page.get_by_placeholder("Enter your qualification").click()
    page.get_by_placeholder("Enter your qualification").fill(CREATE1["qualification"])

    # ── Start Date: 2022, April 12 ────────────────────────────────────────────
    page.get_by_role("button", name="Start Date").click()
    page.wait_for_timeout(500)
    # Click the month-year header to open year-picker
    page.get_by_role("button", name="July 2026").click()
    page.wait_for_timeout(300)
    page.get_by_role("button", name="2022").click()
    page.wait_for_timeout(300)
    # Navigate forward: dblclick counts as 2 clicks, then 1 more = 3 months forward (Jan→Apr)
    page.get_by_label("Go to the Next Month").dblclick()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Tuesday, April 12th,").click()
    page.wait_for_timeout(300)

    # ── End Date: May 11 2022 (navigate back 2 months from current) ───────────
    page.get_by_role("button", name="End Date").click()
    page.wait_for_timeout(500)
    page.get_by_label("Go to the Previous Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Previous Month").click()
    page.wait_for_timeout(200)
    page.get_by_role("dialog").locator("div").nth(2).click()
    page.wait_for_timeout(200)
    page.get_by_label("Monday, May 11th,").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "10_education_created_1")
    print("✅ Education entry 1 created (QIS College / B.Tech).")

    # =========================================================================
    # 2. CREATE 2 – Govt junior college / Intermediate (Jul 14 2020 – May 17 2022)
    # =========================================================================
    print(f"\n── CREATE 2: {CREATE2}")

    # Click the "+" (plus / add) icon – same specific locator as CREATE 1
    page.locator("div").filter(has_text=re.compile(r"^Education$")).get_by_role("img").first.click()
    page.wait_for_timeout(500)

    page.get_by_placeholder("Enter your school/university").click()
    page.get_by_placeholder("Enter your school/university").fill(CREATE2["school"])

    page.get_by_placeholder("Enter your qualification").click()
    page.get_by_placeholder("Enter your qualification").fill(CREATE2["qualification"])

    # ── Start Date: 2020, July 14 ─────────────────────────────────────────────
    page.get_by_role("button", name="Start Date").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="July 2026").click()
    page.wait_for_timeout(300)
    page.get_by_label("Go to the previous 12 years").click()
    page.wait_for_timeout(300)
    page.get_by_role("button", name="2020", exact=True).click()
    page.wait_for_timeout(300)
    # Navigate to July: dblclick(2) + click(1) + dblclick(2) + click(1) = 6 months (Jan→Jul)
    page.get_by_label("Go to the Next Month").dblclick()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").dblclick()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Tuesday, July 14th,").click()
    page.wait_for_timeout(300)

    # ── End Date: 2022, May 17 ────────────────────────────────────────────────
    page.get_by_role("button", name="End Date").click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="July 2026").click()
    page.wait_for_timeout(300)
    page.get_by_role("button", name="2022").click()
    page.wait_for_timeout(300)
    # Navigate forward 4 months (Jan→May)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Go to the Next Month").click()
    page.wait_for_timeout(200)
    page.get_by_label("Tuesday, May 17th,").click()
    page.wait_for_timeout(300)

    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "10_education_created_2")
    print("✅ Education entry 2 created (Govt junior college / Intermediate).")

    # =========================================================================
    # 3. EDIT – Update first entry: QIS College of Engineering / B.Tech in AIML
    #           Change start date from Apr 12 → Apr 13
    # =========================================================================
    print(f"\n── EDIT: {EDIT}")

    # Click the pencil (edit) icon on the first education entry
    page.get_by_label("Education").get_by_role("button").first.click()
    page.wait_for_timeout(1000)

    # School name (edit form placeholder differs from create form)
    school_input = page.get_by_placeholder("Enter school/university name")
    school_input.click()
    school_input.fill(EDIT["school"])

    # Qualification
    qual_input = page.get_by_placeholder("Enter qualification")
    qual_input.click()
    qual_input.fill(EDIT["qualification"])

    # Change start date from Apr 12 → Apr 13.
    # In edit mode the calendar opens at the STORED date (April 2022), so
    # April 13 should be immediately visible – try a short-timeout direct click.
    # Only fall back to full year-picker navigation if the date isn't visible.
    page.get_by_role("button", name=re.compile(r"Apr 12")).click()
    page.wait_for_timeout(800)

    april_13 = page.get_by_label(re.compile(r"April 13"))
    try:
        # Fast path: calendar already at April 2022, click directly
        april_13.first.click(timeout=3000)
    except Exception:
        # Slow path: calendar opened elsewhere (e.g. July 2026) – navigate
        # via year-picker, then advance month-by-month until April 13 is visible
        header_btn = page.get_by_role("button", name=re.compile(
            r"(January|February|March|April|May|June|July|August|September"
            r"|October|November|December)\s+20\d\d"
        ))
        if header_btn.first.is_visible():
            header_btn.first.click()
            page.wait_for_timeout(300)
        # Find 2022 in the year grid
        for _ in range(5):
            if page.get_by_role("button", name="2022").is_visible():
                break
            page.get_by_label("Go to the previous 12 years").click()
            page.wait_for_timeout(300)
        page.get_by_role("button", name="2022").click()
        page.wait_for_timeout(300)
        # Advance month by month until April 13 is visible (max 6 steps)
        for _ in range(6):
            if page.get_by_label(re.compile(r"April 13")).is_visible():
                break
            page.get_by_label("Go to the Next Month").click()
            page.wait_for_timeout(200)
        page.get_by_label(re.compile(r"April 13")).first.click()
    page.wait_for_timeout(300)

    # Save (green check button inside the third child div)
    page.locator("div:nth-child(3) > div > button").first.click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "10_education_edited")
    print("✅ Education entry 1 edited (QIS College of Engineering / B.Tech in AIML).")

    # =========================================================================
    # 4. DELETE – Remove the first education entry
    # =========================================================================
    print("\n── DELETE first education entry")

    # Click the trash (delete) icon – second button in the Education label group
    page.get_by_label("Education").get_by_role("button").nth(1).click()
    page.wait_for_timeout(1000)

    # Confirm deletion in the dialog
    page.get_by_role("button", name="Delete").click()
    page.wait_for_timeout(2000)
    close_toast(page)
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    _screenshot(page, "10_education_deleted")
    print("✅ Education entry deleted.")

    # ── Final verification: confirm the deleted school name is gone ───────────
    deleted_text = page.get_by_text(EDIT["school"])
    expect(deleted_text).to_have_count(0)

    _screenshot(page, "10_education_final_verification")
    print(
        f"\n✅ Education CREATE → EDIT → DELETE lifecycle PASSED "
        f"for employee ID {emp_id}."
    )
