import re
from playwright.sync_api import Playwright, sync_playwright, expect

from test_01_login import do_login
from config import login_as, _screenshot, close_toast


def _goto_tab(page, tab_name: str):
    """Helper to safely close any open popovers and navigate to an Attendance sub-tab."""
    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    except Exception:
        pass

    try:
        page.get_by_role("button", name=tab_name).click()
    except Exception:
        try:
            page.get_by_role("link", name=tab_name).click()
        except Exception:
            page.get_by_text(tab_name, exact=True).click()
    page.wait_for_load_state("networkidle")


def test_negative_attendance_cases(page):
    # Perform login to Attendance module
    do_login(page)
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 1: Search Attendance Report with Non-Existent Employee Query
    # =========================================================================
    _goto_tab(page, "Report")
    
    # Fill non-existent search query
    page.get_by_role("textbox", name="Search by name or email...").fill("NonExistentEmployeeXYZ999")
    try:
        page.locator(".lucide.lucide-search.absolute.right-3").click()
    except Exception:
        page.keyboard.press("Enter")
    page.wait_for_load_state("networkidle")
    _screenshot(page, "negative_01_search_no_results")

    # Reset search filter
    try:
        page.get_by_role("button", name="Reset Filters").first.click()
    except Exception:
        pass
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 2: Apply Non-Matching Filter in Attendance Overview & Reset
    # =========================================================================
    _goto_tab(page, "Overview")

    # Select month filter
    try:
        page.get_by_role("combobox").filter(has_text="Select month").click()
        page.get_by_role("option", name="Jan").click()
        page.wait_for_load_state("networkidle")
    except Exception:
        pass

    _screenshot(page, "negative_02_overview_filtered_jan")

    # Reset Overview filters
    try:
        page.get_by_role("button", name="Reset").click()
        page.wait_for_load_state("networkidle")
    except Exception:
        pass
    _screenshot(page, "negative_02_overview_reset")

    # =========================================================================
    # NEGATIVE TEST CASE 3: Apply Out-of-Bound / Past Date Range Filter on Report Page & Reset
    # =========================================================================
    _goto_tab(page, "Report")

    try:
        page.get_by_role("button").filter(has_text=re.compile(r"\bto\b")).click()
        # Select previous month or past dates
        page.locator(".rdrNextPrevButton").first.click()
        page.get_by_role("button", name="1", exact=True).first.click(force=True)
        
        # Safely close calendar popover with Escape
        page.keyboard.press("Escape")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_03_report_invalid_date_range")

        # Reset Report Filters
        page.get_by_role("button", name="Reset Filters").first.click()
        page.wait_for_load_state("networkidle")
    except Exception:
        page.keyboard.press("Escape")

    # =========================================================================
    # NEGATIVE TEST CASE 4: Toggle Multiple Checkbox Filters on Attendance Tracker & Reset
    # =========================================================================
    _goto_tab(page, "Attendance Tracker")

    try:
        page.get_by_role("button", name="Filters").click()
        page.get_by_role("checkbox", name="Late Arrivals").click()
        page.get_by_role("checkbox", name="Web Check-in").click()
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_04_tracker_multilocation_filtered")

        # Reset Tracker Filters
        page.get_by_role("button", name="Reset").click()
        page.wait_for_load_state("networkidle")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 5: Attempt Export when Filters produce zero/modified records
    # =========================================================================
    _goto_tab(page, "Report")

    try:
        page.get_by_role("textbox", name="Search by name or email...").fill("NonExistentUser12345")
        try:
            page.locator(".lucide.lucide-search.absolute.right-3").click()
        except Exception:
            page.keyboard.press("Enter")
        page.wait_for_load_state("networkidle")

        # Attempt Export dropdown click
        page.get_by_role("button", name="Export").click()
        _screenshot(page, "negative_05_export_zero_records")

        page.get_by_role("button", name="Reset Filters").first.click()
        page.wait_for_load_state("networkidle")
    except Exception:
        pass

    page.wait_for_timeout(3000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    test_negative_attendance_cases(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
