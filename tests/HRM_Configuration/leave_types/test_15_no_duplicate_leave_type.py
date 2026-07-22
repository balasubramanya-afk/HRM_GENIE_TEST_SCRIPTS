import re
from playwright.sync_api import expect, Page
from .config import _screenshot, close_toast, login_as


def test_no_duplicate_leave_type(page: Page):
    """Create a leave type, then attempt to create the same again and verify
    the application shows an 'already exists' error (no duplicates allowed)."""
    login_as(page, "HR")

    # ── Navigate to Leave Types ──────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Leave Types").click()
    page.wait_for_timeout(2000)

    leave_name = "Test Leave Type"

    # ── Step 1: Create the leave type for the first time ─────────────────
    page.get_by_role("button", name="+Add Type").click()
    page.get_by_role("textbox", name="Leave *").fill(leave_name)
    page.get_by_role("combobox", name="Type *").click()
    page.get_by_role("option", name="Paid", exact=True).click()
    page.get_by_role("spinbutton", name="Days *").fill("10")
    page.get_by_role("spinbutton", name="Monthly *").fill("1")
    page.get_by_role("spinbutton", name="Half Year *").fill("5")
    page.get_by_role("button", name="Create").click()
    close_toast(page)
    page.wait_for_timeout(2000)

    # Verify the leave type was created successfully
    page.get_by_role("textbox", name="Search by leave type name...").fill(leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("cell", name=leave_name).first).to_be_visible()

    _screenshot(page, "test_15_duplicate_step1_created")

    # ── Step 2: Attempt to create the same leave type again ──────────────
    page.get_by_role("button", name="+Add Type").click()
    page.get_by_role("textbox", name="Leave *").fill(leave_name)
    page.get_by_role("combobox", name="Type *").click()
    page.get_by_role("option", name="Paid", exact=True).click()
    page.get_by_role("spinbutton", name="Days *").fill("10")
    page.get_by_role("spinbutton", name="Monthly *").fill("1")
    page.get_by_role("spinbutton", name="Half Year *").fill("5")
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(2000)

    # Verify the "already exists" error message is shown
    error_text = page.locator("text=A leave type with this name already exists")
    expect(error_text.first).to_be_visible()

    _screenshot(page, "test_15_duplicate_step2_error")

    # ── Step 3: Close the create modal / sheet ───────────────────────────
    # Press Escape or click the close button to dismiss the create form
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # ── Step 4: Cleanup – delete the leave type we created ───────────────
    page.get_by_role("textbox", name="Search by leave type name...").fill(leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)

    page.locator(".text-red-500").first.click()
    page.get_by_role("button", name="Delete").click()
    close_toast(page)
    page.wait_for_timeout(2000)

    # Verify the leave type has been deleted
    page.get_by_role("textbox", name="Search by leave type name...").fill(leave_name)
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_timeout(1000)
    expect(page.get_by_role("cell", name=leave_name)).not_to_be_visible()

    _screenshot(page, "test_15_duplicate_step3_cleanup")
