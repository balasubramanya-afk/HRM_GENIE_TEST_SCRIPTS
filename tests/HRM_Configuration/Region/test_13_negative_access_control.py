"""
test_13_negative_access_control.py
==================================
Negative test cases for HRM Genie -> HRM Configuration -> Region module (Access Control / RBAC).

Scenarios covered:
  1. Restricted roles (Employee, Manager, BUH, CXO) navigating to the Region page URL
     -> redirected or shown access denied / forbidden message, no management controls visible.
"""

import sys
import os
import re
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot

REGION_URL = "https://qa.hrmgenie.outstrive.co/hrm-config/region"
RESTRICTED_ROLES = ["Employee", "Manager", "BUH", "CXO"]


def create_page(playwright: Playwright, role: str = "HR"):
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
    login_as(page, role)
    return browser, context, page


# ---------------------------------------------------------------------------
# Access control negative tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("role", RESTRICTED_ROLES)
def test_restricted_role_cannot_access_region_page(playwright: Playwright, role: str) -> None:
    """A role without HRM Configuration access should not be able to reach the
    Region page by direct URL - it should be redirected or shown a blocked/403
    state, not the Region list with its management controls."""
    browser, context, page = create_page(playwright, role)
    try:
        page.goto(REGION_URL)
        page.wait_for_timeout(1500)
        _screenshot(page, f"test_13_region_access_blocked_{role.lower().replace(' ', '_')}")

        blocked = (
            "hrm-config/region" not in page.url
            or page.get_by_text(re.compile(r"not authorized|access denied|forbidden|permission", re.I)).count() > 0
        )
        create_region_button = page.get_by_role("button", name=re.compile(r"^\+?\s*Region$", re.I))

        assert blocked or create_region_button.count() == 0, (
            f"Role '{role}' was able to reach the Region page with management controls "
            f"visible at {page.url}"
        )
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        for r in RESTRICTED_ROLES:
            test_restricted_role_cannot_access_region_page(playwright, r)
