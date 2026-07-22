from pathlib import Path
from datetime import datetime, date, timedelta
import re
from playwright.sync_api import Page

# Save screenshots in the 'screenshots' folder inside team_leaves
SCREENSHOT_BASE = Path(__file__).parent / "screenshots"

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
    """Helper to login as specified role."""
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
    """Save screenshot with timestamp."""
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

def get_picker_button(page: Page, label: str):
    """Find date picker button by label or locator candidates."""
    candidates = [
        page.get_by_role("button", name=label),
        page.locator(f'button:has-text("{label}")'),
        page.locator('button[id="date"]'),
        page.locator('button[id^="date"]'),
        page.locator('button[aria-label*="date"]'),
    ]
    for loc in candidates:
        try:
            if loc.count():
                return loc.first
        except Exception:
            continue
    return page.get_by_role("button", name=label)

def select_next_available_date(page: Page, start_offset: int = 0) -> bool:
    """Select the next available date in calendar popup."""
    def ordinal(n: int) -> str:
        if 10 <= n % 100 <= 20:
            return 'th'
        return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    def first_of_next_month(d: date) -> date:
        if d.month == 12:
            return date(d.year + 1, 1, 1)
        return date(d.year, d.month + 1, 1)

    start_date = date.today() + timedelta(days=start_offset)
    months_tried = 0
    next_selectors = [
        'button[aria-label="Next month"]',
        'button[aria-label="next month"]',
        'button[title="Next month"]',
        'button:has-text("Next")',
        'button:has-text(">")',
    ]
    current_month_date = date(start_date.year, start_date.month, 1)
    while months_tried < 24:
        month_name = current_month_date.strftime('%B')
        for day in range(1, 32):
            try:
                candidate = date(current_month_date.year, current_month_date.month, day)
            except ValueError:
                continue
            if candidate < start_date:
                continue
            suf = ordinal(day)
            pattern = re.compile(fr"{month_name}\s+{day}{suf}", re.IGNORECASE)
            locator = page.get_by_role("button", name=pattern)
            try:
                if locator.count():
                    el = locator.first
                    if el.is_enabled() and el.is_visible():
                        el.click()
                        return True
            except Exception:
                pass

        clicked = False
        for sel in next_selectors:
            els = page.locator(sel)
            if els.count():
                try:
                    els.first.click()
                    clicked = True
                    break
                except Exception:
                    continue
        if not clicked:
            break
        months_tried += 1
        current_month_date = first_of_next_month(current_month_date)

    return False
