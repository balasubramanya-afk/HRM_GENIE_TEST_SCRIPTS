import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill("hr@out-strive.com")
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill("HR@dmin06")
    page.get_by_role("button", name="Login").click()
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Holidays").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)