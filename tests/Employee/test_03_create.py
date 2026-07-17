import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page
from config import login_as, _screenshot, generate_unique_employee_data, save_last_employee

IMAGE_PATH = Path(__file__).parent / "images for testing1.jpg"


def test_create_employee(page: Page) -> None:
    # ── Generate unique data for this run ────────────────────────────────────
    emp = generate_unique_employee_data("chandrika")
    print(f"Creating employee: name={emp['name']}  email={emp['email']}  phone={emp['phone']}")

    # ── Login (same flow as test_01_login.py) ────────────────────────────────
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")

    # ── Open "Add New Employee" form ─────────────────────────────────────────
    page.get_by_role("button", name="Add New").click()

    # ── Upload profile photo ─────────────────────────────────────────────────
    page.locator(".lucide.lucide-camera").click()
    page.get_by_label("", exact=True).set_input_files(str(IMAGE_PATH))

    # ── Fill in employee details ─────────────────────────────────────────────
    page.get_by_role("textbox", name="Enter name").click()
    page.get_by_role("textbox", name="Enter name").fill(emp["name"])

    page.get_by_role("combobox").filter(has_text="Select Employee Type").click()
    page.get_by_label("Full Time").get_by_text("Full Time").click()

    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill(emp["email"])

    page.get_by_role("combobox").filter(has_text="Select Branch").click()
    page.get_by_label("Bangalore", exact=True).get_by_text("Bangalore").click()

    page.get_by_role("combobox").filter(has_text=re.compile(r"^Select Department$")).click()
    page.get_by_label("Logistics").get_by_text("Logistics").click()

    page.get_by_role("combobox").filter(has_text="Select Department First").click()
    page.get_by_label("Warehousing & Inventory").get_by_text("Warehousing & Inventory").click()

    page.get_by_role("combobox").filter(has_text=re.compile(r"^Select Designation$")).click()
    page.get_by_label("Warehouse Supervisor").get_by_text("Warehouse Supervisor").click()

    page.get_by_role("combobox").filter(has_text="Select Work Shift").click()
    page.get_by_label("Sample_Update_1784089023").get_by_text("Sample_Update_1784089023").click()

    # ── Date of Birth ────────────────────────────────────────────────────────
    page.get_by_role("button", name="Pick a date").first.click()
    page.get_by_role("button", name="July 2026").click()
    page.get_by_role("button", name="- 2032").click()
    page.get_by_role("button", name="July 2026").click()
    page.get_by_role("button", name="Go to the previous 12 years").click()
    page.get_by_role("button", name="Go to the previous 12 years").click()
    page.get_by_role("button", name="1998").click()
    page.get_by_role("button", name="Tuesday, January 6th,").click()

    # ── Joining Date ─────────────────────────────────────────────────────────
    page.get_by_role("button", name="Pick a date").click()
    page.get_by_role("button", name="Tuesday, July 14th,").click()

    # ── Gender ───────────────────────────────────────────────────────────────
    page.get_by_role("combobox").filter(has_text="Select Gender").click()
    page.get_by_role("textbox", name="Search gender...").click()
    page.get_by_role("textbox", name="Search gender...").fill("fema")
    page.get_by_role("option", name="Female").click()

    # ── Role ─────────────────────────────────────────────────────────────────
    page.get_by_role("combobox").filter(has_text="Select Role").click()
    page.get_by_role("textbox", name="Search roles...").click()
    page.get_by_role("textbox", name="Search roles...").fill("em")
    page.get_by_label("Employee").get_by_text("Employee", exact=True).click()

    # ── Manager ──────────────────────────────────────────────────────────────
    page.get_by_role("combobox").filter(has_text="Select Manager").click()
    page.get_by_label("Kavya TN").get_by_text("Kavya TN").click()

    # ── Phone ────────────────────────────────────────────────────────────────
    page.get_by_role("textbox", name="Enter phone").click()
    page.get_by_role("textbox", name="Enter phone").fill(emp["phone"])

    # ── Submit ───────────────────────────────────────────────────────────────
    page.get_by_role("button", name="Submit").click()
    page.wait_for_load_state("networkidle")

    # ── Save generated name for downstream tests (test_04, test_05) ──────────
    save_last_employee(emp["name"])
    print(f"Saved employee name to last_created_employee.txt: {emp['name']}")

    _screenshot(page, "03_create_employee")

    # ── Verify by searching the new employee ─────────────────────────────────
    page.get_by_role("textbox", name="Search by Name & ID").click()
    page.get_by_role("textbox", name="Search by Name & ID").fill(emp["name"])
    page.wait_for_load_state("networkidle")
    _screenshot(page, "03_create_employee_search")
