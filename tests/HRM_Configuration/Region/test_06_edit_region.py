import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, Playwright, sync_playwright, expect
from config import login_as, _screenshot, close_toast, navigate_to_region


def click_first_edit_button(page: Page) -> None:
    """Clicks the first edit icon/button in the table based on the generated class locator."""
    page.locator(
        ".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#55C7900D\\]\\/5"
    ).first.click()
    page.wait_for_timeout(500)


def test_edit_region(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_06_before_edit_region")

    # --- 1. Edit Region: Change Country to USA ---
    click_first_edit_button(page)
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="USA").click()
    page.get_by_role("button", name="Update").click()
    page.wait_for_timeout(2000)
    print("Change Country to USA")
    _screenshot(page, "test_06_edit_country_to_usa")
    close_toast(page)

    # --- 2. Edit Region: Change Country back to India and update Region Name ---
    click_first_edit_button(page)
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill("South")
    page.get_by_text("Choose Branch(es)").click()
    page.get_by_role("button", name="Update").click()
    page.wait_for_timeout(2000)
    print("Country back to India and update Region Name")
    _screenshot(page, "test_06_edit_country_back_india")
    close_toast(page)

    # --- 3. Edit Region: Update Region Name, add Branch, and assign Region Head ---
    click_first_edit_button(page)
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill("South west")
    page.get_by_role("checkbox", name="Tumkur -").click()
    page.get_by_role("combobox", name="Choose Region Head").click()
    page.get_by_role("option", name="Finance Manager").first.click()
    page.get_by_role("button", name="Update").click()
    page.wait_for_timeout(2000)
    _screenshot(page, "test_06_edit_region_name_branch_head")
    close_toast(page)

    print("All edit region tests passed")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_edit_region(playwright)
