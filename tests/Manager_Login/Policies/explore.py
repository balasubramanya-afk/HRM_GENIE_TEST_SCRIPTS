from playwright.sync_api import sync_playwright
import re

def explore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://qa.hrmgenie.outstrive.co/login")
        page.get_by_placeholder("Enter email").click()
        page.get_by_placeholder("Enter email").fill("VijayKumar.S@brilyant.com")
        page.get_by_placeholder("Enter password").click()
        page.get_by_placeholder("Enter password").fill("Ramesh@12345")
        page.get_by_role("button", name="Login").click()
        
        page.wait_for_timeout(3000)
        page.locator("div").filter(has_text=re.compile(r"^Policies$")).locator("svg").first.click()
        
        page.wait_for_timeout(3000)
        
        # Try to find elements that look like policy titles
        print("--- Table Cells ---")
        cells = page.locator("td").all_inner_texts()
        for i, c in enumerate(cells[:15]):
            print(f"Cell {i}: {c}")
            
        print("--- Headings ---")
        headings = page.locator("h1, h2, h3, h4, h5, h6").all_inner_texts()
        for h in headings:
            print(h)
            
        browser.close()

explore()
