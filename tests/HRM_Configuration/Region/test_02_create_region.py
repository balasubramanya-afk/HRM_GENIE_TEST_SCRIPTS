import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot, close_toast, navigate_to_region


def test_create_region(playwright: Playwright) -> None:
    slow_mo = os.getenv("PLAYWRIGHT_SLOW_MO")
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo= slow_mo, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_before_create_region")

    # Cancelling the Create region action
    page.get_by_role("main").get_by_role("button", name="Region").click()
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(1000)

    ## Creating region with all values given

    # Clicking the Create region button
    page.get_by_role("main").get_by_role("button", name="Region").click()

    # Selecting the country
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()

    # Entering the region name
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill("South West")
    page.get_by_role("textbox", name="Region *").press("Enter")

    # Selecting the branches
    page.get_by_text("Loading branches...").click()
    page.get_by_role("checkbox", name="Kerala").click()
    page.get_by_role("checkbox", name="Kozhikode -").click()
    page.get_by_role("checkbox", name="Tumkur -").click()

    # Clicking create button
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_create_region")

    # Closing the success pop up
    close_toast(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_create_region(playwright)
