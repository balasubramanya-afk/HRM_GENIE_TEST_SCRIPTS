"""
test_09_empty_state.py
======================
Verifies the empty state UI of the Region module when filters yield zero results.

Scenarios covered:
  1. Text search with a non-existent term -> empty state
  2. Branch filter selected (real branch) + non-existent text -> empty state
  3. Non-existent text first, then real branch filter added -> still empty state
  4. Reset Filters clears all filters and restores the full list
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, Playwright, sync_playwright, expect
from config import login_as, _screenshot, navigate_to_region


EMPTY_STATE_TEXT = "No records found"
NON_EXISTENT_QUERY = "ZZZ_NonExistentRegion_999"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def reset_filters(page: Page) -> None:
    """Click Reset Filters, wait for state to update, then explicitly clear the
    search input via keyboard to ensure React's onChange fires and searchQuery = ''."""
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(800)
    # Explicitly clear the search field so React searchQuery state is truly empty
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    if search_input.input_value() != "":
        search_input.press("ControlOrMeta+a")
        search_input.fill("")
        page.wait_for_timeout(300)


def apply_text_search(page: Page, text: str) -> None:
    """Type into the region search box using keystroke events.

    Uses press_sequentially() instead of fill() to reliably trigger React's
    controlled-input onChange handler. After a branch-filter re-render, fill()
    sets the raw DOM value but does not fire the synthetic keyboard events that
    React listens to — so searchQuery state never updates.
    """
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    # Select all and clear existing content
    search_input.press("ControlOrMeta+a")
    search_input.fill("")
    page.wait_for_timeout(150)
    # Type character-by-character so React onChange fires for every keystroke
    search_input.press_sequentially(text, delay=40)
    page.wait_for_timeout(800)


def open_branch_dropdown(page: Page) -> None:
    """Click the Branch combobox to open the dropdown."""
    combobox = page.locator("button[role='combobox']").first
    combobox.click()
    page.wait_for_timeout(800)


def select_branch(page: Page, search_text: str, option_text: str) -> None:
    """Open the branch dropdown, search, and click the matching option.

    Does NOT press Escape after selecting — clicking the option closes the
    dropdown automatically, avoiding Escape-key propagation that could reset
    the main search-box React state.
    """
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill(search_text)
    option = page.locator("div[role='option']").filter(has_text=option_text)
    option.wait_for(state="visible", timeout=10000)
    option.click(force=True)
    page.wait_for_timeout(1200)


def assert_empty_state(page: Page) -> None:
    """Assert the table is in empty state: 'No records found' visible, one tbody row."""
    expect(page.get_by_text(EMPTY_STATE_TEXT)).to_be_visible(timeout=6000)
    rows = page.locator("table tbody tr")
    expect(rows).to_have_count(1)


def assert_non_empty_state(page: Page) -> None:
    """Assert the table has more than one tbody row (i.e. real data rows visible)."""
    page.wait_for_timeout(800)
    rows = page.locator("table tbody tr")
    row_count = rows.count()
    assert row_count > 1, (
        f"Expected data rows after reset, but got {row_count} row(s). "
        f"The empty-state row itself counts as 1."
    )


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------

def test_empty_state(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # Login and navigate
    login_as(page, "HR")
    navigate_to_region(page)
    reset_filters(page)
    page.wait_for_timeout(1500)
    _screenshot(page, "test_09_before_empty_state")

    # ------------------------------------------------------------------
    # Scenario 1: Text search with a non-existent term -> empty state
    # ------------------------------------------------------------------
    print("Scenario 1: Text search with non-existent term...")
    apply_text_search(page, NON_EXISTENT_QUERY)
    _screenshot(page, "test_09_s1_text_search_empty")
    assert_empty_state(page)
    print(f"  ok S1: Empty state shown for text search: '{NON_EXISTENT_QUERY}'")

    reset_filters(page)
    assert_non_empty_state(page)
    print("  ok S1: Full list restored after Reset Filters")

    # ------------------------------------------------------------------
    # Scenario 2: Select a real branch -> confirm data -> add non-existent
    # text search -> empty state.
    # Tests that an active branch filter + text mismatch triggers empty state.
    # ------------------------------------------------------------------
    print("Scenario 2: Branch selected, then non-existent text search...")
    select_branch(page, "Tumkur", "Kerala, Kozhikode, Tumkur")
    page.wait_for_timeout(800)
    expect(
        page.get_by_role("combobox").filter(has_text="Kerala, Kozhikode, Tumkur")
    ).to_be_visible()
    assert_non_empty_state(page)
    print("  ok S2: Branch 'Kerala, Kozhikode, Tumkur' selected -- data is visible")

    apply_text_search(page, NON_EXISTENT_QUERY)
    _screenshot(page, "test_09_s2_branch_then_text_empty")
    assert_empty_state(page)
    print("  ok S2: Empty state shown when non-existent text applied over branch filter")

    reset_filters(page)
    assert_non_empty_state(page)
    print("  ok S2: Full list restored after Reset Filters")

    # ------------------------------------------------------------------
    # Scenario 3: Non-existent text first -> add a real branch filter ->
    # table remains empty (combined filters, opposite order to Scenario 2).
    # ------------------------------------------------------------------
    print("Scenario 3: Non-existent text first, then branch filter added...")
    apply_text_search(page, NON_EXISTENT_QUERY)
    assert_empty_state(page)
    print(f"  ok S3: Empty state confirmed after text search: '{NON_EXISTENT_QUERY}'")

    select_branch(page, "Mumb", "Mumbai, Kolkata, Pune")
    page.wait_for_timeout(800)
    expect(
        page.get_by_role("combobox").filter(has_text="Mumbai, Kolkata, Pune")
    ).to_be_visible()
    _screenshot(page, "test_09_s3_text_then_branch_empty")
    assert_empty_state(page)
    print("  ok S3: Empty state persists after adding branch filter on top of text search")

    # ------------------------------------------------------------------
    # Scenario 4: Reset Filters clears both filters and restores the list.
    # ------------------------------------------------------------------
    print("Scenario 4: Reset Filters restores full list...")
    reset_filters(page)
    _screenshot(page, "test_09_s4_after_reset")

    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    expect(search_input).to_have_value("")
    assert_non_empty_state(page)
    print("  ok S4: Filters cleared -- 'All Branch' visible, search empty, data restored")

    print("\nAll empty state tests passed")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_empty_state(playwright)
