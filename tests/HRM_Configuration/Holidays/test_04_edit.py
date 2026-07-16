import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome",headless=False,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.get_by_role("row", name="India South West Kerala").get_by_role("button").first.click()
    page.get_by_label("Country *").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_label("Region").click()
    page.get_by_label("south-east").get_by_text("south-east").click()
    page.locator("#branch-78").click()
    page.get_by_label("Bangalore").click()
    page.get_by_placeholder("Occasion", exact=True).click()
    page.get_by_placeholder("Occasion", exact=True).click()
    page.get_by_placeholder("Occasion", exact=True).fill("testing-pongal")
    page.get_by_label("Start Date *").click()
    page.get_by_label("Saturday, July 18th,").click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Start Date *").click()
    page.get_by_label("Monday, July 20th,").click()
    page.get_by_label("End Date *").click()
    page.get_by_label("Tuesday, July 21st,").click()
    page.get_by_role("button", name="Update").click()
    page.get_by_label("Notifications (F8)").get_by_role("button").click()
    page.get_by_placeholder("Search by occasion...").click()
    page.get_by_placeholder("Search by occasion...").fill("testing-pongal")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
