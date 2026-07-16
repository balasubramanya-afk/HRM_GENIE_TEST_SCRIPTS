from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, get_picker_button, select_next_available_date, close_toast

def test_manager_can_apply_new_leave(page: Page):
    """Verify manager can see/apply for the new leave type (Similar to Employee)."""
    login_as(page, "Manager")
    updated_leave_name = "Automation Master Leave Updated"
    
    page.goto("https://qa.hrmgenie.outstrive.co/my-leave")
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Apply Leave").click()
    page.wait_for_timeout(1000)
    
    # Read initial balance from the modal
    balance_header = page.locator("h3").filter(has_text=updated_leave_name).first
    balance_header.wait_for(state="visible", timeout=5000)
    initial_balance_text = balance_header.locator("span").nth(1).inner_text()
    initial_balance = float(initial_balance_text)
    
    page.get_by_role("combobox", name="Select Leave Type*").click()
    
    # Select the newly created leave type
    page.get_by_role("option", name=updated_leave_name).click()
    
    # Pick start date
    start_btn = get_picker_button(page, "Pick start date")
    start_btn.wait_for(state="visible", timeout=10000)
    start_btn.click()
    select_next_available_date(page, 1)
    page.wait_for_timeout(500)
    
    # Pick end date
    end_btn = get_picker_button(page, "Pick end date")
    try:
        end_btn.wait_for(state="visible", timeout=5000)
        end_btn.click()
    except Exception:
        page.locator('button:has-text("Pick end date")').first.click()
    select_next_available_date(page, 1)
    
    # Optional: Select Full Day if the radio button is present
    try:
        if page.get_by_role("radio", name="Full Day").is_visible(timeout=1000):
            page.get_by_role("radio", name="Full Day").click()
    except Exception:
        pass
    
    # Enter Reason
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing new leave application by Manager")
    
    # Submit application
    page.get_by_role("button", name="Apply").click()
    close_toast(page)
    page.wait_for_timeout(1000) # Wait for modal to fully close and state to reset
    
    _screenshot(page, "test_11_manager_apply_leave")
    
    # Verify balance was deducted
    page.get_by_role("button", name="Apply Leave").click()
    page.wait_for_timeout(1000)
    
    balance_header.wait_for(state="visible", timeout=5000)
    new_balance_text = balance_header.locator("span").nth(1).inner_text()
    new_balance = float(new_balance_text)
    
    assert new_balance < initial_balance, f"Leave balance was not deducted! Initial: {initial_balance}, New: {new_balance}"
    
    page.keyboard.press("Escape")
