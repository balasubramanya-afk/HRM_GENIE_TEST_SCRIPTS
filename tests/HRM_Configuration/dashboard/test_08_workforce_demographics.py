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

def test_workforce_demographics(page: Page):
    """8. Test Workforce Demographics charts and verify data consistency."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    # Extract Active Employees count upfront while on Dashboard
    dashboard_active_count = None
    active_emp_loc = page.locator("a, div").filter(has_text=re.compile(r"^Active Employees"))
    if active_emp_loc.count() > 0:
        active_emp_text = active_emp_loc.first.inner_text()
        active_match = re.search(r"(\d+)", active_emp_text.replace("Active Employees", ""))
        dashboard_active_count = int(active_match.group(1)) if active_match else None
        print(f"Captured Dashboard Active Employees Count: {dashboard_active_count}")

    page.get_by_role("heading", name="Workforce Demographics").click()
    
    # 1. Age Distribution - Group 1 (20-30)
    group1_loc = page.locator(".h-full.bg-primary-color").first
    if group1_loc.count() > 0:
        group1_loc.click()
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
        det_count = extract_detailed_count(page)
        print(f"[Workforce Demographics - Age 20-30] Detailed View Count: {det_count}")
        _screenshot(page, "test_08_demographics_chart_1")
        page.go_back()
        page.wait_for_timeout(1000)
    
    # 2. Gender Distribution Section
    page.get_by_role("heading", name="Gender Distribution").click()
    
    # Male
    male_loc = page.get_by_text("Male", exact=True)
    male_det_count = None
    if male_loc.count() > 0:
        male_loc.click()
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
        male_det_count = extract_detailed_count(page)
        print(f"[Gender Distribution - Male] Detailed View Count: {male_det_count}")
        _screenshot(page, "test_08_demographics_gender_male")
        page.go_back()
        page.wait_for_timeout(1000)
    
    # Female
    female_loc = page.get_by_text("Female", exact=True)
    female_det_count = None
    if female_loc.count() > 0:
        female_loc.click()
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
        female_det_count = extract_detailed_count(page)
        print(f"[Gender Distribution - Female] Detailed View Count: {female_det_count}")
        _screenshot(page, "test_08_demographics_gender_female")
        page.go_back()
        page.wait_for_timeout(1000)
        
    # Verify Total Active Employees match Male + Female count on detailed pages
    if male_det_count is not None and female_det_count is not None and dashboard_active_count is not None:
        sum_gender = male_det_count + female_det_count
        print(f"Data Consistency Check - Dashboard Active Employees: {dashboard_active_count}, Sum of Gender Views (Male+Female): {sum_gender}")
        assert dashboard_active_count == sum_gender, (
            f"[Gender Distribution] Data Inconsistency Discrepancy! Dashboard Active Employees ({dashboard_active_count}) "
            f"does not match sum of Male ({male_det_count}) + Female ({female_det_count}) detailed views ({sum_gender})"
        )


