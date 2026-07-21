import re
from playwright.sync_api import expect
from test_11_report_view import do_login_report
from config import _screenshot

def test_report_downloads(page):
    do_login_report(page)
    page.wait_for_load_state("networkidle")
    
    # 1. Download Excel
    page.get_by_role("button", name="Export").click()
    with page.expect_download() as download_xlsx_info:
        page.get_by_role("menuitem", name="Excel (.xlsx)").click()
    download_xlsx = download_xlsx_info.value
    print(f"Excel Export Download Complete: {download_xlsx.suggested_filename}")
    
    # 2. Download CSV
    page.get_by_role("button", name="Export").click()
    with page.expect_download() as download_csv_info:
        page.get_by_role("menuitem", name="CSV (.csv)").click()
    download_csv = download_csv_info.value
    print(f"CSV Export Download Complete: {download_csv.suggested_filename}")
    
    _screenshot(page, "report_exported_formats")
    
    page.wait_for_timeout(3000)
