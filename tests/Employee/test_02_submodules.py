import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot, close_toast


def test_load_submodules(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login_as(page, "BUH")
    page.wait_for_url("**/dashboard**", timeout=15000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/general")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_general_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/documents")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_documents_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/profile")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_profile_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/education")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_education_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/experience")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_experience_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/promotions")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_promotions_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/team-employee")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_team_employee_module")

    page.goto("https://qa.hrmgenie.outstrive.co/employee/indirect-report")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_02_employee_indirect_report_module")

    close_toast(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_load_submodules(playwright)
