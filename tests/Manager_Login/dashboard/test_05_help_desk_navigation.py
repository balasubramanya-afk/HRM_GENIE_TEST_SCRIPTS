import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as

def test_help_desk_navigation(page: Page):
    """5. Test clicking the Help Desk button opens ITSM."""
    login_as(page, "Manager")
    page.wait_for_timeout(2000)
    
    with page.expect_popup() as popup_info:
        page.get_by_role("button", name="Help Desk").click()
    
    popup = popup_info.value
    popup.wait_for_load_state("networkidle")
    
    expect(popup).to_have_url(re.compile(r".*itsm\.outstrive\.co.*"))
    _screenshot(popup, "test_05_help_desk_popup")
    
    popup.close()
