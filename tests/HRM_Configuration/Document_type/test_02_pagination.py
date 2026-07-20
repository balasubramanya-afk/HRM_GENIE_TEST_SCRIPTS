import re
import random
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_document_type

def test_pagination(page):
    login_and_navigate_to_document_type(page, role="HR")
    page.wait_for_timeout(3000)
    
    # ==========================================
    # PART 1: Test Navigation Arrows
    # ==========================================
    # Go to Page 2
    page.get_by_text("2", exact=True).click()
    page.wait_for_timeout(1000)
    
    # Go to Previous (Page 1)
    page.get_by_label("Go to previous page").click()
    page.wait_for_timeout(1000)
    
    # Go to Next (Page 2)
    page.get_by_label("Go to next page").click()
    page.wait_for_timeout(1000)
    
    # ==========================================
    # PART 2: Test Rows Per Page Dropdown
    # ==========================================
    # IMPORTANT: Go back to the FIRST page before changing the rows-per-page!
    page.get_by_text("1", exact=True).click()
    page.wait_for_timeout(1000)
    
    # Get the current value of the dropdown
    dropdown = page.locator("button").filter(has_text=re.compile(r"^\d+$")).first
    current_value = dropdown.inner_text().strip()
    
    # Click the dropdown to open it
    dropdown.click()
    page.wait_for_timeout(1000)
    
    # Get all available options
    options = page.get_by_role("option").all()
    if not options:
        options = page.locator("li").all()
        
    valid_options = [opt for opt in options if opt.inner_text().strip().isdigit()]
    
    # Pick a random option different from the current one
    different_options = [opt for opt in valid_options if opt.inner_text().strip() != current_value]
    
    if different_options:
        chosen_option = random.choice(different_options)
    else:
        chosen_option = random.choice(valid_options)
        
    target_value = chosen_option.inner_text().strip()
    
    # Select the randomly chosen value
    chosen_option.click()
    page.wait_for_timeout(2000)
    
    # Verify that the dropdown now displays the newly selected value
    expect(page.locator("button").filter(has_text=target_value).first).to_be_visible()
    
    # ==========================================
    # PART 3: Scroll & Screenshot
    # ==========================================
    # Forcefully scroll any internal scrollable containers to the absolute bottom
    # so the pagination controls are clearly visible in the screenshot
    page.evaluate("""
        const elements = document.querySelectorAll('*');
        for (const el of elements) {
            if (el.scrollHeight > el.clientHeight) {
                el.scrollTop = el.scrollHeight;
            }
        }
    """)
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_02_pagination")
