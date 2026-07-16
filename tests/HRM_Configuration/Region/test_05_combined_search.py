import os
from playwright.sync_api import Page, Playwright, sync_playwright, expect
from test_01_login import login, navigate_to_region


def open_branch_dropdown(page: Page) -> None:
    combobox = page.locator("button[role='combobox']").first
    combobox.click()
    page.wait_for_timeout(500)


def close_branch_dropdown(page: Page) -> None:
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)


def search_and_select_branch(page: Page, search_text: str, option_text: str) -> None:
    open_branch_dropdown(page)
    search_input = page.get_by_role("textbox", name="Search...")
    search_input.fill(search_text)
    page.wait_for_timeout(500)
    page.locator("div[role='option']").filter(has_text=option_text).click(force=True)
    page.wait_for_timeout(500)
    close_branch_dropdown(page)


def search_text(page: Page, text: str) -> None:
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.click()
    search_input.fill(text)
    page.wait_for_timeout(500)


def reset_filters(page: Page) -> None:
    close_branch_dropdown(page)
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(500)
    search_input = page.get_by_role("textbox", name="Search", exact=True)
    if search_input.count() > 0 and search_input.input_value() != "":
        search_input.press("ControlOrMeta+a")
        search_input.fill("")
        page.wait_for_timeout(300)


def test_combined_search(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login(page)
    navigate_to_region(page)
    reset_filters(page)

    # --- 1. Branch first, then text search ---
    search_and_select_branch(page, "Banga", "Bangalore")
    expect(page.get_by_role("combobox").filter(has_text="Bangalore")).to_be_visible()
    search_text(page, "South")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)
    print("Branch + text search applied")

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 2. Text search first, then branch ---
    search_text(page, "Kerala")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(500)
    search_and_select_branch(page, "kera", "Kerala, Kozhikode")
    expect(
        page.get_by_role("combobox").filter(has_text="Kerala, Kozhikode")
    ).to_be_visible()
    page.wait_for_timeout(1000)
    print("Text + branch search applied")

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 3. Both filters with no matching results ---
    search_and_select_branch(page, "Banga", "Bangalore")
    search_text(page, "Kerala")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)
    print("Non-matching combined filter applied")

    reset_filters(page)
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()

    # --- 4. Reset clears both filters ---
    search_text(page, "South West")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(500)
    search_and_select_branch(page, "Banga", "Bangalore")
    expect(page.get_by_role("combobox").filter(has_text="Bangalore")).to_be_visible()

    reset_filters(page)
    region_search = page.get_by_role("textbox", name="Search", exact=True)
    expect(region_search).to_have_value("")
    expect(page.get_by_role("combobox").filter(has_text="All Branch")).to_be_visible()
    print("Reset cleared both filters")

    # --- 5. Branch select, then clear text, re-search text ---
    search_and_select_branch(page, "kera", "Kerala, Kozhikode")
    expect(
        page.get_by_role("combobox").filter(has_text="Kerala, Kozhikode")
    ).to_be_visible()
    search_text(page, "South West")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)

    search_input = page.get_by_role("textbox", name="Search", exact=True)
    search_input.press("ControlOrMeta+a")
    search_input.fill("")
    page.wait_for_timeout(300)
    search_text(page, "Kerala")
    page.get_by_role("textbox", name="Search", exact=True).press("Enter")
    page.wait_for_timeout(1000)
    print("Branch persisted while text changed")

    reset_filters(page)

    print("All combined search tests completed")

    page.close()
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_combined_search(playwright)
