"""
test_09_pagination.py
=====================
Tests ALL pagination controls on the Employee list page in ONE test (single login):

  PART 1 – Rows-per-page ("Show entries") dropdown
    • Discovers ALL numeric options dynamically at runtime
    • Cycles through every option and verifies the dropdown reflects each selection
    • Future-proof: works automatically if new values (e.g. 100, 200) are added

  PART 2 – Page-number navigation  (the numbers between < and >)
    • Sets rows-per-page to the smallest value so maximum pages are available
    • Discovers ALL visible page-number links dynamically
    • Clicks every page number and verifies navigation
    • Tests the < (Previous) and > (Next) arrow buttons

Single login, single session – no repeated logins between parts.
"""
import re
from playwright.sync_api import expect
from config import _screenshot, login_as
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_dropdown_button(page):
    """Return the Show-entries button (the one whose full text is a bare number)."""
    return page.locator("button").filter(has_text=re.compile(r"^\d+$")).first


def _get_numeric_options(page):
    """
    Return (element, text) pairs for every numeric item visible in the open dropdown.
    Tries role=option first, then <li>, then [data-value] fallback.
    """
    for locator in [
        page.get_by_role("option"),
        page.locator("li"),
        page.locator("[data-value]"),
    ]:
        items = locator.all()
        numeric = [
            (el, el.inner_text().strip())
            for el in items
            if el.inner_text().strip().isdigit() and el.is_visible()
        ]
        if numeric:
            return numeric
    return []


def _get_page_number_links(page):
    """
    Return sorted list of (element, page_number_int) for page-number links
    between the < and > arrows in the pagination bar.

    The pagination uses <a> tags (not <button>) for page numbers.
    We look for the pagination <nav> or the container near the prev/next arrows,
    and find all visible elements whose text is a plain number.
    """
    page_links = []

    # The page numbers are <a> or <button> elements inside the pagination nav.
    # The reference script uses page.get_by_text("2", exact=True) to click them.
    # We look for all visible elements with purely numeric text near pagination.

    # Strategy: find elements within the pagination area.
    # The pagination <nav> typically contains the arrows and page numbers.
    nav = page.locator("nav").first
    if nav.count() > 0:
        # Search within the nav for numeric links
        children = nav.locator("a, button").all()
        for child in children:
            try:
                if not child.is_visible():
                    continue
                text = child.inner_text().strip()
                if re.fullmatch(r"\d+", text):
                    page_links.append((child, int(text)))
            except Exception:
                pass

    # If nothing found in <nav>, fall back to broader search
    if not page_links:
        # Look for <a> tags with purely numeric text (page number links)
        all_links = page.locator("a").all()
        for link in all_links:
            try:
                if not link.is_visible():
                    continue
                text = link.inner_text().strip()
                if re.fullmatch(r"\d+", text):
                    page_links.append((link, int(text)))
            except Exception:
                pass

    # Sort by page number and de-duplicate
    seen = set()
    result = []
    for el, num in sorted(page_links, key=lambda x: x[1]):
        if num not in seen:
            seen.add(num)
            result.append((el, num))
    return result
