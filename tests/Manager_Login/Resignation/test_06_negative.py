import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation


def test_manager_resignation_negative_scenarios(page):
    """
    Negative test cases for Manager Login - Resignation Module.

    Negative Test 1: Apply resignation without filling the reason (empty reason field)
    Negative Test 2: Search Team Resignation with a non-existent employee name/ID
    Negative Test 3: Try to act on an already-processed (Approved/Denied) resignation
    Negative Test 4: Approve a team resignation without filling in the comments field
    Negative Test 5: Deny a team resignation without filling in the comments field
    """

    # ==========================================
    # Pre-requisite: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="Manager")
    page.wait_for_timeout(3000)

    # ==========================================
    # Negative Test 1: Submit resignation with an empty reason field
    # Expected: Form should NOT submit; validation error or modal stays open
    # ==========================================
    print("\n--- Negative Test 1: Submit resignation with empty reason ---")

    apply_btn = page.get_by_role("button", name="Apply Resignation")

    if apply_btn.count() == 0:
        print("  [SKIP] 'Apply Resignation' button not found — resignation already applied. Skipping Test 1.")
        _screenshot(page, "test_06_neg1_skipped_already_applied")
    else:
        apply_btn.click()
        page.wait_for_timeout(1000)

        # Clear the reason field to ensure it is empty
        reason_input = page.get_by_role(
            "textbox", name=re.compile(r"Reason for Leaving", re.IGNORECASE)
        )
        reason_input.fill("")  # Explicitly empty

        _screenshot(page, "test_06_neg1_empty_reason_before_submit")

        # Attempt to submit without filling in the reason
        page.get_by_role("button", name="Submit").click()
        page.wait_for_timeout(1500)

        _screenshot(page, "test_06_neg1_empty_reason_after_submit")

        # Verification: the form/modal should still be open (not submitted)
        submit_still_visible = page.get_by_role("button", name="Submit").count() > 0
        assert submit_still_visible, (
            "Negative Test 1 FAILED: Form was submitted with an empty reason. "
            "The Submit button should remain visible, indicating the form is still open."
        )
        print("  [PASS] Form correctly blocked submission with an empty reason field.")

        # Close the form to reset state
        try:
            close_btn = page.get_by_role("button", name="Close").first
            if close_btn.is_visible(timeout=1000):
                close_btn.click()
        except Exception:
            page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 2: Search Team Resignation with a non-existent query
    # Expected: "No records found" message is displayed
    # ==========================================
    print("\n--- Negative Test 2: Search with non-existent employee name/ID ---")

    page.get_by_role("button", name="Team Resignation").click()
    page.wait_for_timeout(2000)

    search_input = page.get_by_placeholder("Search by name or ID")
    nonsense_query = "ZZZZINVALIDXYZ99999"

    search_input.click()
    search_input.fill(nonsense_query)
    search_input.press("Enter")
    page.wait_for_timeout(2000)

    _screenshot(page, "test_06_neg2_invalid_search_result")

    # Verification: No records should be found
    rows_after_search = page.locator("tbody tr").count()
    no_records_text = (
        page.get_by_text("No records found").count() > 0
        or page.get_by_text("No data found").count() > 0
        or page.get_by_text("No results found").count() > 0
    )

    assert rows_after_search == 0 or no_records_text, (
        f"Negative Test 2 FAILED: Search for '{nonsense_query}' returned results unexpectedly. "
        "Expected no records."
    )
    print(f"  [PASS] No records returned for invalid search query '{nonsense_query}'.")

    # Reset the search filter
    reset_button = page.get_by_text("Reset Filters")
    if reset_button.count() > 0:
        reset_button.first.click()
        page.wait_for_timeout(1500)
    else:
        search_input.fill("")
        search_input.press("Enter")
        page.wait_for_timeout(1500)

    # ==========================================
    # Negative Test 3: Attempt to act on an already-processed (non-Pending) resignation
    # Expected: Approve/Deny buttons are disabled or hidden for processed entries
    # ==========================================
    print("\n--- Negative Test 3: Attempt to act on an already-processed resignation ---")

    page.wait_for_timeout(1000)

    # Look for a row that is NOT Pending (i.e., Approved or Denied)
    processed_row = page.locator("tbody tr").filter(
        has_text=re.compile(r"Approved|Rejected", re.IGNORECASE)
    ).first

    if processed_row.count() == 0:
        print("  [SKIP] No processed (Approved/Denied) resignation found in Team table. Skipping Test 3.")
        _screenshot(page, "test_06_neg3_skipped_no_processed_row")
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
        _screenshot(page, "test_06_neg3_disabled_buttons_visible")

        approve_visible = approve_btn.count() > 0 and approve_btn.first.is_visible()
        deny_visible = deny_btn.count() > 0 and deny_btn.first.is_visible()
        comments_disabled = (
            comments_area.count() > 0 and not comments_area.first.is_enabled()
        )

        assert not approve_visible or not deny_visible or comments_disabled, (
            "Negative Test 3 FAILED: Both Approve and Deny buttons are active on a "
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

    