import re
from playwright.sync_api import expect
from test_07_tracker_view import do_login_tracker
from config import _screenshot

def test_tracker_export(page):
    do_login_tracker(page)
    page.wait_for_load_state("networkidle")
    
    # Export and verify download starts
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Export").click()
    download = download_info.value
    
    print(f"Tracker Export Download Complete: {download.suggested_filename}")
    _screenshot(page, "tracker_report_exported")
    
    page.wait_for_timeout(3000)
