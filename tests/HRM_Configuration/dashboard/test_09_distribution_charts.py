import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_distribution_charts(page: Page):
    """9. Test Gender and Department Distribution charts."""
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
            
        loc.first.click()
        page.wait_for_timeout(1000)
        expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
        
        screenshot_name = f"test_09_dept_{dept.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
        _screenshot(page, screenshot_name)
        
        page.go_back()
        page.wait_for_timeout(1000)
