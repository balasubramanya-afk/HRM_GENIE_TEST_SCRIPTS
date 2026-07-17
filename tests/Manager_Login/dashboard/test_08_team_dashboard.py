import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_team_dashboard(page: Page):
    """8. Test Team Dashboard widget, including Team Members, Pending Approvals, On Leave Today, and Pending Reviews."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    # Verify and click the main heading
    page.get_by_role("heading", name="Team Dashboard").click()
    
    # 1. Team members card
    page.get_by_role("link", name=re.compile(r"^Team members")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/team-employee"))
    _screenshot(page, "test_08_team_members")
    page.go_back()
    page.wait_for_timeout(1000)
    # 2. Pending Approvals card
    page.get_by_role("link", name=re.compile(r"^Pending Approvals")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(
        re.compile(r".*/employee/pending-approvals")
)

    expect(page.get_by_text("Leaves")).to_be_visible()
    expect(page.get_by_text("WFH")).to_be_visible()
    expect(page.get_by_text("OD")).to_be_visible()

    _screenshot(page, "test_08_pending_approvals")

    page.go_back()
    page.wait_for_timeout(1000)
    
    # 3. On Leave Today card
    page.get_by_role("link", name=re.compile(r"On Leave Today")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/team-leaves.*"))
    _screenshot(page, "test_08_on_leave_today")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # 4. Pending Reviews card
    page.get_by_role("link", name=re.compile(r"Pending Reviews")).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/internal-performance/review-team-member.*"))
    _screenshot(page, "test_08_pending_reviews")
    page.go_back()
    page.wait_for_timeout(1000)
