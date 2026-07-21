import re
from playwright.sync_api import expect
from test_11_report_view import do_login_report
from config import _screenshot

def test_report_filters(page):
    do_login_report(page)
    
    # 1. Update date range filter
    # Match the date range button containing the word "to"
    page.get_by_role("button").filter(has_text=re.compile(r"\bto\b")).click()
    
    # Select dates from the calendar (forcing clicks since they can be overlapped by react-date-range styling)
    page.get_by_role("button", name="Monday, June 1st,").click(force=True)
    page.get_by_role("button", name="Friday, July 31st, 2026,").click(force=True)
    
    # Click outside to close date picker
    page.get_by_text("Employee Id").first.click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "report_filtered_by_date")
    
    # 2. Reset Filters
    page.get_by_role("button", name="Reset Filters").first.click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "report_filters_reset")
    
    page.wait_for_timeout(3000)
