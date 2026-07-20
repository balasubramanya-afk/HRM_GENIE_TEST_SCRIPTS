from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_time_schedule

def test_login(page):
    login_and_navigate_to_time_schedule(page, role="HR")
    
    # Verify key elements are visible
    expect(page.get_by_role("heading", name="Shift Schedules")).to_be_visible()
    expect(page.get_by_text("Define and manage employee work shifts with ease")).to_be_visible()
    expect(page.get_by_role("button", name="+ Shift")).to_be_visible()
    
    # Wait for 3 seconds to let you see the page before it closes
    page.wait_for_timeout(3000)
    _screenshot(page, "test_01_login")