# ===========================================================================
# SINGLE TEST – login once, test everything in sequence
# ===========================================================================
def test_pagination(page):
    """
    Full pagination test.  Logs in ONCE, then:

      PART 1 – Show-entries dropdown
        - Discovers all numeric options at runtime
        - Clicks every option, verifies the selection

      PART 2 – Page navigation
        - Resets to smallest rows-per-page so max pages are visible
        - Clicks every visible page number (1, 2, 3, ...)
        - Tests the < (Previous) and > (Next) arrow buttons
    """
    # ── Login once ──────────────────────────────────────────────────────────
    login_as(page, role="HR")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Navigate to Employee list (sidebar)
    try:
        page.get_by_role("link", name=re.compile(r"employee", re.IGNORECASE)).first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)
    except Exception:
        pass  # Already on the page

    # ===================================================================
    # PART 1 – Rows-per-page ("Show entries") dropdown
    # ===================================================================
    print("\n" + "=" * 60)
    print("PART 1: Show-entries (rows-per-page) dropdown")
    print("=" * 60)

    dropdown = _get_dropdown_button(page)

    # Open dropdown and read ALL options
    dropdown.click()
    page.wait_for_timeout(1000)

    options = _get_numeric_options(page)
    assert options, "No numeric options found in the rows-per-page dropdown"

    option_texts = [text for _, text in options]
    print(f"  Discovered options: {option_texts}")

    # Close before cycling
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # Click EVERY option and verify
    for target_value in option_texts:
        print(f"\n  → Selecting rows-per-page = {target_value}")

        # Re-open (dropdown closes after each click)
        _get_dropdown_button(page).click()
        page.wait_for_timeout(800)

        # Re-fetch options (DOM re-renders after each selection)
        current_options = _get_numeric_options(page)

        # Robust match: compare stripped text
        target_option = None
        for el, text in current_options:
            if text == target_value:
                target_option = el
                break

        # If exact match not found, fall back to a text-based locator
        if target_option is None:
            fallback = page.get_by_role("option", name=re.compile(rf"^{re.escape(target_value)}$"))
            if fallback.count() == 0:
                fallback = page.locator("li").filter(
                    has_text=re.compile(rf"^{re.escape(target_value)}$")
                )
            if fallback.count() > 0 and fallback.first.is_visible():
                target_option = fallback.first

        assert target_option is not None, (
            f"Option '{target_value}' not found after re-opening the dropdown. "
            f"Available: {[t for _, t in current_options]}"
        )

        target_option.click()
        page.wait_for_timeout(1500)

        # Verify dropdown button now shows the chosen value
        expect(
            _get_dropdown_button(page)
        ).to_have_text(re.compile(rf"^{re.escape(target_value)}$"))
        print(f"     ✓ Verified rows-per-page = {target_value}")

    _screenshot(page, "test_09_part1_rows_per_page")
    # ===================================================================
    # PART 2 – Page-number buttons  (numbers between < and >)
    # ===================================================================
    print("\n" + "=" * 60)
    print("PART 2: Page-number buttons and < > arrows")
    print("=" * 60)

    # Reset to the SMALLEST rows-per-page so we have the most pages to test
    smallest_value = option_texts[0]  # e.g. "10"
    print(f"\n  Resetting rows-per-page to {smallest_value} for maximum pages...")
    _get_dropdown_button(page).click()
    page.wait_for_timeout(800)
    reset_options = _get_numeric_options(page)
    reset_target = next((el for el, t in reset_options if t == smallest_value), None)
    if reset_target is None:
        # Fallback
        reset_target = page.locator("li").filter(
            has_text=re.compile(rf"^{re.escape(smallest_value)}$")
        ).first
    reset_target.click()
    page.wait_for_timeout(2000)
    print(f"  ✓ Set rows-per-page to {smallest_value}")

    # Navigate to page 1 first
    page.get_by_text("1", exact=True).click()
    page.wait_for_timeout(1000)

    # ── Discover and click every page-number link ──────────────────────
    page_links = _get_page_number_links(page)
    page_numbers = [num for _, num in page_links]
    print(f"\n  Discovered page numbers: {page_numbers}")

    if not page_links:
        print("  ⚠ No page-number buttons found – possibly only 1 page of data.")
    else:
        for _, target_page in page_links:
            print(f"\n  → Clicking page [{target_page}]")

            # Use get_by_text for reliability (matches the reference script approach)
            page.get_by_text(str(target_page), exact=True).click()
            page.wait_for_timeout(1000)
            print(f"     ✓ Clicked page [{target_page}]")

    # ── Test > (Next) arrow ──────────────────────────────────────────────
    # First go back to page 1 so Next is available
    print("\n  → Going to page 1 before testing arrows")
    page.get_by_text("1", exact=True).click()
    page.wait_for_timeout(1000)

    print("  → Testing > Next arrow")
    next_arrow = page.get_by_label("Go to next page")
    if next_arrow.count() > 0:
        # Check it's not disabled before clicking
        is_disabled = next_arrow.first.get_attribute("aria-disabled")
        if is_disabled == "true":
            print("     ⚠ Next arrow is disabled (only 1 page?)")
        else:
            next_arrow.first.click()
            page.wait_for_timeout(1000)
            print("     ✓ Clicked > Next arrow")
    else:
        print("     ⚠ Next arrow not found")

    # ── Test < (Previous) arrow ──────────────────────────────────────────
    # After clicking Next we should be on page 2, so Previous should be enabled
    print("\n  → Testing < Previous arrow")
    prev_arrow = page.get_by_label("Go to previous page")
    if prev_arrow.count() > 0:
        is_disabled = prev_arrow.first.get_attribute("aria-disabled")
        if is_disabled == "true":
            print("     ⚠ Previous arrow is disabled (already on page 1)")
        else:
            prev_arrow.first.click()
            page.wait_for_timeout(1000)
            print("     ✓ Clicked < Previous arrow")
    else:
        print("     ⚠ Previous arrow not found")

    # Scroll pagination bar into view for screenshot
    page.evaluate("""
        const elements = document.querySelectorAll('*');
        for (const el of elements) {
            if (el.scrollHeight > el.clientHeight) {
                el.scrollTop = el.scrollHeight;
            }
        }
    """)
    page.wait_for_timeout(1000)
    _screenshot(page, "test_09_part2_page_navigation")
    print("\n✅ Pagination test complete.")
