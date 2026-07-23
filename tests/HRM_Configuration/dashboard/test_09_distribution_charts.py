import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def extract_detailed_count(page: Page) -> int:
    """Helper to extract total entries / records from the target detailed page."""
    page.wait_for_timeout(1000)
    body_text = page.locator("body").inner_text()
    match = re.search(r"of\s+(\d+)\s+(?:entries|records|results)", body_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"Total\s*(?:Employees|Records|Leaves|Check-Ins)?\s*:?\s*(\d+)", body_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return page.locator("tbody tr").count()

def test_distribution_charts(page: Page):
    """9. Test Department Distribution charts and verify data consistency."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Department Distribution").click()
    
    departments = [
        "Services", "Shipment", "Logistics", "Marketing", "Networking",
        "Operations", "Presales", "Sales", "Finance", "AVSI",
        "IT Compute", "Administration", "UC", "Quality Assurance (QA)", "Testing"
    ]
    
    for dept in departments:
        page.get_by_role("heading", name="Department Distribution").scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        
        loc = page.get_by_text(dept, exact=True)
        if loc.count() == 0:
            loc = page.get_by_text(dept)
            
        if loc.count() > 0 and loc.first.is_visible():
            # Extract card summary count e.g. "Services 2 (3.77%)"
            try:
                parent_text = loc.first.locator("xpath=./ancestor::div[contains(@class, 'flex') or contains(@class, 'justify')][1]").inner_text()
                m = re.search(r"(\d+)\s*\([0-9\.]+\%\)", parent_text)
                card_count = int(m.group(1)) if m else None
            except Exception:
                card_count = None

            loc.first.click()
            page.wait_for_timeout(1000)
            expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
            
            detailed_count = extract_detailed_count(page)
            print(f"[Department Distribution - {dept}] Dashboard Count: {card_count}, Detailed View: {detailed_count}")
            
            screenshot_name = f"test_09_dept_{dept.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
            _screenshot(page, screenshot_name)
            
            if card_count is not None:
                assert card_count == detailed_count, (
                    f"[Department Distribution - {dept}] Data Inconsistency Discrepancy! "
                    f"Dashboard card count ({card_count}) does not match Detailed View count ({detailed_count})."
                )
            
            page.go_back()
            page.wait_for_timeout(1000)

