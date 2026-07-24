"""
Negative test cases for Employee module: Documents.

Covers:
  - Documents tab rejects invalid uploads (wrong file type / no file selected).
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Playwright, sync_playwright
from config import login_as, _screenshot, close_toast
from test_05_delete_files import delete_uploaded_files

BASE_URL = "https://qa.hrmgenie.outstrive.co"

INVALID_FILE_PATH = str(
    Path(__file__).parent.parent.parent / "Source_files" / "invalid_sample.txt"
)


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
    login_as(page, "BUH")
    return browser, context, page


# ---------------------------------------------------------------------------
# Documents - invalid upload handling
# ---------------------------------------------------------------------------

@pytest.mark.xfail(
    reason="BUG: Application accepts invalid file types (.txt) in document slots without rejecting them or displaying validation error"
)
def test_documents_invalid_file_type_rejected(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        page.goto(f"{BASE_URL}/employee/documents")
        page.wait_for_timeout(1000)

        # Delete any existing files for a clean state
        delete_uploaded_files(page)

        # Target document file input (e.g. input[id^='docx-']) instead of generic input[type='file'].first (which targets #profilePhoto)
        docx_input = page.locator("input[id^='docx-']").first
        if docx_input.count() > 0:
            docx_input.set_input_files(INVALID_FILE_PATH)
            page.wait_for_timeout(500)

            upload_button = page.get_by_role(
                "button", name=re.compile("upload selected file", re.I)
            )
            if upload_button.count() > 0 and upload_button.is_enabled():
                upload_button.click()
                page.wait_for_timeout(1000)

            _screenshot(page, "test_09_invalid_file_type")

            # Check that success toast DOES NOT appear
            success_toast = page.get_by_text(re.compile("uploaded successfully|success", re.I))
            assert success_toast.count() == 0, (
                "Application accepted an invalid file type (.txt) into document slot and displayed success. "
                "Expected upload of invalid file type to be rejected."
            )

            # Check for explicit error message / error toast
            error_message = page.get_by_text(
                re.compile("invalid file|unsupported|not allowed|file type|failed|error", re.I)
            )
            assert error_message.count() > 0, (
                "Expected an error message or rejection toast when uploading an invalid file type (.txt)."
            )
    finally:
        delete_uploaded_files(page)
        close_toast(page)
        context.close()
        browser.close()


def test_documents_upload_without_selecting_file(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        page.goto(f"{BASE_URL}/employee/documents")
        page.wait_for_timeout(1000)

        # No document file input has been chosen
        upload_button = page.get_by_role(
            "button", name=re.compile("upload selected file", re.I)
        )
        if upload_button.count() > 0 and upload_button.first.is_enabled():
            upload_button.first.click()
            page.wait_for_timeout(500)
            error_message = page.get_by_text(
                re.compile("select a file|no file chosen|required|error", re.I)
            )
            assert error_message.count() > 0 or not upload_button.first.is_enabled()
        else:
            assert upload_button.count() == 0 or not upload_button.first.is_enabled()

        _screenshot(page, "test_09_upload_no_file_selected")
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_documents_invalid_file_type_rejected(playwright)
        test_documents_upload_without_selecting_file(playwright)
