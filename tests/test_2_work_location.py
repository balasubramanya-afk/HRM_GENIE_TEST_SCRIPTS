import re

from playwright.sync_api import expect
from pathlib import Path


def test_work_location_flow(logged_in_page) -> None:
    page = logged_in_page
    print("Prepare to record Work Location flow.")

    # Navigate to dashboard to ensure clean page state
    page.goto("https://qa.hrmgenie.outstrive.co/")
    page.wait_for_load_state("networkidle")
    
    page.locator("div").filter(has_text=re.compile(r"^HRM Configuration$")).click()
    page.get_by_role("button", name="Work Location").click()
    page.get_by_role("textbox", name="Search location, country,").click()
    page.get_by_role("textbox", name="Search location, country,").fill("Testing")
    page.locator(".lucide.lucide-search.absolute.right-3").click()
    page.get_by_role("combobox").filter(has_text="All Countries").click()
    page.locator("span").filter(has_text="Afghanistan").click()
    page.get_by_role("combobox").filter(has_text="Afghanistan").click()
    page.get_by_role("option", name="India").click()
    page.get_by_role("combobox").filter(has_text="India").click()
    page.get_by_text("United States").click()
    page.get_by_role("combobox").filter(has_text="All States").click()
    page.get_by_text("Baghlan").click()
    page.get_by_role("combobox").filter(has_text="Baghlan").click()
    page.get_by_text("Karnataka").click()
    page.get_by_role("combobox").filter(has_text="Karnataka").click()
    page.get_by_text("Alaska").click()
    page.get_by_role("combobox").filter(has_text="Alaska").click()
    page.get_by_text("All States").click()
    page.get_by_role("combobox").filter(has_text="All States").click()
    page.get_by_text("Andhra Pradesh").click()
    page.get_by_role("combobox").filter(has_text="Andhra Pradesh").click()
    page.get_by_text("Tamil Nadu").click()
    page.get_by_role("button", name="Reset Filters").click()
    page.get_by_role("button", name="Location", exact=True).click()
    page.get_by_role("button", name="Close").click()
    page.get_by_role("button", name="Location", exact=True).click()
    page.get_by_role("button", name="Cancel").click()
    page.get_by_role("button", name="Location", exact=True).click()
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()
    page.get_by_role("combobox", name="State *").click()
    page.wait_for_timeout(500)
    state_option = page.get_by_role("option", name="Maharastra")
    state_option.wait_for(state="visible", timeout=15000)
    state_option.click(force=True)
    page.get_by_role("textbox", name="Location *").click()
    page.get_by_role("textbox", name="Location *").fill("Quatarrr")
    page.get_by_role("textbox", name="Location Code *").click()
    page.get_by_role("textbox", name="Location Code *").fill("QTR10000")
    page.get_by_role("button", name="Create").click()
    page.locator(".absolute.right-2").click()
    page.get_by_role("button", name="Location", exact=True).click()
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()
    page.get_by_role("combobox", name="State *").click()
    page.get_by_label("Karnataka").get_by_text("Karnataka").click()
    page.get_by_role("textbox", name="Location *").click()
    page.get_by_role("textbox", name="Location *").fill("Bengaluaru")
    page.get_by_role("textbox", name="Location Code *").click()
    page.get_by_role("textbox", name="Location Code *").fill("Bengaluaru")
    page.get_by_role("button", name="Cancel").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#55C7900D\\]\\/5").first.click()
    page.get_by_role("textbox", name="Location *").click()
    page.get_by_role("textbox", name="Location *").fill("Quatarr")
    page.get_by_role("textbox", name="Location Code *").click()
    page.get_by_role("textbox", name="Location Code *").fill("QTR10000")
    page.get_by_role("button", name="Update").click()
    page.locator(".absolute.right-2").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#55C7900D\\]\\/5").first.click()
    page.get_by_role("combobox", name="State *").click()
    page.get_by_label("Karnataka").get_by_text("Karnataka").click()
    page.get_by_role("button", name="Update").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#FFEDECB2\\]\\/70").first.click()
    page.get_by_role("button", name="Cancel").click()
    page.locator(".absolute.right-2").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#FFEDECB2\\]\\/70").first.click()
    page.get_by_role("button", name="Close").click()
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#FFEDECB2\\]\\/70").first.click()
    page.get_by_role("button", name="Delete").click()
    page.locator(".absolute.right-2").click()
    page.locator(".relative.flex-1.rounded-full").click()
    page.locator(".relative.flex-1.rounded-full").click()
    page.locator(".relative.flex-1.rounded-full").click()
    page.locator(".flex.touch-none").click()
    # Dynamically click only available pagination pages
    for page_num in [2, 3, 4, 5]:
        page_button = page.get_by_text(str(page_num), exact=True)
        if page_button.count() > 0:  # Check if button exists
            page_button.click()
            page.wait_for_timeout(500)  # Small delay between clicks
        else:
            print(f"Pagination page {page_num} not available, skipping.")
    # Safely navigate pages only if buttons are enabled
    nav_buttons = [
        ("Go to previous page", 1),
        ("Go to next page", 1),
        ("Go to previous page", 3),
        ("Go to previous page", 1),
        ("Go to previous page", 1)
    ]
    for button_label, _ in nav_buttons:
        nav_btn = page.get_by_label(button_label)
        if nav_btn.count() > 0 and nav_btn.get_attribute("aria-disabled") != "true":
            nav_btn.click()
            page.wait_for_timeout(300)
        else:
            print(f"Navigation button '{button_label}' is disabled or not available, skipping.")
    # Safely click page size options if they exist
    page_sizes = ["10", "20", "30", "40"]
    for size in page_sizes:
        # Click the combobox to open dropdown
        combobox = page.get_by_role("combobox").filter(has_text=size)
        if combobox.count() > 0:
            combobox.click()
            page.wait_for_timeout(300)
        else:
            # Try to click the option directly if available
            option = page.get_by_text(size, exact=True)
            if option.count() > 0:
                option.click()
                page.wait_for_timeout(300)
            else:
                print(f"Page size option '{size}' not available, skipping.")
    page.get_by_role("main").click()
