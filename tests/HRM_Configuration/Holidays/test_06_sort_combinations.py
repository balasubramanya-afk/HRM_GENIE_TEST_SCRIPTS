import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="chrome",headless=False,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    page.locator("button").filter(has_text="All Countries").click()
    page.get_by_label("Albania").get_by_text("Albania").click()
    page.get_by_role("button", name="Reset Filters").click()
    page.get_by_role("button", name="-01-2026 to 31-12-2026").click()
    page.get_by_label("Saturday, June 20th, 2026,").dblclick()
    page.get_by_label("Monday, July 20th,").dblclick()
    page.get_by_label("Tuesday, July 21st,").click()
    page.get_by_text("Holidays+ New Holiday").click()
    page.get_by_role("button", name="-07-2026 to 16-07-2026").click()
    page.get_by_role("button", name="Today", exact=True).dblclick()
    page.get_by_role("button", name="-07-2026 to 16-07-2026").click()
    page.get_by_role("button", name="Yesterday").click()
    page.get_by_role("button", name="-07-2026 to 15-07-2026").click()
    page.get_by_role("button", name="Last 14 days").click()
    page.get_by_role("button", name="-07-2026 to 16-07-2026").click()
    page.get_by_text("TodayYesterdayLast 7 daysLast").click()
    page.get_by_role("button", name="-06-2026 to 16-07-2026").click()
    page.get_by_role("button", name="This Week").click()
    page.get_by_role("button", name="-07-2026 to 18-07-2026").click()
    page.get_by_role("button", name="Last Week").click()
    page.get_by_role("button", name="-07-2026 to 11-07-2026").click()
    page.get_by_role("button", name="This Month").click()
    page.get_by_role("button", name="-07-2026 to 31-07-2026").click()
    page.get_by_role("button", name="Last Month").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
