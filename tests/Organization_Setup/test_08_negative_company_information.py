import os
import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup, _screenshot

INVALID_EMAILS = [
    "plainaddress",
    "missing-domain@",
    "@missing-local.com",
    "spaces in@email.com",
    "double@@at.com",
]

INVALID_WEBSITES = [
    "not a url",
    "ftp:/broken.com",
    "www .brilyant.com",
    "http://",
]


def ensure_on_org_info_page(page):
    """Ensures page is logged in and navigated to Organization Setup."""
    if "organisation-info" not in page.url:
        login_as(page, "HR")
        navigate_to_organization_setup(page)
    page.wait_for_timeout(1000)


def is_company_info_editor_open(page) -> bool:
    """Returns True if the Company Information editor is currently open."""
    return (
        page.get_by_role("textbox", name="Company Name *").count() > 0
        and page.get_by_role("textbox", name="Company Name *").first.is_visible()
    )


def close_company_info_editor(page):
    """Closes the Company Information editor via Close or Discard button if open."""
    if is_company_info_editor_open(page):
        company_card = page.locator(".rounded-xl.border").filter(has_text="Company Information").first
        close_btn = company_card.get_by_role("button", name=re.compile("close|discard|cancel", re.I))
        if close_btn.count() > 0 and close_btn.first.is_visible():
            close_btn.first.click()
            page.wait_for_timeout(500)


def open_section_editor(page, section_heading: str = "Company Information"):
    """Opens the section editor for the given heading. Idempotent – skips if already open."""
    if is_company_info_editor_open(page):
        return
    company_card = page.locator(".rounded-xl.border").filter(has_text=section_heading).first
    edit_button = company_card.locator(".tracking-tight > .inline-flex, button").first
    edit_button.click()
    page.wait_for_timeout(1000)


def restore_default_company_info(page):
    """Restores Company Information to valid default values."""
    ensure_on_org_info_page(page)
    open_section_editor(page, "Company Information")

    page.get_by_role("textbox", name="Company Name *").fill("Brilyant IT Solutions Pvt Ltd")
    page.get_by_role("textbox", name="Company Website *").fill("www.brilyant.com")
    page.get_by_role("textbox", name="Company Email *").fill("info@out-strive.com")
    page.get_by_role("textbox", name="Mobile Number *").fill("8901234567")
    page.get_by_role("textbox", name="Domain Name *").fill("outstrive.com")

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
# Company Information - negative cases
# ---------------------------------------------------------------------------

def test_empty_company_name_blocked_on_save(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Company Information")

        company_name_field = page.get_by_role("textbox", name="Company Name *")
        company_name_field.fill("")

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_08_empty_company_name")

        error_message = page.get_by_text(re.compile("required|cannot be empty", re.I))
        expect(error_message).to_be_visible()
        close_company_info_editor(page)
    finally:
        context.close()
        browser.close()


@pytest.mark.parametrize("invalid_email", INVALID_EMAILS)
def test_invalid_contact_email_rejected(playwright: Playwright, invalid_email: str) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Company Information")

        email_field = page.get_by_role("textbox", name="Company Email *")
        email_field.fill(invalid_email)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, f"test_08_invalid_email_{invalid_email.replace('@', '_at_')}")

        error_message = page.get_by_text(re.compile("valid email|invalid email", re.I))
        expect(error_message).to_be_visible()
        close_company_info_editor(page)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App does not validate Company Website format upon Save. "
           "Invalid URLs (e.g., 'not a url', 'ftp:/broken.com', 'http://') are accepted "
           "without showing a validation error."
)
@pytest.mark.parametrize("invalid_url", INVALID_WEBSITES)
def test_invalid_website_rejected(playwright: Playwright, invalid_url: str) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Company Information")

        website_field = page.get_by_role("textbox", name="Company Website *")
        website_field.fill(invalid_url)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, f"test_08_invalid_website_{invalid_url.replace('://', '_').replace(' ', '_')}")

        error_message = page.get_by_text(re.compile("valid url|invalid (url|website)", re.I))
        expect(error_message).to_be_visible()
        close_company_info_editor(page)
    finally:
        restore_default_company_info(page)
        context.close()
        browser.close()


def test_company_name_rejects_script_injection(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Company Information")

        payload = "<script>window.__xss_triggered = true;</script>"
        company_name_field = page.get_by_role("textbox", name="Company Name *")
        company_name_field.fill(payload)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_08_script_injection")

        triggered = page.evaluate("() => window.__xss_triggered === true")
        assert not triggered
        close_company_info_editor(page)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App does not enforce a maximum character length on Company Name. "
           "Inputs exceeding 300 characters are accepted without showing a character limit error."
)
def test_company_name_exceeding_max_length_rejected(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_section_editor(page, "Company Information")

        overlong_name = "A" * 300
        company_name_field = page.get_by_role("textbox", name="Company Name *")
        company_name_field.fill(overlong_name)

        save_button = page.get_by_role("button", name=re.compile("save", re.I))
        save_button.click()
        page.wait_for_timeout(500)
        _screenshot(page, "test_08_overlong_company_name")

        error_message = page.get_by_text(re.compile("maximum|too long|character limit", re.I))
        expect(error_message).to_be_visible()
        close_company_info_editor(page)
    finally:
        restore_default_company_info(page)
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_empty_company_name_blocked_on_save(playwright)
        test_invalid_contact_email_rejected(playwright, "double@@at.com")
        test_invalid_website_rejected(playwright, "http://")
        test_company_name_rejects_script_injection(playwright)
        test_company_name_exceeding_max_length_rejected(playwright)


