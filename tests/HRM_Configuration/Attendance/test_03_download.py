import re
from playwright.sync_api import expect
from test_01_login import do_login
from config import _screenshot

def test_download_attendance_report(page):
    do_login(page)
    page.wait_for_load_state("networkidle")
    
    # Click Export and expect the download
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Export").click()
    download = download_info.value
    
    # Log details or verify download was successful
    print(f"Download complete: {download.suggested_filename}")
    
    _screenshot(page, "attendance_report_downloaded")
    
    page.wait_for_timeout(3000)
