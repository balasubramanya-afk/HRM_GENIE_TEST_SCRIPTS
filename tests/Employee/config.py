import random
import time
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page

SCREENSHOT_BASE = Path(__file__).parent / "screenshots"
LAST_EMPLOYEE_FILE = Path(__file__).parent / "last_created_employee.txt"

ROLE_CREDENTIALS = {
    "HR": ("hr@out-strive.com", "HR@dmin06"),
    "HR Manager": ("bhanuprakash.r@brilyant.com", "tzp0zm52jz8wia8bklctw"),
    "HR ASSISTANT": ("lasya.p@brilyant.com", "u02623ag9rf6cb8nhzhjn"),
    "CXO": ("kavya.tn@brilyant.com", "ztu1s8mb23rmwoeusk4ni"),
    "BUH": ("gattu.ashwitha@brilyant.com", "Ramesh@12345"),
    "Manager": ("VijayKumar.S@brilyant.com", "Ramesh@12345"),
    "Employee": ("chandrika.v@brilyant.com", "Ramesh@123"),
    "Employee2": ("narimeti.thrisha@brilyant.com", "Admin@123"),
}


def login_as(page: Page, role: str):
    """Helper to login as any of the defined roles."""
    if role not in ROLE_CREDENTIALS:
        raise ValueError(f"Unknown role: {role}")
    email, pwd = ROLE_CREDENTIALS[role]
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").fill(email)
    page.get_by_role("textbox", name="Enter password").fill(pwd)
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    print(f"Login successful as {role}")


def _screenshot(page: Page, name: str):
    SCREENSHOT_BASE.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=SCREENSHOT_BASE / f"{name}_{ts}.png", full_page=True)


def close_toast(page: Page):
    """Wait for a success/error toast to appear and dismiss it."""
    try:
        toast = page.locator("text=successfully").first
        toast.wait_for(state="visible", timeout=4000)
        try:
            page.locator("[role='status'] button, [role='alert'] button, .toast button").last.click(timeout=1000)
        except Exception:
            pass
        toast.wait_for(state="hidden", timeout=5000)
    except Exception:
        pass


def generate_unique_employee_data(base_name: str = "chandrika") -> dict:
    """Generate unique employee name, email, and phone for every test run.

    Returns a dict with keys: 'name', 'email', 'phone'.
    Example:
        name  → chandrika_48237
        email → chandrika_48237@yopmail.com
        phone → 8342917065
    """
    # 5-char suffix: last 4 digits of epoch + 1 random digit to avoid collisions
    suffix = str(int(time.time()))[-4:] + str(random.randint(0, 9))
    unique_name = f"{base_name}_{suffix}"
    email = f"{unique_name}@yopmail.com"
    # Random 10-digit Indian-style mobile (starts 7-9)
    phone = str(random.randint(7000000000, 9999999999))
    return {"name": unique_name, "email": email, "phone": phone}


def generate_edit_data() -> dict:
    """Generate random employee edit data for each run."""
    suffix = str(int(time.time()))[-4:] + str(random.randint(0, 9))
    
    genders = ["Male", "Female"]
    marital_statuses = ["Married", "Unmarried"]
    relationships = ["Father", "Mother", "Brother", "Sister", "Spouse"]
    
    return {
        "name": f"EditTest_{suffix}",
        "gender": random.choice(genders),
        "phone": str(random.randint(7000000000, 9999999999)),
        "marital_status": random.choice(marital_statuses),
        # Address fields
        "address_street": f"Street_{suffix}",
        "address_pincode": str(random.randint(100000, 999999)),
        # Emergency contact
        "emergency_name": f"Contact_{suffix}",
        "emergency_phone": str(random.randint(7000000000, 9999999999)),
        "emergency_relation": random.choice(relationships),
    }



def save_last_employee(name: str) -> None:
    """Persist the last-created employee name so downstream tests can pick it up."""
    LAST_EMPLOYEE_FILE.write_text(name, encoding="utf-8")


def load_last_employee() -> str:
    """Read the employee name saved by the most recent create test."""
    if not LAST_EMPLOYEE_FILE.exists():
        raise FileNotFoundError(
            f"{LAST_EMPLOYEE_FILE} not found. Run test_03_create.py first."
        )
    return LAST_EMPLOYEE_FILE.read_text(encoding="utf-8").strip()
