import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_leave_distribution_types(page):
    do_login(page)
    page.wait_for_load_state("networkidle")
    
    # Verify and interact with the leave type filters/distribution list at the bottom/side
    # e.g., Casual, Sick, Paid, LOP, Maternity, Paternity
    expect(page.get_by_text("Casual", exact=True)).to_be_visible()
    expect(page.get_by_text("Sick", exact=True)).to_be_visible()
    expect(page.get_by_text("Paid", exact=True)).to_be_visible()
    
    # Click to toggle/check details for a few distributions
    page.get_by_text("Casual", exact=True).first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "leave_casual_selected")
    
    # Navigate back to overview as clicking card redirects
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Sick", exact=True).first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "leave_sick_selected")
    
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")
    
    page.wait_for_timeout(2000)
