import re
from playwright.sync_api import expect
from test_07_tracker_view import do_login_tracker
from config import _screenshot

def test_tracker_sorting(page):
    do_login_tracker(page)
    page.wait_for_load_state("networkidle")
    
    # Click Employee Id header to sort
    page.get_by_text("Employee Id").click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "tracker_sorted_by_emp_id")
    
    # Click Department header to sort
    page.get_by_text("Department").click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "tracker_sorted_by_dept")
    
    page.wait_for_timeout(3000)
