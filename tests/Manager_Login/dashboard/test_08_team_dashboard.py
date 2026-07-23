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
    match = re.search(r"Total\s*(?:Employees|Records|Leaves|Check-Ins|Approvals)?\s*:?\s*(\d+)", body_text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return page.locator("tbody tr").count()

def test_team_dashboard(page: Page):
    """8. Test Team Dashboard widget metrics and verify data consistency."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Team Dashboard").click()
    
    # 1. Team members card
    tm_card_loc = page.locator("a, div").filter(has_text=re.compile(r"^Team members")).first
    tm_card_count = None
    if tm_card_loc.count() > 0:
        tm_text = tm_card_loc.inner_text()
        m = re.search(r"(\d+)", tm_text.replace("Team members", ""))
        tm_card_count = int(m.group(1)) if m else None

    page.get_by_role("link", name=re.compile(r"^Team members")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/team-employee"))
    det_tm_count = extract_detailed_count(page)
    print(f"[Team Dashboard - Team Members] Dashboard: {tm_card_count}, Detailed View: {det_tm_count}")
    _screenshot(page, "test_08_team_members")
    
    if tm_card_count is not None:
        assert tm_card_count == det_tm_count, (
            f"[Team Dashboard - Team Members] Data Inconsistency Discrepancy! "
            f"Dashboard count ({tm_card_count}) does not match Detailed View count ({det_tm_count})."
        )
        
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 2. Pending Approvals card
    pa_card_loc = page.locator("div, a").filter(has_text=re.compile(r"^Pending Approvals")).first
    pa_card_count = None
    breakdown_sum = None
    if pa_card_loc.count() > 0:
        pa_text = pa_card_loc.inner_text()
        m = re.search(r"^Pending Approvals\s*(\d+)", pa_text)
        pa_card_count = int(m.group(1)) if m else None
        
        # Parse breakdown text: e.g. "3 Leaves , 1 WFH , 2 OD"
        leaves_m = re.search(r"(\d+)\s*Leaves", pa_text)
        wfh_m = re.search(r"(\d+)\s*WFH", pa_text)
        od_m = re.search(r"(\d+)\s*OD", pa_text)
        if leaves_m and wfh_m and od_m:
            breakdown_sum = int(leaves_m.group(1)) + int(wfh_m.group(1)) + int(od_m.group(1))
            print(f"[Pending Approvals Breakdown] Summary Count: {pa_card_count}, Breakdown Sum ({leaves_m.group(1)}+{wfh_m.group(1)}+{od_m.group(1)}): {breakdown_sum}")

    # Check navigation if link exists
    pa_link = page.get_by_role("link", name=re.compile(r"Pending Approvals"))
    if pa_link.count() > 0 and pa_link.first.is_visible():
        pa_link.first.click()
        page.wait_for_timeout(1000)
        if "pending-approvals" in page.url:
            det_pa_count = extract_detailed_count(page)
            print(f"[Team Dashboard - Pending Approvals] Dashboard: {pa_card_count}, Detailed View: {det_pa_count}")
            _screenshot(page, "test_08_pending_approvals")
            if pa_card_count is not None:
                assert pa_card_count == det_pa_count, f"[Pending Approvals] Data Discrepancy: Dashboard ({pa_card_count}) != Detailed View ({det_pa_count})"
            page.go_back()
            page.wait_for_timeout(1000)
    else:
        _screenshot(page, "test_08_pending_approvals")
        if pa_card_count is not None and breakdown_sum is not None:
            assert pa_card_count == breakdown_sum, (
                f"[Pending Approvals] Data Inconsistency Discrepancy! "
                f"Dashboard summary count ({pa_card_count}) does not match breakdown sum ({breakdown_sum})."
            )

    
    # 3. On Leave Today card
    olt_card_loc = page.locator("a, div").filter(has_text=re.compile(r"^On Leave Today")).first
    olt_card_count = None
    if olt_card_loc.count() > 0:
        olt_text = olt_card_loc.inner_text()
        m = re.search(r"(\d+)", olt_text.replace("On Leave Today", ""))
        olt_card_count = int(m.group(1)) if m else None

    page.get_by_role("link", name=re.compile(r"On Leave Today")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/team-leaves.*"))
    det_olt_count = extract_detailed_count(page)
    print(f"[Team Dashboard - On Leave Today] Dashboard: {olt_card_count}, Detailed View: {det_olt_count}")
    _screenshot(page, "test_08_on_leave_today")
    
    if olt_card_count is not None:
        assert olt_card_count == det_olt_count, (
            f"[Team Dashboard - On Leave Today] Data Inconsistency Discrepancy! "
            f"Dashboard count ({olt_card_count}) does not match Detailed View count ({det_olt_count})."
        )
        
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 4. Pending Reviews card
    pr_card_loc = page.locator("a, div").filter(has_text=re.compile(r"^Pending Reviews")).first
    pr_card_count = None
    if pr_card_loc.count() > 0:
        pr_text = pr_card_loc.inner_text()
        m = re.search(r"(\d+)", pr_text.replace("Pending Reviews", ""))
        pr_card_count = int(m.group(1)) if m else None

    page.get_by_role("link", name=re.compile(r"Pending Reviews")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance/review-team-member.*"))
    det_pr_count = extract_detailed_count(page)
    print(f"[Team Dashboard - Pending Reviews] Dashboard: {pr_card_count}, Detailed View: {det_pr_count}")
    _screenshot(page, "test_08_pending_reviews")
    
    if pr_card_count is not None:
        assert pr_card_count == det_pr_count, (
            f"[Team Dashboard - Pending Reviews] Data Inconsistency Discrepancy! "
            f"Dashboard count ({pr_card_count}) does not match Detailed View count ({det_pr_count})."
        )
        
    page.go_back()
    page.wait_for_timeout(1000)

