import os
from playwright.sync_api import Playwright, sync_playwright
from test_01_login import login, navigate_to_organization_setup

SOURCE_DIR = os.path.join(os.path.dirname(__file__), "Source_files")


def test_logo_upload(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login(page)
    navigate_to_organization_setup(page)

    # --- Upload logo-dark ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.get_by_text("Choose file here").first.click()
    page.locator("#logo-dark").set_input_files(os.path.join(SOURCE_DIR, "Blind_Logo_dark.png"))
    page.get_by_role("button", name="Save").first.click()
    # NOTE: ".absolute.right-2" matches multiple "remove image" buttons on this
    # page (strict mode violation). Using .first as a stopgap fix. Replace with
    # a scoped/unique locator (e.g. data-testid) once available - see TODO below.
    page.locator(".absolute.right-2").first.click()

    # --- Upload logo-light ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.get_by_text("Choose file here").nth(1).click()
    page.locator("#logo-light").set_input_files(os.path.join(SOURCE_DIR, "Floursecent_Icon_Light.png"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()

    # --- Upload favicon ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    # NOTE: positional/structural locator (nth-child chain) - fragile if layout
    # changes. Recommend re-recording with codegen once favicon upload row has
    # a stable attribute.
    page.locator("div:nth-child(3) > .relative > .my-4 > .absolute").click()
    page.get_by_text("Choose file here").nth(2).click()
    page.locator("#favicon").set_input_files(os.path.join(SOURCE_DIR, "Heart_plus_Favicon.png"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()

    # --- Additional upload interaction ---
    # TODO: This block clicked "Choose file here" twice but never called
    # set_input_files on a real file input - looked like a copy/paste leftover
    # in the original script. Fill in the correct locator + file path once
    # confirmed which field this section is for (fixed below with a placeholder).
    # --- Re-upload dark logo with alternate image ---
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.get_by_text("Choose file here").first.click()
    page.locator("#logo-dark").set_input_files(os.path.join(SOURCE_DIR, "Tom_and_Jerry_Dark_Icon.jpeg"))
    page.get_by_role("button", name="Save").first.click()
    page.locator(".absolute.right-2").first.click()

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_logo_upload(playwright)