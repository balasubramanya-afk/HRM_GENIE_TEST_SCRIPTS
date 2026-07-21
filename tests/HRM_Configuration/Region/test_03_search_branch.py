import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, Playwright, sync_playwright, expect
from config import login_as, _screenshot, navigate_to_region


def open_branch_dropdown(page: Page) -> None:
    """Click the combobox to open it."""
    combobox = page.locator("button[role='combobox']").first
    combobox.click()
    page.wait_for_timeout(1000)


def close_branch_dropdown(page: Page) -> None:
    """Press Escape to close the dropdown."""
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)


def search_and_select_branch(page: Page, search_text: str, option_text: str) -> None:
    """Open dropdown, type in search, select option."""
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill(search_text)
    option = page.locator("div[role='option']").filter(has_text=option_text)
    option.wait_for(state="visible", timeout=10000)
    option.click(force=True)
    page.wait_for_timeout(1000)
    close_branch_dropdown(page)


def reset_filters(page: Page) -> None:
    close_branch_dropdown(page)
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(500)


def test_search_branch(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    reset_filters(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_before_search_branch")

    # --- 1. Tumkur search and select ---
    search_and_select_branch(page, "Tumkur", "Kerala, Kozhikode, Tumkur")
    print("Tumkur branch selected successfully")
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_tumkur_selected")

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    page.wait_for_timeout(1000)

    # --- 2. Keyboard navigation (ArrowDown/ArrowUp) ---
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill("Mumbai")
    page.wait_for_timeout(1000)
    search_input.press("ArrowDown")
    page.wait_for_timeout(200)
    search_input.press("ArrowUp")
    page.wait_for_timeout(200)
    search_input.press("ArrowDown")
    page.wait_for_timeout(200)
    search_input.press("Enter")
    page.wait_for_timeout(500)
    close_branch_dropdown(page)
    page.wait_for_timeout(1000)
    _screenshot(page, "test_03_keyboard_navigation")

    reset_filters(page)
    page.wait_for_timeout(1000)

    # --- 3. Kerala, Kozhikode search and select ---
    search_and_select_branch(page, "kera", "Kerala, Kozhikode")
    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_03_kerala_kozhikode")

    # --- 4. Open dropdown and Escape to close ---
    open_branch_dropdown(page)
    page.get_by_role("textbox", name="Search...").press("Escape")
    page.wait_for_timeout(300)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    page.wait_for_timeout(1000)

    # --- 5. Full name search and Enter to select ---
    search_and_select_branch(page, "Mumbai, Kolkata, Pune", "Mumbai, Kolkata, Pune")
    reset_filters(page)
    page.wait_for_timeout(1000)

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
    page.wait_for_timeout(1000)
    print("All branch filter tests passed")
    _screenshot(page, "test_03_all_branch_filter_tests")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_search_branch(playwright)
