import re
import pytest
from playwright.sync_api import Playwright, sync_playwright, expect
from config import login_as, navigate_to_organization_setup, _screenshot


def open_dropdown_and_select(page, combobox_filter, option_text):
    page.get_by_role("combobox").filter(has_text=combobox_filter).click()
    page.wait_for_timeout(1000)
    page.locator(
        f"[role='option']:has-text('{option_text}'), [data-radix-select-item]:has-text('{option_text}')"
    ).first.click(timeout=10000)

def get_date_combo(page):
    # Anchored to the "Date Format" label so it never matches the language
    # selector combobox in the top nav.
    return page.get_by_text("Date Format", exact=False).locator(
        "xpath=following::button[@role='combobox'][1]"
    )

def get_time_combo(page):
    return page.get_by_text("Time Format", exact=False).locator(
        "xpath=following::button[@role='combobox'][1]"
    )

def get_prefix_field(page):
    return page.get_by_role("textbox", name="Employee Prefix *")


@pytest.mark.xfail(
    reason="BUGS REPORTED: 1) System Settings read-only view displays raw format codes instead of human-readable labels. 2) Edit form does not reset to saved state on reopen after Discard."
)
def test_regional_settings(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_organization_setup(page)

    toggle = page.locator(
        "div:nth-child(3) > .flex.flex-col > .tracking-tight > .inline-flex"
    )

    # -------------------------------------------------------------------------
    # BUG CHECK #1: Verify read-only view does not display raw PHP format codes
    # (e.g. "d-m-Y", "g:i a", "H:i") instead of human-readable labels.
    # -------------------------------------------------------------------------
    readonly_card = page.locator("div:nth-child(3) > .flex.flex-col")
    readonly_text = readonly_card.inner_text()
    raw_code_patterns = [r"\bd-m-Y\b", r"\bm-d-Y\b", r"\bY-m-d\b", r"\bg:i\b", r"\bH:i\b", r"\bh:i\b"]
    has_raw_code = any(re.search(pat, readonly_text, re.IGNORECASE) for pat in raw_code_patterns)
    assert not has_raw_code, (
        f"BUG: System Settings read-only view displays raw format code in '{readonly_text}' "
        f"instead of human-readable label (e.g., 'DD-MM-YYYY (e.g., 31-12-2025)')."
    )

    # Open regional settings and capture the CURRENT saved values, whatever
    # they happen to be. This makes the test independent of any specific
    # hardcoded value like "DD-MM-YYYY" or "BITECOS", so it keeps working
    # even if the org's saved settings change in future.
    toggle.click()
    page.wait_for_timeout(1500)
    _screenshot(page, "test_04_regional_settings_open")

    original_date_format = get_date_combo(page).inner_text().strip()
    original_time_format = get_time_combo(page).inner_text().strip()
    original_prefix = get_prefix_field(page).input_value()

    # Pick a *different* value than the current one for date/time format,
    # so the edit is guaranteed to be a real change regardless of current state.
    date_options = ["DD-MM-YYYY (e.g., 31-12-2025)", "MM-DD-YYYY (e.g., 12-31-2025)"]
    new_date_format = next(o for o in date_options if o != original_date_format)

    time_options = ["12-hour (e.g., 1:30 pm)", "24-hour (e.g., 13:30)"]
    new_time_format = next(o for o in time_options if o != original_time_format)

    new_prefix = original_prefix + "X" if original_prefix else "TESTPFX"

    # Change date format, time format, employee prefix -> Discard
    get_date_combo(page).click()
    page.get_by_role("option", name=new_date_format).click()
    page.wait_for_timeout(2000)
    open_dropdown_and_select(page, original_time_format.split(" ")[0], new_time_format)
    get_prefix_field(page).click()
    get_prefix_field(page).fill(new_prefix)
    page.get_by_role("button", name="Discard").click()
    _screenshot(page, "test_04_regional_settings_discarded")

    # Verify original values persisted after discard (collapsed/read-only view)
    page.wait_for_timeout(1000)
    page.get_by_text(original_prefix, exact=True).click()

    # -------------------------------------------------------------------------
    # BUG CHECK #2: Re-open the edit form after discard and verify it reflects the
    # ORIGINAL captured values, not the values we typed before discarding.
    # -------------------------------------------------------------------------
    toggle.click()
    page.wait_for_timeout(1500)
    _screenshot(page, "test_04_regional_settings_reopened")

    date_combo_text = get_date_combo(page).inner_text().strip()
    time_combo_text = get_time_combo(page).inner_text().strip()
    prefix_value = get_prefix_field(page).input_value()

    assert date_combo_text == original_date_format, (
        f"BUG: Expected Date Format to revert to original saved value "
        f"'{original_date_format}' after Discard, but edit form shows "
        f"'{date_combo_text}' — edit form is not resetting to saved state "
        f"on reopen after Discard."
    )
    assert time_combo_text == original_time_format, (
        f"BUG: Expected Time Format to revert to original saved value "
        f"'{original_time_format}' after Discard, but edit form shows "
        f"'{time_combo_text}' — edit form is not resetting to saved state "
        f"on reopen after Discard."
    )
    assert prefix_value == original_prefix, (
        f"BUG: Expected Employee Prefix to revert to original saved value "
        f"'{original_prefix}' after Discard, but edit form shows "
        f"'{prefix_value}' — edit form is not resetting to saved state "
        f"on reopen after Discard."
    )

    # Edit and save (restore original values explicitly, confirming Save works)
    get_date_combo(page).click()
    page.get_by_role("option", name=original_date_format).click()
    page.wait_for_timeout(1000)
    open_dropdown_and_select(
        page, new_time_format.split(" ")[0], original_time_format
    )
    get_prefix_field(page).click()
    get_prefix_field(page).fill(original_prefix)
    page.get_by_role("button", name="Save").click()
    page.locator(".absolute.right-2").first.click()
    _screenshot(page, "test_04_regional_settings_saved")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_regional_settings(playwright)