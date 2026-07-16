from playwright.sync_api import Playwright, sync_playwright


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


def run(playwright: Playwright) -> None:
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
    page.locator("div:nth-child(9) > .inline-flex").click()
    page.get_by_role("button", name="Region").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
