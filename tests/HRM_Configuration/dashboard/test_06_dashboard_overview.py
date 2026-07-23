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

def test_dashboard_overview(page: Page):
    """6. Test dashboard quick metric links and verify summary data consistency."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    # 1. New Joinees
    nj_card_text = page.locator("a, div").filter(has_text=re.compile(r"^New Joinees")).first.inner_text()
    nj_match = re.search(r"(\d+)", nj_card_text.replace("New Joinees", ""))
    nj_dashboard_count = int(nj_match.group(1)) if nj_match else None
    
    page.get_by_role("link", name="New Joinees").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    nj_detailed_count = extract_detailed_count(page)
    print(f"[New Joinees] Dashboard: {nj_dashboard_count}, Detailed View: {nj_detailed_count}")
    _screenshot(page, "test_06_dashboard_overview_new_joinees")
    
    if nj_dashboard_count is not None:
        assert nj_dashboard_count == nj_detailed_count, f"[New Joinees] Data Inconsistency: Dashboard ({nj_dashboard_count}) != Detailed View ({nj_detailed_count})"
        
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Total check-Ins
    tc_card_text = page.locator("a, div").filter(has_text=re.compile(r"^Total check-Ins")).first.inner_text()
    tc_match = re.search(r"(\d+)", tc_card_text.replace("Total check-Ins", ""))
    tc_dashboard_count = int(tc_match.group(1)) if tc_match else None

    page.get_by_role("link", name="Total check-Ins").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/new-hr-attendance.*"))
    tc_detailed_count = extract_detailed_count(page)
    print(f"[Total Check-Ins] Dashboard: {tc_dashboard_count}, Detailed View: {tc_detailed_count}")
    _screenshot(page, "test_06_dashboard_overview_total_checkins")
    
    if tc_dashboard_count is not None:
        assert tc_dashboard_count == tc_detailed_count, f"[Total Check-Ins] Data Inconsistency: Dashboard ({tc_dashboard_count}) != Detailed View ({tc_detailed_count})"

    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3. Late check-Ins
    lc_card_text = page.locator("a, div").filter(has_text=re.compile(r"^Late check-Ins")).first.inner_text()
    lc_match = re.search(r"(\d+)", lc_card_text.replace("Late check-Ins", ""))
    lc_dashboard_count = int(lc_match.group(1)) if lc_match else None

    page.get_by_role("link", name="Late check-Ins").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/attendance-tracker-new.*"))
    lc_detailed_count = extract_detailed_count(page)
    print(f"[Late Check-Ins] Dashboard: {lc_dashboard_count}, Detailed View: {lc_detailed_count}")
    _screenshot(page, "test_06_dashboard_overview_late_checkins")
    
    if lc_dashboard_count is not None:
        assert lc_dashboard_count == lc_detailed_count, f"[Late Check-Ins] Data Inconsistency: Dashboard ({lc_dashboard_count}) != Detailed View ({lc_detailed_count})"

    page.go_back()
    page.wait_for_timeout(1000)
    
    # 4. On Leave
    ol_card_text = page.locator("a, div").filter(has_text=re.compile(r"^On Leave")).first.inner_text()
    ol_match = re.search(r"(\d+)", ol_card_text.replace("On Leave", ""))
    ol_dashboard_count = int(ol_match.group(1)) if ol_match else None

    page.get_by_role("link", name="On Leave").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/all-employees-leaves.*"))
    ol_detailed_count = extract_detailed_count(page)
    print(f"[On Leave] Dashboard: {ol_dashboard_count}, Detailed View: {ol_detailed_count}")
    _screenshot(page, "test_06_dashboard_overview_on_leave")
    
    if ol_dashboard_count is not None:
        assert ol_dashboard_count == ol_detailed_count, f"[On Leave] Data Inconsistency: Dashboard ({ol_dashboard_count}) != Detailed View ({ol_detailed_count})"

    page.go_back()
    page.wait_for_timeout(1000)

    
    # Click the date filter (matching the date range button) and select "Today"
    page.get_by_role("button", name=re.compile(r"\d{4}")).first.click()
    page.wait_for_timeout(500)
    page.get_by_role("button", name="Today", exact=True).click()
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_06_dashboard_overview_date_today")