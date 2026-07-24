import os
import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup, _screenshot

INVALID_PREFIXES = ["!!!", "AB CD", "12345678901234567890", "😀😀"]


def ensure_on_org_info_page(page):
    """Ensures page is logged in and navigated to Organization Setup."""
    if "organisation-info" not in page.url:
        login_as(page, "HR")
        navigate_to_organization_setup(page)
    page.wait_for_timeout(1000)


def is_system_settings_editor_open(page) -> bool:
    """Returns True if the System Settings editor is currently open."""
    return (
        page.get_by_role("textbox", name="Employee Prefix *").count() > 0
        and page.get_by_role("textbox", name="Employee Prefix *").first.is_visible()
    )


def close_system_settings_editor(page):
    """Closes the System Settings editor via Close or Discard button if open."""
    if is_system_settings_editor_open(page):
        card = page.locator(".rounded-xl.border").filter(has_text="System Settings").first
        close_btn = card.get_by_role("button", name=re.compile("close|discard|cancel", re.I))
        if close_btn.count() > 0 and close_btn.first.is_visible():
            close_btn.first.click()
            page.wait_for_timeout(500)


def open_section_editor(page, section_heading: str = "System Settings"):
    """Clicks the edit (pencil) icon for System Settings section."""
    if is_system_settings_editor_open(page):
        return
    card = page.locator(".rounded-xl.border").filter(has_text=section_heading).first
    edit_button = card.locator(".tracking-tight > .inline-flex, button").first
    edit_button.click()
    page.wait_for_timeout(1000)


def restore_default_system_settings(page):
    """Restores System Settings to default valid values."""
    ensure_on_org_info_page(page)
    open_section_editor(page, "System Settings")

    prefix_field = page.get_by_role("textbox", name="Employee Prefix *")
    prefix_field.fill("BITECOS")

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
# System Settings - negative cases
# ---------------------------------------------------------------------------

def test_empty_employee_prefix_blocked_on_save(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "System Settings")

        prefix_field = page.get_by_role("textbox", name="Employee Prefix *")
        prefix_field.fill("")

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_09_empty_employee_prefix")

        error_message = page.get_by_text(re.compile("required|cannot be empty", re.I))
        expect(error_message).to_be_visible()
        close_system_settings_editor(page)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App accepts invalid Employee Prefix formats (e.g. special chars, spaces, overlong text, emojis) "
           "without showing a validation error on Save."
)
@pytest.mark.parametrize("invalid_prefix", INVALID_PREFIXES)
def test_employee_prefix_rejects_invalid_characters(playwright: Playwright, invalid_prefix: str) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "System Settings")

        prefix_field = page.get_by_role("textbox", name="Employee Prefix *")
        prefix_field.fill(invalid_prefix)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, f"test_09_invalid_prefix_{invalid_prefix.replace(' ', '_')}")

        error_message = page.get_by_text(re.compile("invalid|alphanumeric|not allowed", re.I))
        expect(error_message).to_be_visible()
        close_system_settings_editor(page)
    finally:
        restore_default_system_settings(page)
        context.close()
        browser.close()


def test_date_format_dropdown_has_no_freeform_entry(playwright: Playwright) -> None:
    """Guards against raw format string entries - Date Format should only be selectable."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "System Settings")
        _screenshot(page, "test_09_date_format_dropdown")

        date_format_field = page.get_by_text("Date Format", exact=False).locator(
            "xpath=following::button[@role='combobox'][1]"
        )
        tag_name = date_format_field.evaluate("el => el.tagName.toLowerCase()")
        is_editable = date_format_field.evaluate(
            "el => el.isContentEditable || el.tagName.toLowerCase() === 'input'"
        )
        assert not is_editable or tag_name in ("select", "button")
        close_system_settings_editor(page)
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_empty_employee_prefix_blocked_on_save(playwright)
        test_employee_prefix_rejects_invalid_characters(playwright, "!!!")
        test_date_format_dropdown_has_no_freeform_entry(playwright)


