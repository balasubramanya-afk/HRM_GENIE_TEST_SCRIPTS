import sys
import os
from pathlib import Path
from datetime import datetime
import random

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot, close_toast, navigate_to_region


def test_create_region(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, slow_mo=slow_mo, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_before_create_region")

    # Closing the Create region action
    page.get_by_role("main").get_by_role("button", name="Region").click()
    page.get_by_role("button", name="Close").click()
    _screenshot(page, "test_02_create_region_dialog_closed")
    page.wait_for_timeout(1000)

    # Cancelling the Create region action
    page.get_by_role("main").get_by_role("button", name="Region").click()
    page.get_by_role("button", name="Cancel").click()
    _screenshot(page, "test_02_create_region_dialog_cancelled")
    page.wait_for_timeout(1000)

    ## Creating region with all values given

    # Adding suffix will helps to create the region and check for duplication
    unique_suffix = f"{datetime.now().strftime('%M%S')}_{random.randint(10, 99)}"
    region_name = f"South West {unique_suffix}"

    # Clicking the Create region button
    page.get_by_role("main").get_by_role("button", name="Region").click()

    # Selecting the country
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()

    # Entering the region name
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill(region_name)
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
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Creating duplicate region to verify error message
    page.get_by_role("main").get_by_role("button", name="Region").click()
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill(region_name)
    page.get_by_role("textbox", name="Region *").press("Enter")
    
    # Selecting the branches
    page.get_by_text("Loading branches...").click()
    page.get_by_role("checkbox", name="Kerala").click()
    page.get_by_role("checkbox", name="Kozhikode -").click()
    page.get_by_role("checkbox", name="Tumkur -").click()

    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_duplicate_region_error")
    page.get_by_text("Region name already exists").wait_for(
        state="visible", timeout=5000
    )
    print("Duplicate region error verified")
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(1000)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_create_region(playwright)
