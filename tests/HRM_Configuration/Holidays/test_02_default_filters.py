import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome",headless=False,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.get_by_role("button", name="Holidays").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("All Countries").click()
    page.get_by_role("button", name="-01-2026 to 31-12-2026").click()
    page.get_by_role("button", name="June 2026").click()
    page.get_by_role("dialog").click()
    page.get_by_text("Holidays+ New Holiday").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)