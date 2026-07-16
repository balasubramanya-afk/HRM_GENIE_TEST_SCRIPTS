import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_distribution_charts(page: Page):
    """9. Test Gender and Department Distribution charts."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Department Distribution").click()
    
    page.get_by_text("Services").first.click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_09_dept_services")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_text("Shipment").first.click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_09_dept_shipment")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_text("Logistics").first.click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_09_dept_logistics")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_text("Sales", exact=True).first.click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_09_dept_sales")
    page.go_back()
    page.wait_for_timeout(1000)
