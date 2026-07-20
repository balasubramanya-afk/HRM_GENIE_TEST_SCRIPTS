import re
from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page

BASE_URL = "https://qa.hrmgenie.outstrive.co/login"
SCREENSHOT_BASE = Path(__file__).parent / "screenshot"

ROLES = {
    "Manager": ("VijayKumar.S@brilyant.com", "Ramesh@12345"),
}


def login_and_navigate_to_certifications(page, role="Manager"):
    email, password = ROLES[role]
    page.goto(BASE_URL)
    page.get_by_placeholder("Enter email").click()
    page.get_by_placeholder("Enter email").fill(email)
    page.get_by_placeholder("Enter password").click()
    page.get_by_placeholder("Enter password").fill(password)
    page.get_by_role("button", name="Login").click()
    
    # Wait for dashboard to load and click Policies directly
    page.wait_for_timeout(3000)
    page.locator("div").filter(has_text=re.compile(r"^Certifications$")).locator("svg").first.click()
    
    # Fallback if svg click doesn't work:
    # page.get_by_role("button", name="Certifications").click()



def _screenshot(page: Page, name: str):
    SCREENSHOT_BASE.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    page.screenshot(path=SCREENSHOT_BASE / f"{name}_{ts}.png", full_page=True)
