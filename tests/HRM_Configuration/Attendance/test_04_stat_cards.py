import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_interact_stat_cards(page):
    do_login(page)
    page.wait_for_load_state("networkidle")
    
    # Verify and interact with the summary metrics cards
    # We click them to expand/filter the list beneath them as recorded in sample.py
    
    # 1. Click Present card
    page.get_by_text("Present").first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "stats_present_selected")
    # Navigate back to overview as clicking card redirects
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")
    
    # 2. Click Total WFH card
    page.get_by_text("Total WFH").first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "stats_wfh_selected")
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")
    
    # 3. Click Total Leave card
    page.get_by_text("Total Leave").first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "stats_leave_selected")
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")

    # 4. Click Check In card
    page.get_by_text("Check In").first.click()
    page.wait_for_load_state("networkidle")
    _screenshot(page, "stats_check_in_selected")
    page.goto("https://qa.hrmgenie.outstrive.co/new-attendance/overview")
    page.wait_for_load_state("networkidle")
    
    page.wait_for_timeout(2000)
