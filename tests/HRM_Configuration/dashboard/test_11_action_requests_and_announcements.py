import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_action_requests_and_announcements(page: Page):
    """11. Test Action Requests, Announcements, and Holidays with Dynamic Count Consistency Verification."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Action Request").click()
    
    # Dynamically capture Probation Reviews count displayed on the dashboard card
    probation_count_loc = page.locator("h3:has-text('Probation Reviews') + span")
    dashboard_probation_count = None
    if probation_count_loc.count() > 0:
        dashboard_probation_count = int(probation_count_loc.inner_text().strip())
        print(f"Captured Dashboard Probation Reviews Count: {dashboard_probation_count}")
    
    # Click on the Action Request 'Due' button using locator
    due_loc = page.locator("div").filter(has_text=re.compile(r"^Due$"))
    if due_loc.count() > 0:
        due_loc.first.click()
    else:
        page.get_by_role("button", name="Due").click()
    
    page.wait_for_timeout(1000)
    
    # If still on dashboard, click exact Due button
    if "all-employees" not in page.url:
        page.locator("button").filter(has_text=re.compile(r"^Due$")).first.click()
        page.wait_for_timeout(1000)

    # Verify navigation to detailed page
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_11_action_request_due")
    
    # Extract record count on detailed page
    body_text = page.locator("body").inner_text()
    match = re.search(r"of\s+(\d+)\s+entries", body_text, re.IGNORECASE)
    detailed_count = int(match.group(1)) if match else page.locator("tbody tr").count()
    print(f"Detailed View Record Count: {detailed_count}")
    
    # Assert data consistency between dashboard widget count and detailed view count
    if dashboard_probation_count is not None:
        print(f"Data Consistency Check - Dashboard: {dashboard_probation_count}, Detailed: {detailed_count}")
        assert dashboard_probation_count == detailed_count, (
            f"Data Inconsistency Discrepancy Found! "
            f"Dashboard Probation Reviews count ({dashboard_probation_count}) "
            f"does not match Detailed View record count ({detailed_count})."
        )
    
    page.go_back()
    page.wait_for_timeout(1000)
    
    # Click Announcements and Holidays
    page.get_by_role("heading", name=re.compile(r"^Announcements")).click()
    page.get_by_role("heading", name="Current Month Holidays").click()
    _screenshot(page, "test_11_announcements_and_holidays")


