import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_attendance_pagination(page):
    do_login(page)
    page.wait_for_load_state("networkidle")
    
    # Verify pagination elements (e.g. page numbers and totals)
    # 1. Click page 2 in the table pagination list
    page.get_by_text("2", exact=True).first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "attendance_page_2")
    
    # 2. Click page 3 in the table pagination list
    page.get_by_text("3", exact=True).first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "attendance_page_3")
    
    page.wait_for_timeout(2000)
