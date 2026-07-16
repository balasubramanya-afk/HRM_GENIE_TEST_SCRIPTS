import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_language_switcher(page: Page):
    """3. Test language switcher functionality."""
    login_as(page, "HR")
    page.wait_for_timeout(2000)
    
    # Switch language to US
    page.get_by_role("combobox").first.select_option("us")
    page.wait_for_timeout(1000)
    
    # Switch language back to EN
    page.get_by_role("combobox").first.select_option("en")
    page.wait_for_timeout(1000)
    
    _screenshot(page, "test_03_language_switcher")
