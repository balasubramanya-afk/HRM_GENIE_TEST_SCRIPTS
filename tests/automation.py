from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, Playwright, sync_playwright


LOGIN_URL = "https://qa.hrmgenie.outstrive.co/login"
AUTH_STATE_PATH = Path(__file__).resolve().parent.parent / ".auth-state.json"


def assert_login_page(page: Page) -> None:
    page.wait_for_load_state("networkidle")
    assert page.url.startswith(LOGIN_URL), f"Expected login page, but got: {page.url}"
    assert page.get_by_role("button", name="Login").is_visible()


def login(page: Page) -> None:
    page.goto(LOGIN_URL)
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("hr@out-strive.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("HR@dmin06")
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")


def run_negative_cases(page: Page) -> None:
    page.goto(LOGIN_URL)
    assert_login_page(page)

    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(1000)
    assert_login_page(page)

    page.get_by_role("textbox", name="Enter email").fill("invalid-email")
    page.get_by_role("textbox", name="Enter password").fill("wrong-password")
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(2000)
    assert_login_page(page)


def run_positive_case(page: Page) -> None:
    login(page)


def save_auth_state(context, path: Optional[Path] = None) -> None:
    target = path or AUTH_STATE_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(target))


def run(playwright: Playwright, wait_for_exit: bool = False) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    run_negative_cases(page)
    run_positive_case(page)

    if wait_for_exit:
        print("Automation complete. The browser will stay open until you press Enter.")
        input("Press Enter to close the browser and exit...")

    context.close()
    browser.close()


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright, wait_for_exit=True)


if __name__ == "__main__":
    main()
