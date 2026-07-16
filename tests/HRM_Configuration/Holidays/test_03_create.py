import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome",headless=False,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.get_by_role("button", name="+ New Holiday").click()
    page.get_by_label("Country *").click()
    page.get_by_label("India").click()
    page.get_by_label("Region*").click()
    page.get_by_label("west", exact=True).click()
    page.get_by_label("Region*").click()
    page.get_by_label("South West").get_by_text("South West").click()
    page.get_by_label("Kerala").click()
    page.get_by_placeholder("e.g. Independence Day").click()
    page.get_by_placeholder("e.g. Independence Day").fill("testing-diwali")
    page.get_by_label("Start Date *").click()
    page.get_by_label("Friday, July 17th,").click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Friday, July 17th, 2026,").click()
    page.get_by_label("Friday, July 17th,").click()
    page.locator("div").filter(has_text=re.compile(r"^Send this update to all employees$")).first.click()
    page.get_by_role("button", name="Create").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
