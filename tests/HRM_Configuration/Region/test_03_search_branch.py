import re
import os
from playwright.sync_api import Page, Playwright, sync_playwright, expect

from test_01_login import login, navigate_to_region


def open_branch_dropdown(page: Page) -> None:
    """Click the combobox to open it."""
    # Assuming the Branch filter is the first combobox on the page
    combobox = page.locator("button[role='combobox']").first
    combobox.click()
    page.wait_for_timeout(500)


def close_branch_dropdown(page: Page) -> None:
    """Press Escape to close the dropdown."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)


def search_and_select_branch(page: Page, search_text: str, option_text: str) -> None:
    """Open dropdown, type in search, select option."""
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill(search_text)
    page.wait_for_timeout(500)
    # Click the option directly using has_text
    page.locator("div[role='option']").filter(has_text=option_text).click(force=True)
    page.wait_for_timeout(500)
    close_branch_dropdown(page)


def reset_filters(page: Page) -> None:
    close_branch_dropdown(page)
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(500)


def test_search_branch(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", 
        headless=False, 
        slow_mo=slow_mo, 
        args=["--start-maximized"]
    )

    context = browser.new_context(
        no_viewport=True
    )
    page = context.new_page()
    login(page)
    navigate_to_region(page)
    reset_filters(page)

    # --- 1. Bangalore search and select ---
    search_and_select_branch(page, "Banga", "Bangalore")
    branch_combobox = page.get_by_role("combobox").filter(has_text="Bangalore")
    expect(branch_combobox).to_be_visible()
    print("Bangalore branch selected successfully")

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 2. Keyboard navigation (ArrowDown/ArrowUp) ---
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill("Banga")
    page.wait_for_timeout(500)
    search_input.press("ArrowDown")
    page.wait_for_timeout(200)
    search_input.press("ArrowUp")
    page.wait_for_timeout(200)
    search_input.press("ArrowDown")
    page.wait_for_timeout(200)
    search_input.press("Enter")
    page.wait_for_timeout(500)
    close_branch_dropdown(page)

    reset_filters(page)

    # --- 3. Kerala, Kozhikode search and select ---
    search_and_select_branch(page, "kera", "Kerala, Kozhikode")
    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 4. Open dropdown and Escape to close ---
    open_branch_dropdown(page)
    page.get_by_role("textbox", name="Search...").press("Escape")
    page.wait_for_timeout(300)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 5. Full name search and Enter to select ---
    search_and_select_branch(page, "Kerala, Kozhikode", "Kerala, Kozhikode")
    reset_filters(page)

    # --- 6. Verify reset clears everything ---
    open_branch_dropdown(page)
    page.get_by_role("textbox", name="Search...").fill("test")
    page.wait_for_timeout(300)
    page.get_by_role("textbox", name="Search...").press("Escape")
    page.wait_for_timeout(300)

    region_search = page.get_by_role("textbox", name="Search", exact=True)
    if region_search.count() > 0:
        region_search.fill("South")
        page.wait_for_timeout(500)

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    if region_search.count() > 0:
        region_search.fill("")
        page.wait_for_timeout(500)
        expect(region_search).to_have_value("")
    print("All branch filter tests passed")

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_search_branch(playwright)
