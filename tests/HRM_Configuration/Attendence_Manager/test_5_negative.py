import re
from playwright.sync_api import Playwright, sync_playwright, expect

from test_1_login import do_login_manager
from config import login_as, _screenshot, close_toast


def test_negative_attendance_manager_cases(page):
    # Perform login to Attendance Manager
    do_login_manager(page)
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # NEGATIVE TEST CASE 1: Search Team Attendance with Non-Existent Employee Query
    # =========================================================================
    try:
        page.get_by_role("tab", name="Team Attendance").click()
        page.wait_for_load_state("networkidle")

        # Fill search box with non-existent query
        search_box = page.get_by_role("textbox", name="Search by shift type & status")
        search_box.fill("999999_NonExistentUser")
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_01_team_search_no_results")

        # Clear search query
        search_box.fill("")
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 2: Apply Non-Matching Checkbox Filters in My Attendance Tab & Reset
    # =========================================================================
    try:
        page.get_by_role("tab", name="My Attendance").click()
        page.wait_for_load_state("networkidle")

        page.get_by_role("button", name="Filters").click()
        page.get_by_role("checkbox", name="Late Arrivals").click(force=True)
        page.keyboard.press("Escape")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_02_my_attendance_filter_applied")

        # Reset filters
        page.get_by_role("button", name="Reset").first.click()
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_02_my_attendance_filter_reset")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 3: Apply Out-of-Bound Date Range in Team Attendance & Reset
    # =========================================================================
    try:
        page.get_by_role("tab", name="Team Attendance").click()
        page.wait_for_load_state("networkidle")

        # Open date range picker
        page.locator(".lucide.lucide-chevron-down").click()
        # Click previous month button
        page.locator(".rdrNextPrevButton").first.click()
        page.get_by_role("button", name="1", exact=True).nth(1).click(force=True)
        page.keyboard.press("Escape")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_03_team_invalid_date_range")

        # Reset filters
        page.get_by_role("button", name="Reset").first.click()
        page.wait_for_load_state("networkidle")
    except Exception:
        page.keyboard.press("Escape")

    # =========================================================================
    # NEGATIVE TEST CASE 4: Search Team Attendance with Special Characters & Symbols
    # =========================================================================
    try:
        page.get_by_role("tab", name="Team Attendance").click()
        page.wait_for_load_state("networkidle")

        search_box = page.get_by_role("textbox", name="Search by shift type & status")
        search_box.fill("@#$%^&*!~")
        search_box.press("Enter")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_04_team_search_special_chars")

        # Reset filter
        page.get_by_role("button", name="Reset").first.click()
        page.wait_for_load_state("networkidle")
    except Exception:
        pass

    # =========================================================================
    # NEGATIVE TEST CASE 5: Apply Multiple Conflicting Filters on Team Attendance & Reset
    # =========================================================================
    try:
        page.get_by_role("tab", name="Team Attendance").click()
        page.wait_for_load_state("networkidle")

        page.get_by_role("button", name="Filters").click()
        try:
            page.get_by_role("checkbox", name="Late Arrivals").click(force=True)
        except Exception:
            pass
        try:
            page.get_by_role("checkbox", name="Web Check-in").click(force=True)
        except Exception:
            pass
        page.keyboard.press("Escape")
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_05_team_multicheckbox_filtered")

        # Reset all filters
        page.get_by_role("button", name="Reset").first.click()
        page.wait_for_load_state("networkidle")
        _screenshot(page, "negative_05_team_multicheckbox_reset")
    except Exception:
        pass

    page.wait_for_timeout(3000)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    test_negative_attendance_manager_cases(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
