"""
Negative test cases for Employee module: My Details sub-tabs.

Covers:
  - My Details sub-tabs (General, Job Profile, Education, Experience, Promotions)
    are strictly read-only -- no editable fields/save/edit controls should ever
    appear on these pages.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Playwright, Page, sync_playwright
from config import login_as, _screenshot

BASE_URL = "https://qa.hrmgenie.outstrive.co"

READ_ONLY_TABS = {
    "General": "/employee/general",
    "Job Profile": "/employee/profile",
    "Education": "/employee/education",
    "Experience": "/employee/experience",
    "Promotions": "/employee/promotions",
}


def create_page(playwright: Playwright):
    headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=headless,
        slow_mo=slow_mo,
        args=["--start-maximized"],
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "BUH")
    return browser, context, page


def assert_page_is_read_only(page: Page):
    """Fails if any editable field or save/edit button is present."""
    textboxes = page.get_by_role("textbox")
    editable_count = 0
    for i in range(textboxes.count()):
        tb = textboxes.nth(i)
        placeholder = tb.get_attribute("placeholder") or ""
        if "search" in placeholder.lower():
            continue
        if tb.is_editable():
            editable_count += 1

    assert editable_count == 0, (
        f"Expected no editable textboxes, found {editable_count}"
    )

    save_or_edit_buttons = page.get_by_role(
        "button", name=re.compile(r"^\s*(save|edit)\s*$", re.I)
    )
    assert save_or_edit_buttons.count() == 0, (
        "Expected no Save/Edit buttons on a read-only view, but found "
        f"{save_or_edit_buttons.count()}"
    )


# ---------------------------------------------------------------------------
# My Details - read-only enforcement
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tab_name,tab_path", list(READ_ONLY_TABS.items()))
def test_my_details_tab_is_read_only(
    playwright: Playwright, tab_name: str, tab_path: str
) -> None:
    browser, context, page = create_page(playwright)
    try:
        page.goto(f"{BASE_URL}{tab_path}")
        page.wait_for_timeout(1000)
        assert_page_is_read_only(page)
        _screenshot(page, f"test_08_readonly_{tab_name.lower().replace(' ', '_')}")
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        for tab_name, tab_path in READ_ONLY_TABS.items():
            test_my_details_tab_is_read_only(playwright, tab_name, tab_path)
