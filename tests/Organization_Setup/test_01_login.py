from playwright.sync_api import Page, Playwright, sync_playwright
import re
from config import login_as, navigate_to_organization_setup, _screenshot

BASE_URL = "https://qa.hrmgenie.outstrive.co/"



def test_login(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
        args=["--start-maximized"]
    )
    context = browser.new_context(
        no_viewport=True
    )
    page = context.new_page()
    login_as(page,"HR")
    navigate_to_organization_setup(page)
    _screenshot(page, "test_01_login_organization_setup")

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_login(playwright)
