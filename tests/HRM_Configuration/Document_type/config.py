import re
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://qa.hrmgenie.outstrive.co/login"
SCREENSHOT_BASE = Path(__file__).parent / "screenshot"

ROLES = {
    "HR": ("hr@out-strive.com", "HR@dmin06"),
    "Employee": ("chandrika.v@brilyant.com", "Ramesh@123"),
}


def login_and_navigate_to_document_type(page, role="HR"):
    email, password = ROLES[role]
    page.goto(BASE_URL)
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill(email)
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill(password)
    page.get_by_role("button", name="Login").click()
    
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).get_by_role("button").click()
    page.get_by_role("button", name="Document Type").click()


def login_and_navigate_to_employee_documents(page, role="Employee"):
    email, password = ROLES[role]
    page.goto(BASE_URL)
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill(email)
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill(password)
    page.get_by_role("button", name="Login").click()
    
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="Documents").click()


def _screenshot(page: Page, name: str):
    SCREENSHOT_BASE.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=SCREENSHOT_BASE / f"{name}_{ts}.png", full_page=True)
