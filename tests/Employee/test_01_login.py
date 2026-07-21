from playwright.sync_api import Page, Playwright, sync_playwright
import re
import datetime
from pathlib import Path

BASE_URL = "https://qa.hrmgenie.outstrive.co/"

# Save screenshots in the 'screenshots' folder inside my_leaves
SCREENSHOT_BASE = Path(__file__).parent / "screenshots"

def _screenshot(page: Page, name: str):
    """Save screenshot with timestamp."""
    SCREENSHOT_BASE.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=SCREENSHOT_BASE / f"{name}_{ts}.png", full_page=True)

def login(page):
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("gattu.ashwitha@brilyant.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("Ramesh@12345")
    page.get_by_role("button", name="Show password").click()
    page.get_by_role("button", name="Hide password").click()
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")


def test_login(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_login(playwright)
