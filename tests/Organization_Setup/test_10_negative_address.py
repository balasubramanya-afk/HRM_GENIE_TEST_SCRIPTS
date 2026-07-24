import os
import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup

INVALID_POST_CODES = [
    "",              # empty - required field
    "ABCDE",         # letters instead of digits
    "12",            # too short
    "1234567890123", # unreasonably long
    "56-0008",       # invalid characters
]


def ensure_on_org_info_page(page):
    """Ensures page is logged in and navigated to Organization Setup."""
    if "organisation-info" not in page.url:
        login_as(page, "HR")
        navigate_to_organization_setup(page)
    page.wait_for_timeout(1000)


def is_address_editor_open(page) -> bool:
    """Returns True if the Address editor is currently open."""
    return (
        page.get_by_role("textbox", name="Primary Address *").count() > 0
        and page.get_by_role("textbox", name="Primary Address *").first.is_visible()
    )


def close_address_editor(page):
    """Closes the Address editor via Close or Discard button if open."""
    if is_address_editor_open(page):
        card = page.locator(".rounded-xl.border").filter(has_text="Address").first
        close_btn = card.get_by_role("button", name=re.compile("close|discard|cancel", re.I))
        if close_btn.count() > 0 and close_btn.first.is_visible():
            close_btn.first.click()
            page.wait_for_timeout(500)


def open_section_editor(page, section_heading: str = "Address"):
    """Clicks the edit (pencil) icon for Address section."""
    if is_address_editor_open(page):
        return
    card = page.locator(".rounded-xl.border").filter(has_text=section_heading).first
    edit_button = card.locator(".tracking-tight > .inline-flex, button").first
    edit_button.click()
    page.wait_for_timeout(1000)


def restore_default_address(page):
    """Restores Address to valid default values."""
    ensure_on_org_info_page(page)
    open_section_editor(page, "Address")

    page.get_by_role("textbox", name="Primary Address *").fill(
        "911/B, 8th Floor, Oxford Towers, New Municipal No.139, Opp. Leela Palace, HAL Old Airport Rd, Kodihalli, Bangalore"
    )
    country_dropdown = page.get_by_text("Country", exact=False).locator("xpath=following::button[@role='combobox'][1]")
    country_dropdown.click()
    page.get_by_role("option", name="India", exact=True).click()

    state_dropdown = page.get_by_text("State", exact=False).locator("xpath=following::button[@role='combobox'][1]")
    state_dropdown.click()
    page.get_by_role("option", name="Karnataka", exact=True).click()

    page.get_by_role("textbox", name="City *").fill("Bengaluru")
    page.get_by_role("textbox", name="Post Code *").fill("560008")

    save_button = page.get_by_role("button", name=re.compile("save", re.I))
    save_button.click()
    page.wait_for_timeout(1500)


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
    login_as(page, "HR")
    navigate_to_organization_setup(page)
    page.wait_for_timeout(1000)
    return browser, context, page


# ---------------------------------------------------------------------------
# Address - negative cases
# ---------------------------------------------------------------------------

def test_empty_primary_address_blocked_on_save(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Address")

        address_field = page.get_by_role("textbox", name="Primary Address *")
        address_field.fill("")

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()

        is_invalid = address_field.evaluate(
            "el => !el.checkValidity() || el.getAttribute('aria-invalid') === 'true' || el.matches(':invalid')"
        )
        assert is_invalid or page.get_by_text(re.compile("required|cannot be empty", re.I)).count() > 0
        close_address_editor(page)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App accepts invalid Post Code formats (e.g. letters, too short, too long, special chars) "
           "without showing a validation error on Save."
)
@pytest.mark.parametrize("invalid_post_code", INVALID_POST_CODES)
def test_invalid_post_code_rejected(playwright: Playwright, invalid_post_code: str) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Address")

        post_code_field = page.get_by_role("textbox", name="Post Code *")
        post_code_field.fill(invalid_post_code)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()

        error_message = page.get_by_text(re.compile("invalid|required|valid post ?code", re.I))
        expect(error_message).to_be_visible()
        close_address_editor(page)
    finally:
        restore_default_address(page)
        context.close()
        browser.close()


def test_state_options_scoped_to_selected_country(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Address")

        country_dropdown = page.get_by_text("Country", exact=False).locator("xpath=following::button[@role='combobox'][1]")
        country_dropdown.click()
        page.get_by_role("option", name="India", exact=True).click()

        state_dropdown = page.get_by_text("State", exact=False).locator("xpath=following::button[@role='combobox'][1]")
        state_dropdown.click()
        invalid_state_option = page.get_by_role("option", name="California", exact=True)
        expect(invalid_state_option).not_to_be_visible()
        close_address_editor(page)
    finally:
        context.close()
        browser.close()


def test_close_without_save_discards_address_changes(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Address")

        city_field = page.get_by_role("textbox", name="City *")
        original_city = city_field.input_value()

        city_field.fill("Some Other City " + os.urandom(2).hex())

        close_button = page.get_by_role("button", name=re.compile("close|cancel|discard", re.I)).first
        close_button.click()
        page.wait_for_timeout(500)

        if original_city:
            expect(page.get_by_text(original_city).first).to_be_visible()
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_empty_primary_address_blocked_on_save(playwright)
        test_invalid_post_code_rejected(playwright, "ABCDE")
        test_state_options_scoped_to_selected_country(playwright)
        test_close_without_save_discards_address_changes(playwright)


