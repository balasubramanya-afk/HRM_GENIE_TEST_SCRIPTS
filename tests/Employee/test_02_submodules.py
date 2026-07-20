from playwright.sync_api import Playwright, sync_playwright
from test_01_login import login


def test_load_submodules(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login(page)
    page.wait_for_url("**/dashboard**", timeout=15000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/general")
    page.wait_for_timeout(1000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/documents")
    page.wait_for_timeout(1000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/profile")
    page.wait_for_timeout(2000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/education")
    page.wait_for_timeout(2000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/experience")
    page.wait_for_timeout(2000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/promotions")
    page.wait_for_timeout(2000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/team-employee")
    page.wait_for_timeout(2000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/indirect-report")
    page.wait_for_timeout(2000)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_load_submodules(playwright)
