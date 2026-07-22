import sys
import os
import re
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, Playwright, sync_playwright, expect
from config import login_as, _screenshot, close_toast, navigate_to_region

def create_region(page: Page, name: str) -> None:
    """Helper to create a single region with standard inputs."""
    page.get_by_role("main").get_by_role("button", name="Region").click()
    page.wait_for_timeout(300)
    
    # Selecting the country
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()
    
    # Entering the region name
    page.get_by_role("textbox", name="Region *").fill(name)
    page.get_by_role("textbox", name="Region *").press("Enter")
    
    # Selecting the branches
    page.get_by_text("Loading branches...").click()
    page.get_by_role("checkbox", name="Kerala").click()
    
    # Clicking create button
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(500)
    close_toast(page)
    page.wait_for_timeout(300)

def delete_pagination_regions(page: Page) -> None:
    """Deletes all regions starting with 'Pagination Region' from the database."""
    print("Searching for remaining 'Pagination Region' entries to delete...")
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.click()
    search_input.press("ControlOrMeta+a")
    search_input.fill("Pagination Region")
    search_input.press("Enter")
    page.wait_for_timeout(1000)
    
    while True:
        row = page.locator("table tbody tr").filter(has_text="Pagination Region").first
        if row.count() > 0 and row.is_visible():
            delete_btn = row.locator("button").last
            if delete_btn.is_visible():
                delete_btn.click()
                page.wait_for_timeout(500)
                page.get_by_role("button", name="Delete").click()
                page.wait_for_timeout(800)
                close_toast(page)
                page.wait_for_timeout(300)
            else:
                break
        else:
            break
            
    # Clear the search filter
    search_input.click()
    search_input.press("ControlOrMeta+a")
    search_input.fill("")
    search_input.press("Enter")
    page.wait_for_timeout(1000)

def select_entries_per_page(page: Page, value: str) -> None:
    """Helper to select entries per page option (e.g. '20', '30') from Radix select dropdown in TableFooter."""
    # Locate the Radix select trigger in the footer (near 'Show' and 'entries')
    footer_container = page.locator("div").filter(has_text=re.compile(r"Show.*entries")).last
    trigger = footer_container.locator("button[role='combobox']")
    if trigger.count() == 0:
        trigger = page.locator("button[role='combobox']").last
    trigger.click()
    page.wait_for_timeout(500)
    
    # Click the option matching `value`
    option = page.get_by_role("option", name=value, exact=True)
    option.click()
    page.wait_for_timeout(1000)

