from playwright.sync_api import Page, Playwright, sync_playwright
import re

BASE_URL = "https://qa.hrmgenie.outstrive.co/"
def login(page):
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("hr@out-strive.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("HR@dmin06")
    page.get_by_role("button", name="Show password").click()
    page.get_by_role("button", name="Hide password").click()
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")


def navigate_to_region(page: Page) -> None:
    """Navigates to the Region configuration page."""
    page.wait_for_load_state("networkidle")
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).click()
    page.get_by_role("button", name="Region").click()
    page.wait_for_load_state("networkidle")


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
    login(page)
    navigate_to_region(page)

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_login(playwright)
