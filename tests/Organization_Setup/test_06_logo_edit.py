import os
from playwright.sync_api import Playwright, sync_playwright, expect
from test_01_login import login, navigate_to_organization_setup

SOURCE_DIR = os.path.join(os.path.dirname(__file__), "Source_files")


def test_logo_edit(playwright: Playwright) -> None:
    slow_mo =int(os.getenv("PLAYWRIGHT_SLOW_MO"))
    browser = playwright.chromium.launch(
        channel="chrome", 
        headless=False, 
        args=["--start-maximized"],
        slow_mo= slow_mo
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login(page)
    navigate_to_organization_setup(page)

    logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
    info_card = page.locator(".rounded-xl.border").filter(has_text="Company Information")

    # Replace light logo — upload auto-saves, no Close/Save step exists
    page.locator("#logo-light").set_input_files(
        os.path.join(SOURCE_DIR, "Pink_Panther_Light_Icon.jpeg")
    )
    expect(logo_card.get_by_alt_text("Logo Light Preview")).to_be_visible(timeout=20000)

    # Replace favicon — same auto-save behavior
    page.locator("#favicon").set_input_files(
        os.path.join(SOURCE_DIR, "Looney_tunes_Favicon.jpeg")
    )
    expect(logo_card.get_by_alt_text("Favicon Preview")).to_be_visible(timeout=20000)

    # --- Company Information "Discard" behavior (the real edit/save/discard flow) ---
    edit_pencil = info_card.locator("h3 button")

    # Attempt #1: open edit mode, discard without changing anything
    edit_pencil.click()
    discard_btn = info_card.get_by_role("button", name="Discard")
    expect(discard_btn).to_be_visible(timeout=10000)
    discard_btn.click()

    # Attempt #2: repeat
    expect(edit_pencil).to_be_visible(timeout=10000)
    edit_pencil.click()
    discard_btn = info_card.get_by_role("button", name="Discard")
    expect(discard_btn).to_be_visible(timeout=10000)
    discard_btn.click()

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_logo_edit(playwright)