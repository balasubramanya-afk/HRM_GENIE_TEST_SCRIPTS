import os
import re
from playwright.sync_api import Page, Playwright, sync_playwright, expect
from test_01_login import login, navigate_to_region


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
        channel="chrome", 
        headless=False, 
        slow_mo=slow_mo, 
        args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login(page)
    navigate_to_region(page)

    # --- 1. Search for existing region "India" ---
    search_text(page, "India")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.get_by_role("cell", name="India North").click()
    reset_filters(page)

    # --- 2. Clear search input via keyboard shortcuts ---
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.click()
    search_input.press("ControlOrMeta+a")
    search_input.fill("")
    page.wait_for_timeout(300)

    # --- 3. Search for "Bala" ---
    search_text(page, "Bala")
    reset_filters(page)

    # --- 4. Search for "Warehouse" ---
    search_text(page, "Warehouse")
    reset_filters(page)

    print("All text search tests completed")

    page.close()

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_search_text(playwright)
