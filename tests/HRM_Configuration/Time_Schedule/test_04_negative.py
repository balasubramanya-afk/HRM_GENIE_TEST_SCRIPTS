
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_time_schedule
import re

def test_time_schedule_negative_scenarios(page):
    # ==========================================
    # Pre-requisite: Login and Navigate
    # ==========================================
    # Automatically accept any alerts or beforeunload dialogs (which block reloads)
    page.on("dialog", lambda dialog: dialog.accept())
    
    login_and_navigate_to_time_schedule(page, role="HR")
    page.wait_for_timeout(2000)
    
    # Ensure we are on the Shift tab
    page.get_by_role("button", name="Shift").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 1: Don't fill anything and click create
    # ==========================================
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(500)
    
    # Click Create inside the modal without filling fields
    page.get_by_role("button", name="Create").click()
    
    # Validation should prevent creation, modal should still be open
    page.wait_for_timeout(500)
    _screenshot(page, "test_04_negative_1_empty_create")
    
    # Close the modal using Cancel button
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Reset state to clear any stuck modals
    page.reload()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Shift").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 2: Fill everything and click cancel
    # ==========================================
    page.get_by_role("button", name="Create").click()
    page.get_by_placeholder("Enter the shift name").fill("Cancelled Shift")
    
    # Open dropdown and select a department
    page.get_by_label("Applicable Departments *").click()
    page.get_by_role("option").nth(1).click()
    
    # Click outside to close dropdown if needed (clicking the shift name field)
    page.get_by_placeholder("Enter the shift name").click()
    
    # Click some days
    page.get_by_label("Monday").click()
    page.get_by_label("Tuesday").click()
    
    # Click Close/Cancel to abort creation
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(1000)
    
    # Verify it is not created
    expect(page.get_by_text("Cancelled Shift")).not_to_be_visible()
    _screenshot(page, "test_04_negative_2_cancel_create")

    # ==========================================
    # Reset state to clear any stuck modals
    page.reload()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Shift").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 3: Create shift with a duplicate name
    # ==========================================
    with open("created_timeschedule.txt", "r") as f:
        shift_name = f.read().strip()
    
    # Try to create a new shift with the existing name
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(500)
    
    page.get_by_placeholder("Enter the shift name").fill(shift_name)
    page.get_by_label("Applicable Departments *").click()
    page.get_by_role("option").nth(1).click()
    page.get_by_placeholder("Enter the shift name").click()
    
    # Click create, validation should prevent it because the name exists
    page.get_by_role("button", name="Create").click()
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_04_negative_3_duplicate_name")
    
    # Cancel out of the modal
    page.get_by_role("button", name="Cancel").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Reset state to clear any stuck modals
    page.reload()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Shift").click()
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 4: Select > 40 hrs and verify warning message
    # ==========================================
    with open("created_timeschedule.txt", "r") as f:
        shift_name = f.read().strip()
    
    # Use JS to find the exact text node, walk up to its card, and click the first button (Edit).
    # This avoids the brittle xpath=../../.. pattern that can land on the wrong container.
    page.evaluate(f"""() => {{
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {{
            if (node.nodeValue.trim() === '{shift_name}') {{
                let el = node.parentElement;
                for (let i = 0; i < 8; i++) {{
                    el = el.parentElement;
                    if (!el) break;
                    const btn = el.querySelector('button');
                    if (btn) {{ btn.click(); break; }}
                }}
                break;
            }}
        }}
    }}""")
    page.wait_for_timeout(1000)
    
    # Scope all interactions to inside the Edit dialog to avoid matching background elements
    dialog = page.get_by_role("dialog")
    
    # Turn on ALL days that are currently off (inside the edit modal)
    # Switches have IDs like #day-Monday, #day-Tuesday, etc.
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        switch = dialog.locator(f"#day-{day}")
        if switch.get_attribute("aria-checked") != "true":
            switch.scroll_into_view_if_needed()
            switch.click()
            page.wait_for_timeout(200)
            
    # Click Update to submit (Edit modal uses "Update" not "Create")
    dialog.get_by_role("button", name="Update").click()
    page.wait_for_timeout(500)
    
    # Scroll the inner scrollable content area down to reveal the warning
    # The scrollable container has class 'overflow-y-auto' (confirmed from DOM inspection)
    dialog.locator(".overflow-y-auto").evaluate("el => el.scrollBy(0, 400)")
    page.wait_for_timeout(500)
    _screenshot(page, "test_04_negative_4_hours_warning")
    
    # Verify the warning message is visible (actual UI text says 40, not 45)
    expect(page.get_by_text("Total working hours per week cannot exceed 40 hours")).to_be_visible(timeout=5000)
    
    # Close the modal using Escape key (most reliable for Radix UI Sheet)
    page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # ==========================================
    # Reset state to clear any stuck modals
    page.reload()
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Shift").click()
    page.wait_for_timeout(1000)

    