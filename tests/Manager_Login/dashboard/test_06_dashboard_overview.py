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
    match = re.search(r"Total\s*(?:Employees|Records|Leaves|Check-Ins|Requests)?\s*:?\s*(\d+)", body_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return page.locator("tbody tr").count()

def test_dashboard_overview(page: Page):
    """6. Test dashboard quick metric links and verify data consistency."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    # 1. Leave Balance
    page.get_by_role("link", name=re.compile(r"Leave Balance")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/my-leave"))
    _screenshot(page, "test_06_overview_leave_balance")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Next Review
    page.get_by_role("link", name=re.compile(r"Next Review")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance"))
    _screenshot(page, "test_06_overview_next_review")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3. Pending Leave Requests
    plr_card_loc = page.locator("a, div").filter(has_text=re.compile(r"^Pending Leave Requests")).first
    plr_card_count = None
    if plr_card_loc.count() > 0:
        plr_text = plr_card_loc.inner_text()
        m = re.search(r"(\d+)", plr_text.replace("Pending Leave Requests", ""))
        plr_card_count = int(m.group(1)) if m else None

    page.get_by_role("link", name=re.compile(r"Pending Leave Requests")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/my-leave.*"))
    det_plr_count = extract_detailed_count(page)
    print(f"[Manager - Pending Leave Requests] Dashboard: {plr_card_count}, Detailed View: {det_plr_count}")
    _screenshot(page, "test_06_overview_pending_leave_requests")
    
    if plr_card_count is not None:
        assert plr_card_count == det_plr_count, (
            f"[Manager Dashboard - Pending Leave Requests] Data Inconsistency Discrepancy! "
            f"Dashboard count ({plr_card_count}) does not match Detailed View count ({det_plr_count})."
        )
        
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 4. Attendance Overview
    att_card_loc = page.locator("a, div").filter(has_text=re.compile(r"^Attendance Overview")).first
    att_card_count = None
    if att_card_loc.count() > 0:
        att_text = att_card_loc.inner_text()
        m = re.search(r"(\d+)", att_text.replace("Attendance Overview", ""))
        att_card_count = int(m.group(1)) if m else None

    page.get_by_role("link", name=re.compile(r"Attendance Overview")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/new-attendance/attendance-tracker-new.*"))
    det_att_count = extract_detailed_count(page)
    print(f"[Manager - Attendance Overview] Dashboard: {att_card_count}, Detailed View: {det_att_count}")
    _screenshot(page, "test_06_overview_attendance_overview")
    
    if att_card_count is not None:
        assert att_card_count == det_att_count, (
            f"[Manager Dashboard - Attendance Overview] Data Inconsistency Discrepancy! "
            f"Dashboard count ({att_card_count}) does not match Detailed View count ({det_att_count})."
        )

    page.go_back()
    page.wait_for_timeout(1000)

