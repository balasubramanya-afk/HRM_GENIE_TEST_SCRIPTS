import os
import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_time_schedule

def test_edit_time_schedule(page):
    # ==========================================
    # PART 1: HR Edits Time Schedule (Shift)
    # ==========================================
    login_and_navigate_to_time_schedule(page, role="HR")
    page.wait_for_timeout(3000)
    
    # Read the shift name
    if os.path.exists("created_timeschedule.txt"):
        with open("created_timeschedule.txt", "r") as f:
            shift_name = f.read().strip()
    else:
        shift_name = "Sample_Fallback"
        
    updated_shift_name = f"{shift_name}_Update"
    
    # Find the card with the shift name and click its Edit icon
    # Since the exact structure is a card containing the text, we can filter a div that contains the text
    # and then find the edit button within it.
    card = page.locator("div").filter(has_text=re.compile(f"^{shift_name}$")).locator("..").locator("..").locator("..")
    # Actually, Playwright's locator().filter(has_text=shift_name) on the card container works best.
    # The Edit button is the one with the green bg. We will filter the button by its class.
    # Alternatively, we can use `page.locator("div").filter(has_text=shift_name).locator("button").first.click()`
    # Let's use a simpler approach: get the button near the text.
    page.locator("div").filter(has_text=re.compile(f"^{shift_name}$")).locator("xpath=../../..").locator("button").first.click()

    page.get_by_role("textbox", name="Shift *").click()
    page.get_by_role("textbox", name="Shift *").fill(updated_shift_name)
    page.get_by_role("button", name="Update").click()
    page.wait_for_timeout(2000)
    
    # Click another element after update
    page.locator("div").filter(has_text=re.compile(f"^{updated_shift_name}$")).locator("xpath=../../..").locator("button").first.click()
    page.get_by_role("button", name="09:").nth(2).click()
    page.get_by_role("combobox").filter(has_text="09").click()
    page.get_by_role("option", name="10").click()
    page.get_by_role("button", name="Update").click()
    
    page.wait_for_timeout(2000)
    _screenshot(page, "test_03_edit")

    # Store the updated name for deletion
    with open("created_timeschedule.txt", "w") as f:
        f.write(updated_shift_name)
