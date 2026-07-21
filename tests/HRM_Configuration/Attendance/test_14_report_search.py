import re
from playwright.sync_api import expect
from test_11_report_view import do_login_report
from config import _screenshot

def test_report_search(page):
    do_login_report(page)
    page.wait_for_load_state("networkidle")
    
    # Fill in the search box
    page.get_by_role("textbox", name="Search by name or email...").fill("Bhanu Prakash")
    # Click the search button/icon next to it
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.wait_for_load_state("networkidle")
    
    _screenshot(page, "report_searched_bhanu")
    
    # Reset search filter
    page.get_by_role("button", name="Reset Filters").first.click()
    page.wait_for_load_state("networkidle")
    
    page.wait_for_timeout(3000)
