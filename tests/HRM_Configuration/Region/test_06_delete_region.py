import re
from playwright.sync_api import Playwright, sync_playwright, expect
from test_01_login import login, navigate_to_region
import os

def test_delete_region(playwright: Playwright) -> None:
    slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
    browser = playwright.chromium.launch(
        channel="chrome", 
        headless=False, 
        slow_mo=slow_mo, 
        args=["--start-maximized"]
    )

    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    
    login(page)
    navigate_to_region(page)
    page.locator(".inline-flex.items-center.justify-center.gap-2.whitespace-nowrap.text-sm.font-medium.transition-colors.focus-visible\\:outline-none.focus-visible\\:ring-1.focus-visible\\:ring-ring.disabled\\:pointer-events-none.disabled\\:opacity-50.\\[\\&_svg\\]\\:pointer-events-none.\\[\\&_svg\\]\\:size-4.\\[\\&_svg\\]\\:shrink-0.bg-\\[\\#FFEDECB2\\]\\/70").first.click()
    page.get_by_role("button", name="Delete").click()
    page.locator(".absolute.right-2").click()
    page.close()

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_delete_region(playwright)
