import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot, navigate_to_region


def test_login(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_region(page)
    _screenshot(page, "test_01_region_module")
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_login(playwright)
