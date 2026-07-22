import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup, _screenshot, close_toast

SOURCE_DIR = Path(__file__).resolve().parents[2] / "Source_files"
if not SOURCE_DIR.exists():
    SOURCE_DIR = Path(__file__).parent / "Source_files"


def test_logo_edit(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
        args=["--start-maximized"],
        slow_mo=slow_mo,
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_organization_setup(page)
    page.wait_for_timeout(2000)
    _screenshot(page, "test_06_before_logo_edit")

    logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")

    # --- 1. Open Logo Edit Mode ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)

    # --- 2. Remove & Replace Logo Dark ---
    logo_dark_sec = logo_card.locator("div.space-y-4").filter(has_text="Logo dark")
    remove_dark_btn = logo_dark_sec.locator("button.absolute")
    if remove_dark_btn.count() > 0 and remove_dark_btn.first.is_visible():
        remove_dark_btn.first.click()
        page.wait_for_timeout(500)
    page.locator("#logo-dark").set_input_files(
        os.path.join(SOURCE_DIR, "Tom_and_Jerry_Dark_Icon.jpeg")
    )
    page.wait_for_timeout(1500)
    logo_card.get_by_role("button", name="Save").click()
    close_toast(page)
    page.wait_for_timeout(1500)
    _screenshot(page, "test_06_after_logo_dark_reupload")

    # --- 3. Re-enter Edit Mode & Replace Logo Light ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    logo_light_sec = logo_card.locator("div.space-y-4").filter(has_text="Logo Light")
    remove_light_btn = logo_light_sec.locator("button.absolute")
    if remove_light_btn.count() > 0 and remove_light_btn.first.is_visible():
        remove_light_btn.first.click()
        page.wait_for_timeout(500)
    page.locator("#logo-light").set_input_files(
        os.path.join(SOURCE_DIR, "Pink_Panther_Light_Icon.jpeg")
    )
    page.wait_for_timeout(1500)
    logo_card.get_by_role("button", name="Save").click()
    close_toast(page)
    page.wait_for_timeout(1500)
    _screenshot(page, "test_06_after_logo_light_reupload")

    # --- 4. Re-enter Edit Mode & Replace Favicon ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    favicon_sec = logo_card.locator("div.space-y-4").filter(has_text="Favicon")
    remove_favicon_btn = favicon_sec.locator("button.absolute")
    if remove_favicon_btn.count() > 0 and remove_favicon_btn.first.is_visible():
        remove_favicon_btn.first.click()
        page.wait_for_timeout(500)
    page.locator("#favicon").set_input_files(
        os.path.join(SOURCE_DIR, "Looney_tunes_Favicon.jpeg")
    )
    page.wait_for_timeout(1500)
    logo_card.get_by_role("button", name="Save").click()
    close_toast(page)
    page.wait_for_timeout(1500)
    _screenshot(page, "test_06_after_favicon_reupload")


    # --- 5. Verify Close Button in Logo Edit Mode ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)
    close_btn = logo_card.get_by_role("button", name="Close")
    expect(close_btn).to_be_visible(timeout=10000)
    close_btn.click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_06_logo_edit_closed")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_logo_edit(playwright)