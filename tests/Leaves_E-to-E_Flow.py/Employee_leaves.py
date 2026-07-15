import re
from datetime import date, timedelta
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    def select_next_available_date(start_offset: int = 0, max_lookahead: int = 365) -> bool:
        def ordinal(n: int) -> str:
            if 10 <= n % 100 <= 20:
                return 'th'
            return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

        def first_of_next_month(d: date) -> date:
            if d.month == 12:
                return date(d.year + 1, 1, 1)
            return date(d.year, d.month + 1, 1)

        # Try month by month, for each month scan valid days and prefer future dates
        start_date = date.today() + timedelta(days=start_offset)
        months_tried = 0
        next_selectors = [
            'button[aria-label="Next month"]',
            'button[aria-label="next month"]',
            'button[title="Next month"]',
            'button:has-text("Next")',
            'button:has-text(">")',
        ]
        current_month_date = date(start_date.year, start_date.month, 1)
        while months_tried < 24:
            month_name = current_month_date.strftime('%B')
            # scan valid days in this month
            for day in range(1, 32):
                try:
                    candidate = date(current_month_date.year, current_month_date.month, day)
                except ValueError:
                    continue
                # skip past dates
                if candidate < start_date:
                    continue
                suf = ordinal(day)
                # match month+day (ignoring weekday and optional year)
                pattern = re.compile(fr"{month_name}\s+{day}{suf}", re.IGNORECASE)
                locator = page.get_by_role("button", name=pattern)
                try:
                    if locator.count():
                        el = locator.first
                        if el.is_enabled() and el.is_visible():
                            el.click()
                            return True
                except Exception:
                    # ignore and continue scanning days
                    pass

            # navigate to next month if all days in this month are unavailable
            clicked = False
            for sel in next_selectors:
                els = page.locator(sel)
                if els.count():
                    try:
                        els.first.click()
                        clicked = True
                        break
                    except Exception:
                        continue
            if not clicked:
                break
            months_tried += 1
            current_month_date = first_of_next_month(current_month_date)

        return False
    def close_open_dialogs(timeout: int = 3000) -> None:
        try:
            # Close any open dialogs by clicking visible Close buttons until none remain
            while page.locator("div[role='dialog']").count():
                close_btns = page.get_by_role("button", name="Close")
                if close_btns.count():
                    try:
                        close_btns.first.click()
                        page.locator("div[role='dialog']").first.wait_for(state="hidden", timeout=timeout)
                    except Exception:
                        break
                else:
                    break
        except Exception:
            return
    def get_picker_button(label: str):
        # try several locator strategies to find the picker button
        candidates = [
            page.get_by_role("button", name=label),
            page.locator(f'button:has-text("{label}")'),
            page.locator('button[id="date"]'),
            page.locator('button[id^="date"]'),
            page.locator('button[aria-label*="date"]'),
        ]
        for loc in candidates:
            try:
                if loc.count():
                    return loc.first
            except Exception:
                continue
        # fallback to the role-based locator (may raise on wait)
        return page.get_by_role("button", name=label)
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("Ramesh.mali@brilyant.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("Ramesh@12345")
    page.get_by_role("button", name="Login").click()
    page.locator("div").filter(has_text=re.compile(r"^Leaves$")).click()
    page.get_by_role("button", name="Apply Leave").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Casual Leave").click()
    
    start_btn = get_picker_button("Pick start date")
    start_btn.wait_for(state="visible", timeout=10000)
    start_btn.click()
    select_next_available_date(0)
    page.wait_for_timeout(500)
    end_btn = get_picker_button("Pick end date")
    try:
        end_btn.wait_for(state="visible", timeout=10000)
        end_btn.click()
    except Exception:
        page.locator('button:has-text("Pick end date")').first.click()
    select_next_available_date(0)
    page.get_by_placeholder("Describe your reason").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing")
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="Apply Leave").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Sick Leave").click()
    
    start_btn = get_picker_button("Pick start date")
    start_btn.wait_for(state="visible", timeout=10000)
    start_btn.click()
    select_next_available_date(1)
    page.wait_for_timeout(500)
    end_btn = get_picker_button("Pick end date")
    try:
        end_btn.wait_for(state="visible", timeout=10000)
        end_btn.click()
    except Exception:
        page.locator('button:has-text("Pick end date")').first.click()
    select_next_available_date(1)
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing")
    page.get_by_role("radio", name="Half Day").click()
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="Apply Leave").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Paid Leave").click()
    
    start_btn = get_picker_button("Pick start date")
    start_btn.wait_for(state="visible", timeout=10000)
    start_btn.click()
    select_next_available_date(2)
    page.wait_for_timeout(500)
    end_btn = get_picker_button("Pick end date")
    try:
        end_btn.wait_for(state="visible", timeout=10000)
        end_btn.click()
    except Exception:
        page.locator('button:has-text("Pick end date")').first.click()
    select_next_available_date(2)
    page.get_by_role("radio", name="Half Day").click()
    page.get_by_role("radio", name="Second Half").click()
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing")
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="-07-2026 to 31-07-2026").click()
    page.get_by_role("button", name="Monday, June 1st,").click()
    page.get_by_role("button", name="Thursday, July 30th, 2026,").click()
    page.locator("button").filter(has_text="-06-2026 to 30-07-2026").click()
    page.locator("button").filter(has_text="All Type").click()
    page.get_by_label("Paternity Leave").get_by_text("Paternity Leave").click()
    page.get_by_role("combobox").filter(has_text="Paternity Leave").click()
    page.get_by_role("option", name="Casual Leave").click()
    page.get_by_role("combobox").filter(has_text="Casual Leave").click()
    page.get_by_role("option", name="Sick Leave").click()
    page.get_by_role("combobox").filter(has_text="Sick Leave").click()
    page.get_by_role("option", name="Paid Leave").click()
    page.get_by_role("combobox").filter(has_text="All Status").click()
    page.get_by_role("option", name="Pending").click()
    page.get_by_role("combobox").filter(has_text="All Leave Type").click()
    page.get_by_label("Half Day").get_by_text("Half Day").click()
    page.get_by_role("combobox").filter(has_text="Half Day").click()
    page.get_by_role("option", name="Full Day").click()
    page.get_by_role("button", name="Reset Filters").click()
    
    page.get_by_role("combobox").filter(has_text="Full Day").click()
    page.get_by_text("All Leave Type").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.rounded-xl.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.h-9.w-9.text-emerald-500").first.click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Sick Leave").click()
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing Testing")
    page.get_by_role("button", name="Apply").click()
    page.locator("tr:nth-child(2) > .p-2 > .flex > .inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.rounded-xl.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.h-9.w-9.text-emerald-500").click()
    #page.get_by_role("combobox", name="Select Leave Type*").click()
    #page.get_by_label("Select Leave Type*").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Casual Leave").click()
    page.get_by_role("radio", name="Second Half").click()
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing Testing")
    page.get_by_role("button", name="Apply").click()
    page.locator("tr:nth-child(3) > .p-2 > .flex > .inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.rounded-xl.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.h-9.w-9.text-emerald-500").click()
    page.get_by_role("combobox", name="Select Leave Type*").click()
    page.get_by_role("option", name="Paternity Leave").click()
    page.get_by_role("textbox", name="Reason*").click()
    page.get_by_role("textbox", name="Reason*").fill("Testing Testing Testing")
    page.get_by_role("button", name="Apply").click()
    page.get_by_role("button", name="RA Online").click()
    page.get_by_role("menuitem", name="Log out").click()
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("ayushri.k@brilyant.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("91mo1aajk6rwxtgssc8d")
    page.get_by_role("button", name="Login").click()
    page.locator("div").filter(has_text=re.compile(r"^Leaves$")).click()
    page.get_by_role("button", name="Team Leaves").click()
    page.get_by_role("cell", name="1137").first.click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("textbox", name="Search by name or ID").click()
    page.get_by_role("textbox", name="Search by name or ID").fill("")
    page.get_by_role("button", name="-07-2026 to 31-07-2026").click()
    page.get_by_role("button", name="Monday, June 1st,").click()
    page.get_by_role("button", name="Thursday, July 30th, 2026,").click()
    page.locator("button").filter(has_text="All Type").click()
    page.get_by_label("Paternity Leave").get_by_text("Paternity Leave").click()
    page.get_by_role("combobox").filter(has_text="Paternity Leave").click()
    page.get_by_role("option", name="Paid Leave").click()
    page.get_by_role("combobox").filter(has_text="All Status").click()
    page.get_by_role("option", name="Pending").click()
    page.get_by_role("combobox").filter(has_text="All Leave Type").click()
    page.get_by_role("option", name="Half Day").click()
    page.get_by_role("combobox").filter(has_text="All Designation").click()
    page.get_by_text("Lead Developer").click()
    page.get_by_role("button", name="Reset Filters").click()
    page.get_by_role("combobox").filter(has_text="Half Day").click()
    page.get_by_text("All Leave Type").click()
    
    radix_btn = page.locator("[id=\"radix-:rfm:\"]")
    try:
        radix_btn.wait_for(state="visible", timeout=10000)
        radix_btn.click()
    except Exception:
        # fallback: attempt a direct click (may raise same error)
        radix_btn.click()
    page.get_by_role("menuitem", name="Approve").click()
    page.get_by_role("textbox", name="Reason").click()
    page.get_by_role("textbox", name="Reason").fill("approve")
    page.get_by_role("button", name="Approve").click()
    page.locator("[id=\"radix-:rij:\"]").click()
    page.get_by_role("menuitem", name="Reject").click()
    page.get_by_role("textbox", name="Reason").click()
    page.get_by_role("textbox", name="Reason").fill("Reject")
    page.get_by_role("button", name="Reject").click()
    page.get_by_role("row", name="Employee ID Employee Name").get_by_role("checkbox").click()
    page.get_by_role("button", name="Approve Selected (4)").click()
    page.get_by_role("textbox", name="Reason").click()
    page.get_by_role("textbox", name="Reason").fill("approve")
    page.get_by_role("button", name="Approve").click()
    page.locator(".absolute.right-2").click()
    page.get_by_role("button", name="AY Online").click()
    page.get_by_role("menuitem", name="Log out").click()
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("Ramesh.mali@brilyant.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("Ramesh@12345")
    page.get_by_role("button", name="Login").click()
    page.locator("div").filter(has_text=re.compile(r"^Leaves$")).click()
    page.get_by_role("cell", name="Testing Testing Testing").first.click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("cell", name="-07-2026").nth(2).click()
    page.get_by_role("button", name="Close").click()
    page.get_by_text("Not Applicable").nth(2).click()
    page.get_by_role("button", name="Close").click()
    page.get_by_text("-").nth(4).click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="RA Online").click()
    page.get_by_role("menuitem", name="Log out").click()
    page.get_by_role("textbox", name="Enter email").click()
    page.get_by_role("textbox", name="Enter email").fill("hr@out-strive.com")
    page.get_by_role("textbox", name="Enter password").click()
    page.get_by_role("textbox", name="Enter password").fill("HR@dmin06")
    page.get_by_role("button", name="Login").click()
    page.locator("div").filter(has_text=re.compile(r"^Leaves$")).click()
    page.get_by_role("textbox", name="Search by name or ID...").click()
    page.get_by_role("textbox", name="Search by name or ID...").fill("")
    page.get_by_text("RARamesh MaliRamesh.mali@").first.click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="OU Online").click()
    page.get_by_role("menuitem", name="Log out").click()

    

    # ---------------------
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)