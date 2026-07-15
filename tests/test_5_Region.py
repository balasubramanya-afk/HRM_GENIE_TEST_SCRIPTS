import re

from playwright.sync_api import expect


def test_region_flow(logged_in_page) -> None:
    page = logged_in_page
    print("Prepare to record Region flow.")

    # Navigate to dashboard to ensure clean page state
    page.goto("https://qa.hrmgenie.outstrive.co/")
    page.wait_for_load_state("networkidle")

    
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).click()
    page.get_by_role("button", name="Region").click()
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("south")
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("")
    page.get_by_role("textbox", name="Search", exact=True).click()
    page.get_by_role("textbox", name="Search", exact=True).fill("")