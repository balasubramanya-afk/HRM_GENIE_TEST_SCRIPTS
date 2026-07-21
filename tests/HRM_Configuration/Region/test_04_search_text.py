import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, Playwright, sync_playwright, expect
from config import login_as, _screenshot, navigate_to_region


def reset_filters(page: Page) -> None:
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(500)


def search_text(page: Page, text: str) -> None:
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.click()
    search_input.fill(text)
    page.wait_for_timeout(500)


def test_search_text(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_04_before_search_text")

    # --- 1. Search for existing region "South West" (Match will found) ---
    search_text(page, "South West")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.get_by_role("cell", name="South West").click()
    page.wait_for_timeout(2000)
    _screenshot(page, "test_04_south_west_search")
    reset_filters(page)

    # --- 2. Clear search input via keyboard shortcuts ---
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.click()
    search_input.press("ControlOrMeta+a")
    search_input.fill("")
    page.wait_for_timeout(300)

    # --- 3. Search for "Bala" (No match found) ---
    search_text(page, "Bala")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_04_bala_search")
    reset_filters(page)

    # --- 4. Search for "Warehouse" (1 match found)---
    search_text(page, "Warehouse")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_04_warehouse_search")
    reset_filters(page)
    page.wait_for_timeout(1000)
    

    print("All text search tests completed")

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_search_text(playwright)
