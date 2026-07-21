from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page

SCREENSHOT_BASE = Path("screenshots") / "announcements"

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
    """Helper to login as any of the 7 roles."""
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