import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot, generate_edit_data


def test_edit_first_employee(page: Page) -> None:
    # ── Generate dynamic data ────────────────────────────────────────────────
    edit_data = generate_edit_data()
    print(f"Editing employee with dynamic data: {edit_data}")

    # ── Login ───────────────────────────────────────────────────────────────
    login_as(page, "HR")

    # ── Navigate to All Employees ───────────────────────────────────────────
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")

    # ── Open first employee details & edit mode ──────────────────────────────
    # Click the eye/view action icon on the first row
    page.locator(".inline-flex.items-center.justify-center.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.hover\\:bg-accent.hover\\:text-accent-foreground.px-4.py-2.w-max").first.click()
    page.wait_for_load_state("networkidle")

    # Click the Edit button
    page.get_by_role("button", name="Edit").click()
    page.wait_for_load_state("networkidle")

    # =========================================================================
    # 1. Employee Details Section
    # =========================================================================
    print("Editing Employee Details...")
    # Click pencil icon for employee details (first one)
    page.locator(".p-2.text-gray-400").first.click()
    page.wait_for_timeout(1000)

    # Name
    page.get_by_role("textbox", name="Enter name").click()
    page.get_by_role("textbox", name="Enter name").fill(edit_data["name"])

    # Gender (1st combobox)
    page.locator("button[role='combobox']").nth(0).click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name=edit_data["gender"], exact=True).click()

    # Phone Number
    page.get_by_role("textbox", name="Enter phone number").click()
    page.get_by_role("textbox", name="Enter phone number").fill(edit_data["phone"])

    # Marital Status (2nd combobox)
    page.locator("button[role='combobox']").nth(1).click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name=edit_data["marital_status"], exact=True).click()

    # Department -> Finance (static requirement) (4th combobox)
    page.locator("button[role='combobox']").nth(3).click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name="Finance", exact=True).click()

    # Sub Department -> Finance Manager (static requirement) (5th combobox)
    page.locator("button[role='combobox']").nth(4).click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name="Finance Manager", exact=True).click()

    # Designation -> Finance Manager (static requirement) (6th combobox)
    page.locator("button[role='combobox']").nth(5).click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name="Finance Manager", exact=True).click()

    # Save Employee Details
    page.locator(".p-2.text-green-600").click()
    page.wait_for_timeout(1000)

    # =========================================================================
    # 2. Address Section
    # =========================================================================
    print("Editing Address Section...")
    # Click Address edit icon (the second pencil)
    page.locator(".p-2.text-gray-400").nth(1).click()
    page.wait_for_timeout(1000)

    # Street
    page.get_by_role("textbox").nth(1).click()
    page.get_by_role("textbox").nth(1).fill(edit_data["address_street"])

    # Country -> India (static requirement)
    page.locator("button").nth(25).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="India", exact=True).click()
    page.wait_for_timeout(500)

    # State -> Karnataka (defaulting to a valid state in India)
    page.locator("button").nth(26).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Karnataka", exact=True).click()
    page.wait_for_timeout(500)

    # City -> Bengaluru
    page.locator("button").nth(27).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Bengaluru", exact=True).click()
    page.wait_for_timeout(500)

    # Pincode
    page.get_by_role("textbox").nth(2).click()
    page.get_by_role("textbox").nth(2).fill(edit_data["address_pincode"])

    # Save Address
    page.locator(".p-2.text-green-600").click()
    page.wait_for_timeout(1000)

    # =========================================================================
    # 3. Emergency Contact Section
    # =========================================================================
    print("Editing Emergency Contact Section...")
    # Click Emergency Contact edit icon (the third pencil)
    page.locator(".p-2.text-gray-400").nth(2).click()
    page.wait_for_timeout(1000)

    # Emergency Contact Name
    page.get_by_role("textbox", name="Enter name").click()
    page.get_by_role("textbox", name="Enter name").fill(edit_data["emergency_name"])

    # Emergency Contact Phone
    page.get_by_role("textbox", name="Enter mobile number").click()
    page.get_by_role("textbox", name="Enter mobile number").fill(edit_data["emergency_phone"])

    # Relationship
    page.get_by_role("tabpanel", name="General").get_by_role("combobox").click()
    page.wait_for_timeout(500)
    page.get_by_role("option", name=edit_data["emergency_relation"], exact=True).click()

    # Save Emergency Contact
    page.locator(".p-2.text-green-600").click()
    page.wait_for_timeout(1000)

    # ── Final Verification & Screenshot ──────────────────────────────────────
    page.goto("https://qa.hrmgenie.outstrive.co/employee/all-employees")
    page.wait_for_load_state("networkidle")
    
    # Search for the updated employee name to verify
    page.get_by_role("textbox", name="Search by Name & ID").click()
    page.get_by_role("textbox", name="Search by Name & ID").fill(edit_data["name"])
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "05_employee_edit_success")
    print(f"Edit successful! Verified new name: {edit_data['name']}")
