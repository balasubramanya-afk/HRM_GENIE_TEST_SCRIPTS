import os
import re
import pytest
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup, close_toast, _screenshot

SOURCE_DIR = Path(__file__).resolve().parents[2] / "Source_files"
if not SOURCE_DIR.exists():
    SOURCE_DIR = Path(__file__).resolve().parents[1] / "Source_files"


def ensure_on_org_info_page(page):
    """Ensures the page is logged in and on Organization Setup."""
    if "organisation-info" not in page.url:
        login_as(page, "HR")
        navigate_to_organization_setup(page)
    page.wait_for_timeout(1000)


def is_logo_editor_open(page) -> bool:
    """Returns True if the Company Logo editor is currently open (Close button visible)."""
    logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
    close_btn = logo_card.get_by_role("button", name="Close")
    return close_btn.count() > 0 and close_btn.is_visible()


def open_company_logo_editor(page):
    """Opens the Company Logo section editor. Idempotent - skips if already open."""
    if is_logo_editor_open(page):
        return
    page.locator(".tracking-tight > .inline-flex").first.click()
    page.wait_for_timeout(1000)


def close_logo_editor(page):
    """Closes the Company Logo editor via the 'Close' button. Safe to call if already closed."""
    logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
    close_btn = logo_card.get_by_role("button", name="Close")
    if close_btn.count() > 0 and close_btn.is_visible():
        close_btn.click()
        page.wait_for_timeout(500)


def get_logo_input(page, logo_section: str):
    """Returns the file input element for the given logo section using confirmed IDs."""
    section_map = {
        "Logo dark": "#logo-dark",
        "Logo Light": "#logo-light",
        "Favicon": "#favicon",
    }
    return page.locator(section_map[logo_section])


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
# Company Logo - negative cases
# ---------------------------------------------------------------------------

def test_close_without_save_discards_selected_file(playwright: Playwright) -> None:
    """Regression guard: opening editor, picking a file, then clicking Close should NOT
    persist the favicon to the server."""
    browser, context, page = create_page(playwright)
    try:
        temp_wrong_extension_image = str(SOURCE_DIR / "logo.bmp")
        if not Path(temp_wrong_extension_image).exists():
            Path(temp_wrong_extension_image).write_bytes(os.urandom(1024))

        ensure_on_org_info_page(page)
        logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
        favicon_section = logo_card.locator("div").filter(has_text="Favicon").last
        favicon_img = favicon_section.locator("img").first
        original_src = ""
        if favicon_img.count() > 0 and favicon_img.is_visible():
            original_src = favicon_img.get_attribute("src") or ""

        open_company_logo_editor(page)
        upload_input = get_logo_input(page, "Favicon")
        upload_input.set_input_files(temp_wrong_extension_image)
        page.wait_for_timeout(500)
        _screenshot(page, "test_07_logo_close_without_save")

        close_logo_editor(page)
        page.wait_for_timeout(1000)

        save_btn_in_heading = logo_card.get_by_role("button", name="Save")
        close_btn_in_heading = logo_card.get_by_role("button", name="Close")
        expect(save_btn_in_heading).not_to_be_visible(timeout=3000)
        expect(close_btn_in_heading).not_to_be_visible(timeout=3000)

        page.reload(wait_until="networkidle")
        page.wait_for_timeout(1500)

        logo_card_after = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
        favicon_section_after = logo_card_after.locator("div").filter(has_text="Favicon").last
        favicon_img_after = favicon_section_after.locator("img").first
        _screenshot(page, "test_07_logo_discard_verified")

        if original_src:
            actual_src = favicon_img_after.get_attribute("src") if favicon_img_after.count() > 0 else ""
            assert actual_src == original_src
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App does not currently show a client-side validation error when a "
           "non-image file (e.g. PDF, TXT) is selected. Expected behaviour: an inline "
           "error like 'Invalid file type' or 'Only images are supported' should appear."
)
@pytest.mark.parametrize("logo_section", ["Logo dark", "Logo Light", "Favicon"])
def test_reject_non_image_file_type(playwright: Playwright, logo_section: str) -> None:
    """Uploading a non-image file should show an invalid-file-type validation error."""
    browser, context, page = create_page(playwright)
    try:
        pdf_path = SOURCE_DIR / "3-mb-sample-pdf-file.pdf"
        temp_invalid_file = str(pdf_path) if pdf_path.exists() else str(SOURCE_DIR / "invalid_logo.txt")
        if not Path(temp_invalid_file).exists():
            Path(temp_invalid_file).write_text("Sample file to check the Logo upload actions")

        ensure_on_org_info_page(page)
        open_company_logo_editor(page)

        upload_input = get_logo_input(page, logo_section)
        upload_input.set_input_files(temp_invalid_file)
        page.wait_for_timeout(1000)
        _screenshot(page, f"test_07_non_image_{logo_section.lower().replace(' ', '_')}")

        error_message = page.get_by_text(
            re.compile(r"invalid file|unsupported format|only (images|png|jpg|svg)", re.I)
        )
        expect(error_message).to_be_visible(timeout=5000)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App does not currently show a client-side validation error when an "
           "oversized file (>5MB) is selected. Expected behaviour: an inline error "
           "like 'File size exceeds limit' or 'File too large' should appear."
)
@pytest.mark.parametrize("logo_section", ["Logo dark", "Logo Light", "Favicon"])
def test_reject_oversized_file(playwright: Playwright, logo_section: str) -> None:
    """Uploading a file larger than the allowed limit should show a file-size error."""
    browser, context, page = create_page(playwright)
    try:
        temp_oversized_file = str(SOURCE_DIR / "oversized_logo.png")
        if not Path(temp_oversized_file).exists():
            Path(temp_oversized_file).write_bytes(os.urandom(6 * 1024 * 1024))

        ensure_on_org_info_page(page)
        open_company_logo_editor(page)

        upload_input = get_logo_input(page, logo_section)
        upload_input.set_input_files(temp_oversized_file)
        page.wait_for_timeout(1000)
        _screenshot(page, f"test_07_oversized_{logo_section.lower().replace(' ', '_')}")

        error_message = page.get_by_text(re.compile(r"file size|too large|exceeds", re.I))
        expect(error_message).to_be_visible(timeout=5000)
    finally:
        context.close()
        browser.close()


@pytest.mark.xfail(
    reason="BUG: App may keep the Save button enabled even when no new file has been "
           "selected in the editor. Expected behaviour: Save should be disabled until "
           "a valid new file is chosen."
)
def test_save_stays_disabled_with_no_file_selected(playwright: Playwright) -> None:
    """Save button should stay disabled when the editor is opened with no new file chosen."""
    browser, context, page = create_page(playwright)
    try:
        ensure_on_org_info_page(page)
        open_company_logo_editor(page)
        _screenshot(page, "test_07_no_file_selected")

        logo_card = page.locator(".rounded-xl.border").filter(has_text="Company Logo")
        save_button = logo_card.get_by_role("button", name="Save")
        expect(save_button).to_be_disabled(timeout=3000)
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_close_without_save_discards_selected_file(playwright)
        test_reject_non_image_file_type(playwright, "Logo dark")
        test_reject_oversized_file(playwright, "Logo dark")
        test_save_stays_disabled_with_no_file_selected(playwright)



