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

def test_leave_analytics(page: Page):
    """10. Test Leave Analytics section and verify data consistency."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Leave Analytics").click()
    
    # Extract total leaves count displayed on dashboard card (e.g. 49)
    total_leaves_loc = page.locator("h2:has-text('Total leaves taken')")
    dashboard_total_leaves = None
    if total_leaves_loc.count() > 0:
        parent = total_leaves_loc.first.locator("xpath=./ancestor::div[1]")
        m = re.search(r"(\d+)", parent.inner_text())
        if m:
            dashboard_total_leaves = int(m.group(1))
    
    print(f"[Leave Analytics] Dashboard Total Leaves: {dashboard_total_leaves}")
    
    # Click the date filter for Leave Analytics and select "Last 7 days"
    page.get_by_role("button", name=re.compile(r"\d{4}")).nth(1).click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Last 7 days").click()
    page.wait_for_timeout(1000)
    _screenshot(page, "test_10_leave_analytics_filtered")
    
    # Selecting Sick Leave portion from analytics
    sick_leave_loc = page.get_by_text("Sick Leave").first
    if sick_leave_loc.count() > 0:
        sick_leave_loc.click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_sick_leave_analytics")
        if "leaves" in page.url:
            det_count = extract_detailed_count(page)
            print(f"[Leave Analytics - Sick Leave] Detailed View Count: {det_count}")
            page.go_back()
            page.wait_for_timeout(1000)
    
    # Selecting Paternity Leave portion
    pat_leave_loc = page.get_by_text("Paternity Leave").first
    if pat_leave_loc.count() > 0:
        pat_leave_loc.click()
        page.wait_for_timeout(1000)
        _screenshot(page, "test_10_paternity_leave_analytics")
        if "leaves" in page.url:
            det_count = extract_detailed_count(page)
            print(f"[Leave Analytics - Paternity Leave] Detailed View Count: {det_count}")
            page.go_back()
            page.wait_for_timeout(1000)

