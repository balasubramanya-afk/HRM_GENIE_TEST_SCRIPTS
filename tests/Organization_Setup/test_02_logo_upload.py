import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright
from config import login_as, navigate_to_organization_setup, _screenshot

SOURCE_DIR = Path(__file__).resolve().parents[2] / "Source_files"
if not SOURCE_DIR.exists():
    SOURCE_DIR = Path(__file__).parent / "Source_files"


def test_logo_upload(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_organization_setup(page)
    _screenshot(page, "test_02_before_logo_upload")

    # --- Upload logo-dark ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    page.locator("#logo-dark").set_input_files(os.path.join(SOURCE_DIR, "Blind_Logo_dark.png"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()
    _screenshot(page, "test_02_logo_dark_uploaded")
    page.wait_for_timeout(1000)

    # --- Upload logo-light ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    page.locator("#logo-light").set_input_files(os.path.join(SOURCE_DIR, "Floursecent_Icon_Light.png"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()
    _screenshot(page, "test_02_logo_light_uploaded")
    page.wait_for_timeout(1000)

    # --- Upload favicon ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    page.locator("#favicon").set_input_files(os.path.join(SOURCE_DIR, "Heart_plus_Favicon.png"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()
    _screenshot(page, "test_02_favicon_uploaded")
    page.wait_for_timeout(1000)

    # --- Re-upload dark logo with alternate image ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    page.locator("#logo-dark").set_input_files(os.path.join(SOURCE_DIR, "Tom_and_Jerry_Dark_Icon.jpeg"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()
    _screenshot(page, "test_02_logo_dark_reuploaded")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_logo_upload(playwright)