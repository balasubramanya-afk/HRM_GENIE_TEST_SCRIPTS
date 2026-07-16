import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_workforce_demographics(page: Page):
    """8. Test Workforce Demographics charts."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    page.get_by_role("heading", name="Workforce Demographics").click()
    
    page.locator(".h-full.bg-primary-color").first.click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_08_demographics_chart_1")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.locator(".space-y-4 > div:nth-child(2) > .h-4").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_08_demographics_chart_2")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.locator("div:nth-child(4) > .h-4").click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_08_demographics_chart_3")
    page.go_back()
    page.wait_for_timeout(1000)
    
    # Gender Distribution Section (moved from test_09)
    page.get_by_role("heading", name="Gender Distribution").click()
    
    page.get_by_text("Male", exact=True).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_08_demographics_gender_male")
    page.go_back()
    page.wait_for_timeout(1000)
    
    page.get_by_text("Female", exact=True).click()
    page.wait_for_timeout(1000)
    expect(page).to_have_url(re.compile(r".*/employee/all-employees.*"))
    _screenshot(page, "test_08_demographics_gender_female")
    page.go_back()
    page.wait_for_timeout(1000)
