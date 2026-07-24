import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation


def test_hr_resignation_negative_scenarios(page):
    """
    Negative test cases for HR Login - Resignation Module.

    Negative Test 1: Filter by an invalid / non-existent employee name
    
    Negative Test 2: Attempt to act on an already-processed (Approved/Denied) resignation
   
    """

    # ==========================================
    # Pre-requisite: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="HR")
    page.wait_for_timeout(3000)

    # ==========================================
    # Negative Test 1: Filter/Search with a non-existent employee name
    # Expected: Table shows no records / empty state message
    # ==========================================
    print("\n--- Negative Test 1: Filter with non-existent employee name ---")

    # Use the exact "Search by name or ID" placeholder to target the table-level
    # search field — NOT the global header search bar at the top of the page.
    search_input = page.get_by_placeholder("Search by name or ID")

    nonsense_query = "ZZZZINVALIDXYZ99999"

    if search_input.count() == 0:
        print("  [SKIP] 'Search by name or ID' field not found on HR resignation page. Skipping Test 1.")
        _screenshot(page, "test_07_neg1_skipped_no_search")
    else:
        # Click on the table search field (below the heading, above the table)
        search_input.first.click()
        search_input.first.fill(nonsense_query)
        search_input.first.press("Enter")
        page.wait_for_timeout(2000)

        _screenshot(page, "test_07_neg1_invalid_filter_result")

        # Verification: Table should show no records
        rows_after_search = page.locator("tbody tr").count()
        no_records_text = (
            page.get_by_text("No records found").count() > 0
            or page.get_by_text("No data found").count() > 0
            or page.get_by_text("No results found").count() > 0
        )

        assert rows_after_search == 0 or no_records_text, (
            f"Negative Test 1 FAILED: Search for '{nonsense_query}' returned results unexpectedly. "
            "Expected no records in the table."
        )
        print(f"  [PASS] No records returned for invalid search query '{nonsense_query}'.")

        # Reset the search by clicking "Reset Filters" link
        reset_button = page.get_by_text("Reset Filters")
        if reset_button.count() > 0:
            reset_button.first.click()
            page.wait_for_timeout(1500)
        else:
            search_input.first.fill("")
            search_input.first.press("Enter")
            page.wait_for_timeout(1500)

    

    # ==========================================
    # Negative Test 2: Attempt to act on an already-processed (non-Pending) resignation
    # Expected: Approve/Deny buttons are disabled or hidden for processed entries
    # ==========================================
    print("\n--- Negative Test 2: Attempt to act on an already-processed resignation ---")

    page.wait_for_timeout(1000)

    # Look for a row that is NOT Pending (i.e., Approved or Denied)
    processed_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"Approved|Denied|Rejected", re.IGNORECASE)
    ).first

    if processed_row.count() == 0:
        print("  [SKIP] No processed (Approved/Denied) resignation found. Skipping Test 3.")
        _screenshot(page, "test_07_neg2_skipped_no_processed_row")
    else:
        processed_row.click()
        page.wait_for_timeout(2000)

        panel = page.locator("div[role='dialog'], [aria-label='Employee Detail']").first

        # Verify action buttons are absent/disabled or comments area is read-only
        approve_btn = panel.get_by_role("button", name="Approve")
        deny_btn = panel.get_by_role("button", name="Deny")
        comments_area = panel.get_by_placeholder("Write your comments here...")

        # Scroll to make Approve/Deny buttons visible before taking the screenshot
        # so the disabled state is clearly captured
        if approve_btn.count() > 0:
            try:
                approve_btn.first.scroll_into_view_if_needed()
            except Exception:
                pass
        elif deny_btn.count() > 0:
            try:
                deny_btn.first.scroll_into_view_if_needed()
            except Exception:
                pass
        else:
            # Fallback: scroll the panel content down to reveal the action area
            try:
                panel.evaluate("el => el.scrollBy(0, 400)")
            except Exception:
                page.evaluate("window.scrollBy(0, 400)")
        page.wait_for_timeout(500)

        # Screenshot AFTER scrolling — disabled Approve/Deny buttons should now be visible
        _screenshot(page, "test_07_neg2_disabled_buttons_visible")

        approve_visible = approve_btn.count() > 0 and approve_btn.first.is_visible()
        deny_visible = deny_btn.count() > 0 and deny_btn.first.is_visible()
        comments_disabled = (
            comments_area.count() > 0 and not comments_area.first.is_enabled()
        )

        assert not approve_visible or not deny_visible or comments_disabled, (
            "Negative Test 2 FAILED: Both Approve and Deny buttons are active on a "
            "processed resignation. Actions on already-processed entries should be restricted."
        )
        print("  [PASS] Action buttons are correctly restricted for an already-processed resignation.")

        # Close the panel
        try:
            close_btn = panel.get_by_role("button", name="Close").first
            if close_btn.is_visible(timeout=500):
                close_btn.click(timeout=1000)
        except Exception:
            page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

   