def test_pagination(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    
    # Step 1: Login and navigate
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(2000)
    
    # Step 2: Delete any leftover pagination regions for a fresh start
    delete_pagination_regions(page)
    
    # Step 3: Check current number of entries
    info_locator = page.get_by_text(re.compile(r"Showing \d+ to \d+ of \d+ entries"))
    total_entries = 0
    if info_locator.count() > 0 and info_locator.first.is_visible():
        info_text = info_locator.first.inner_text()
        match = re.search(r"Showing \d+ to \d+ of (\d+) entries", info_text)
        if match:
            total_entries = int(match.group(1))
    else:
        total_entries = page.locator("table tbody tr").count()
        
    print(f"Current total entries: {total_entries}")
    
    # Step 4: Ensure we have at least 21 entries to show 2 pages even at 20 entries per page
    created_regions = []
    MIN_REQUIRED = 21
    if total_entries < MIN_REQUIRED:
        needed = MIN_REQUIRED - total_entries
        print(f"Creating {needed} additional regions to trigger multi-page & page-size pagination...")
        for i in range(needed):
            unique_name = f"Pagination Region {i}_{datetime.now().strftime('%M%S')}_{random.randint(10, 99)}"
            create_region(page, unique_name)
            created_regions.append(unique_name)
            
        # Refresh navigation to reload the list with pagination
        navigate_to_region(page)
        page.wait_for_timeout(2000)
    
    # Check that pagination info shows at least 21 entries
    info_locator = page.get_by_text(re.compile(r"Showing 1 to 10 of \d+ entries"))
    expect(info_locator.first).to_be_visible()
    
    # Scroll the pagination controls into view so they are visible in the screenshot
    info_locator.first.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Verify pagination elements exist and are correct
    _screenshot(page, "test_08_pagination_page_1")
    
    # Check that page 1 is active
    page_1_button = page.locator("nav[role='navigation']").get_by_text("1", exact=True)
    expect(page_1_button).to_have_attribute("aria-current", "page")
    
    # Check that page 2 button is visible
    page_2_button = page.locator("nav[role='navigation']").get_by_text("2", exact=True)
    expect(page_2_button).to_be_visible()
    
    # Step 5: Click page 2 to navigate
    print("Navigating to page 2...")
    page_2_button.click()
    page.wait_for_timeout(2000)
    
    # Check pagination info for page 2
    info_page_2 = page.get_by_text(re.compile(r"Showing 11 to \d+ of \d+ entries"))
    expect(info_page_2.first).to_be_visible()
    
    # Scroll the pagination controls into view so they are visible in the screenshot
    info_page_2.first.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    _screenshot(page, "test_08_pagination_page_2")
    
    # Verify we are on page 2
    expect(page_2_button).to_have_attribute("aria-current", "page")
    
    # Step 6: Click Go to previous page to navigate back
    print("Navigating back to page 1...")
    page.get_by_label("Go to previous page").click()
    page.wait_for_timeout(2000)
    
    # Verify we are back on page 1
    expect(page_1_button).to_have_attribute("aria-current", "page")
    expect(info_locator.first).to_be_visible()
    
    # Step 7: Click Go to next page to navigate forward
    print("Testing 'Go to next page' button...")
    page.get_by_label("Go to next page").click()
    page.wait_for_timeout(2000)
    expect(page_2_button).to_have_attribute("aria-current", "page")
    
    # Step 8: Test entries per page switching (onEntriesPerPageChange)
    print("Testing entries per page selection (onEntriesPerPageChange)...")
    
    # Navigate back to page 1 first
    page_1_button.click()
    page.wait_for_timeout(1500)
    expect(page_1_button).to_have_attribute("aria-current", "page")
    
    # --- Switch to 20 entries per page ---
    print("  Switching to 20 entries per page...")
    select_entries_per_page(page, "20")
    
    info_20 = page.get_by_text(re.compile(r"Showing 1 to 20 of \d+ entries"))
    expect(info_20.first).to_be_visible()
    print("    ✓ Verified 'Showing 1 to 20 of N entries'")
    _screenshot(page, "test_08_pagination_20_per_page")
    
    # Page 2 should still exist since total entries >= 21
    expect(page_2_button).to_be_visible()
    
    # Navigate to page 2 at 20 entries per page to verify page 2 range (e.g. 21 to 21)
    page_2_button.click()
    page.wait_for_timeout(1500)
    info_20_page2 = page.get_by_text(re.compile(r"Showing 21 to \d+ of \d+ entries"))
    expect(info_20_page2.first).to_be_visible()
    print("    ✓ Verified page 2 showing 'Showing 21 to N of N entries' at 20/page")
    
    # Navigate back to page 1
    page_1_button.click()
    page.wait_for_timeout(1500)
    
    # --- Switch back to 10 entries per page ---
    print("  Switching back to 10 entries per page...")
    select_entries_per_page(page, "10")
    
    info_10 = page.get_by_text(re.compile(r"Showing 1 to 10 of \d+ entries"))
    expect(info_10.first).to_be_visible()
    print("    ✓ Reverted to 10 entries per page successfully")
    _screenshot(page, "test_08_pagination_back_to_10")
    
    # Step 9: Clean up created regions
    delete_pagination_regions(page)
    
    print("\nPagination validation (page navigation & entries per page selection) successful! ✓")
    
    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_pagination(playwright)
