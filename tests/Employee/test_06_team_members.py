import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, _screenshot, close_toast


def test_team_members(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login_as(page, "BUH")
    page.wait_for_timeout(2000)

    # Navigate to Employee module
    page.goto("https://qa.hrmgenie.outstrive.co/employee/general")
    page.get_by_role("button", name="Team's Members").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_06_team_members")

    # Filter by Designation
    page.get_by_role("combobox").filter(has_text="All Designations").click()
    page.get_by_label("Senior FP&A Analyst").get_by_text("Senior FP&A Analyst").click()
    page.wait_for_timeout(1000)
    # Filter by Department
    page.get_by_role("combobox").filter(has_text="All Departments").click()
    page.get_by_label("Finance").get_by_text("Finance").click()
    page.wait_for_timeout(1000)
    # Filter by All Location
    page.get_by_role("combobox").filter(has_text="All Locations").click()
    page.get_by_role("option", name="Bangalore").click()

    # Search
    page.get_by_role("textbox", name="Search...").click()
    page.get_by_role("textbox", name="Search...").fill("adfas")
    page.wait_for_timeout(1000)
    _screenshot(page, "test_06_team_members_filter")

    # Resetting the filters
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_06_team_members_reset")

    # Get the data
    cell_lines = (
        page.locator("tbody tr").first.locator("td").nth(1).inner_text().split("\n")
    )
    print("Cell Lines ----> ", cell_lines)
    employee_name = cell_lines[2].strip()
    print("Employee Name ----> ", employee_name)

    # Clicks on the employee name
    page.locator("tbody tr").first.locator("td").first.click()

    # Verifies if the employee name is visible
    expect(page.get_by_role("heading", name=employee_name)).to_be_visible()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_06_team_members_employee_info")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_team_members(playwright)
