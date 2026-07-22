from playwright.sync_api import Playwright, sync_playwright
from config import login_as, navigate_to_organization_setup, _screenshot


def test_primary_address(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_organization_setup(page)

    # Open primary address section
    page.locator(
        "div:nth-child(4) > .flex.flex-col > .tracking-tight > .inline-flex"
    ).click()
    _screenshot(page, "test_05_primary_address_open")

    # Fill primary address -> Discard
    page.get_by_role("textbox", name="Primary Address *").click()
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Primary Address *").fill(
        "911/B, 8th Floor, Oxford Towers, New Municipal No.139, Opp. Leela Palace,  HAL Old Airport Rd, Kodihalli, Bangalore"
    )
    page.get_by_role("button", name="Discard").click()
    _screenshot(page, "test_05_primary_address_discarded")

    # Fill city and post code -> Discard
    page.locator(
        "div:nth-child(4) > .flex.flex-col > .tracking-tight > .inline-flex"
    ).click()
    page.get_by_role("textbox", name="City *").click()
    page.get_by_role("textbox", name="City *").fill("Bangalore")
    page.get_by_role("textbox", name="City *").press("Enter")
    page.get_by_role("textbox", name="Post Code *").click()
    page.get_by_role("textbox", name="Post Code *").fill("560021")
    page.get_by_role("button", name="Discard").click()
    _screenshot(page, "test_05_city_postcode_discarded")

    # Change state to Tamil Nadu, city to Chennai -> Save
    page.locator(
        "div:nth-child(4) > .flex.flex-col > .tracking-tight > .inline-flex"
    ).click()
    page.get_by_role("combobox").filter(has_text="Karnataka").click()
    page.get_by_role("option", name="Tamil Nadu").click()
    page.get_by_role("textbox", name="City *").click()
    page.get_by_role("textbox", name="City *").fill("Chennai")
    page.get_by_role("textbox", name="City *").press("Enter")
    page.get_by_role("button", name="Save").click()
    _screenshot(page, "test_05_state_chennai_saved")

    # Edit state back to Karnataka, update city and post code -> Save
    page.locator(
        "div:nth-child(4) > .flex.flex-col > .tracking-tight > .inline-flex"
    ).click()
    page.get_by_role("combobox").filter(has_text="Tamil Nadu").click()
    page.get_by_role("option", name="Karnataka").click()
    page.get_by_role("textbox", name="City *").click()
    page.get_by_role("textbox", name="City *").fill("Bengaluru")
    page.get_by_role("textbox", name="Post Code *").click()
    page.get_by_role("textbox", name="Post Code *").fill("560008")
    page.get_by_role("button", name="Save").click()
    _screenshot(page, "test_05_state_karnataka_saved")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_primary_address(playwright)
