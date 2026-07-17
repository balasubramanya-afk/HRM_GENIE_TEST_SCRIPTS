import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_my_tasks(page: Page):
    """13. Test My Tasks section header visibility."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    heading = page.get_by_role("heading", name="My Tasks")
    expect(heading).to_be_visible()
    heading.click()
    
    _screenshot(page, "test_13_my_tasks")
