import os
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_resignation

def test_export_resignations(page):
    # ==========================================
    # PART 1: Login and Navigate to Resignation
    # ==========================================
    login_and_navigate_to_resignation(page, role="HR")
    
    # Wait for the table to fully render
    page.wait_for_timeout(2000)
    
    # Remove previous downloads if they exist
    if os.path.exists("exported_resignation.xlsx"):
        os.remove("exported_resignation.xlsx")
    if os.path.exists("exported_resignation.csv"):
        os.remove("exported_resignation.csv")
    
    # ==========================================
    # PART 2: Export as Excel
    # ==========================================
    page.get_by_role("button", name="Export").click()
    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Excel (.xlsx)").click()
        
    download_excel = download_info.value
    download_excel.save_as("exported_resignation.xlsx")
    page.wait_for_timeout(1000)
    
    # Verify the excel file was downloaded
    assert os.path.exists("exported_resignation.xlsx"), "Excel file was not downloaded!"
    
    # ==========================================
    # PART 3: Export as CSV
    # ==========================================
    page.get_by_role("button", name="Export").click()
    with page.expect_download() as download_csv_info:
        page.get_by_role("menuitem", name="CSV (.csv)").click()
        
    download_csv = download_csv_info.value
    download_csv.save_as("exported_resignation.csv")
    page.wait_for_timeout(1000)
    
    # Verify the csv file was downloaded
    assert os.path.exists("exported_resignation.csv"), "CSV file was not downloaded!"
    
    _screenshot(page, "test_06_export")
