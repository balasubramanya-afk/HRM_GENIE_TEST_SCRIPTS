import time
import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_time_schedule

def test_create_time_schedule(page):
    # ==========================================
    # PART 1: HR Creates Time Schedule (Shift)
    # ==========================================
    login_and_navigate_to_time_schedule(page, role="HR")
    page.wait_for_timeout(3000)
    
    unique_suffix = str(int(time.time()))
    shift_name = f"Sample_{unique_suffix}"
    
    with open("created_timeschedule.txt", "w") as f:
        f.write(shift_name)
    
    # Dump HTML for debugging
    with open("page_html.txt", "w") as f:
        f.write(page.content())
        
    # --- Create Shift ---
    page.get_by_role("main").get_by_role("button", name="Shift").click()
    page.get_by_role("textbox", name="Shift *").click()
    page.get_by_role("textbox", name="Shift *").fill(shift_name)
    page.get_by_role("combobox").click()
    page.get_by_role("option", name="30 Min").click()
    
    page.get_by_role("button", name="Applicable Departments *").click()
    page.locator("div").filter(has_text=re.compile(r"^Services\(0\)$")).nth(1).click()
    page.get_by_role("button", name="Applicable Departments *").click()
    
    page.get_by_role("switch", name="Wednesday").click()
    page.get_by_role("switch", name="Saturday").click()
    
    page.get_by_role("button", name="17:").nth(4).click()
    page.get_by_role("combobox").filter(has_text="17").click()
    page.wait_for_timeout(3000)
    page.get_by_role("option", name="12").click()
    page.get_by_role("button", name="Create").click()
    
    page.wait_for_timeout(2000)
    _screenshot(page, "test_02_create")
    
    # Save the dynamically created name to a text file for subsequent tests
    with open("created_timeschedule.txt", "w") as f:
        f.write(shift_name)
