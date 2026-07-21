import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, _screenshot, close_toast


def test_indirect_reportees(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login_as(page, "BUH")
    page.wait_for_timeout(2000)

    # Navigate to Employee module
    page.goto("https://qa.hrmgenie.outstrive.co/employee/general")
    page.get_by_role("button", name="Indirect Reportees").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_07_indirect_reportees")

    # Filter by Designation
    page.get_by_role("combobox").filter(has_text="All Designations").click()
    page.get_by_role("option", name="Senior FP&A Analyst").click()

    # Filter by Department
    page.get_by_role("combobox").filter(has_text="All Departments").click()
    page.get_by_role("option", name="Finance").click()

    # Filter by All location
    page.get_by_role("combobox").filter(has_text="All Locations").click()
    page.get_by_role("option", name="Kerala").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_07_indirect_reportees_filter")
    # Resetting the filters
    page.get_by_role("button", name="Reset Filters").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_07_indirect_reportees_reset")

    # Get the Data
    cell_lines = (
        page.locator("tbody tr").first.locator("td").nth(1).inner_text().split("\n")
    )
    print("Cell Lines ----> ", cell_lines)
    employee_name = cell_lines[2].strip()
    print("Employee Name ----> ", employee_name)

    # Clicks on the employee name
    page.locator("tbody tr").first.locator("td").first.click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_07_indirect_reportees_profile")
    # Verifies if the employee name is visible
    expect(page.get_by_role("heading", name=employee_name)).to_be_visible()

    close_toast(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_indirect_reportees(playwright)
