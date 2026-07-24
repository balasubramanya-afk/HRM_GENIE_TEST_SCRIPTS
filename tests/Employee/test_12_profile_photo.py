"""
Test cases for Employee module: Profile Photo Update (Positive & Negative).

Covers:
  - Positive: Uploading a valid profile photo image (.png/.jpg) updates the avatar and displays "Profile image changed".
  - Negative: Uploading an invalid non-image file (.txt) should be rejected and should not trigger a successful profile photo change.
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pytest
from playwright.sync_api import Playwright, Page, sync_playwright, expect
from config import login_as, _screenshot, close_toast

BASE_URL = "https://qa.hrmgenie.outstrive.co"

VALID_IMAGE_PATH = str(
    Path(__file__).parent.parent.parent / "Source_files" / "Looney_tunes_Favicon.jpeg"
)

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
# Positive Test Case: Update Profile Photo with Valid Image
# ---------------------------------------------------------------------------

def test_update_profile_photo_success(playwright: Playwright) -> None:
    browser, context, page = create_page(playwright)
    try:
        page.goto(f"{BASE_URL}/employee/documents")
        page.wait_for_timeout(1000)

        # Locate profile photo input in UserInfo header card
        profile_input = page.locator("#profilePhoto, input[name='profilePhoto']").first
        expect(profile_input).to_be_attached(timeout=10000)

        profile_input.set_input_files(VALID_IMAGE_PATH)
        page.wait_for_timeout(1500)

        _screenshot(page, "test_12_profile_photo_updated")

        # Verify success toast notification
        success_toast = page.get_by_text(re.compile("Profile image changed", re.I))
        expect(success_toast).to_be_visible(timeout=5000)
    finally:
        close_toast(page)
        context.close()
        browser.close()


# ---------------------------------------------------------------------------
# Negative Test Case: Reject Non-Image File for Profile Photo
# ---------------------------------------------------------------------------

@pytest.mark.xfail(
    reason="BUG: Application accepts non-image file formats (.txt) for Profile Photo upload without validating image file type"
)
def test_update_profile_photo_invalid_file_type_rejected(
    playwright: Playwright,
) -> None:
    browser, context, page = create_page(playwright)
    try:
        page.goto(f"{BASE_URL}/employee/documents")
        page.wait_for_timeout(1000)

        profile_input = page.locator("#profilePhoto, input[name='profilePhoto']").first
        expect(profile_input).to_be_attached(timeout=10000)

        profile_input.set_input_files(INVALID_FILE_PATH)
        page.wait_for_timeout(1500)

        _screenshot(page, "test_12_profile_photo_invalid_file_type")

        # Assert that "Profile image changed" DOES NOT appear for a text file
        success_toast = page.get_by_text(re.compile("Profile image changed", re.I))
        assert success_toast.count() == 0, (
            "Application accepted a non-image text file (.txt) as profile photo and displayed 'Profile image changed'. "
            "Expected non-image profile photo uploads to be rejected."
        )

        # Assert that error toast or message appears
        error_message = page.get_by_text(
            re.compile("failed|invalid|unsupported|image|error", re.I)
        )
        assert error_message.count() > 0, (
            "Expected an error message when uploading a non-image file as profile photo."
        )
    finally:
        close_toast(page)
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_update_profile_photo_success(playwright)
        test_update_profile_photo_invalid_file_type_rejected(playwright)
