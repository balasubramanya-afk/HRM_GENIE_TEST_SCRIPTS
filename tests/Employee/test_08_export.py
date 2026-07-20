import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import Page, expect
from config import login_as, _screenshot

# Where to save the downloaded files (inside the test folder for cleanliness)
DOWNLOAD_DIR = Path(__file__).parent / "downloads"


def test_export_employees(page: Page) -> None:
    # ── Setup: ensure download folder exists and remove old exports ─────────
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    excel_path = DOWNLOAD_DIR / "exported_employees.xlsx"
    csv_path   = DOWNLOAD_DIR / "exported_employees.csv"

    if excel_path.exists():
        excel_path.unlink()
    if csv_path.exists():
        csv_path.unlink()

    # ── Login and navigate to All Employees ─────────────────────────────────
    login_as(page, "HR")
    page.locator("div").filter(has_text=re.compile(r"^Employee$")).get_by_role("button").click()
    page.get_by_role("button", name="All Employees").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # ── Export as Excel (.xlsx) ─────────────────────────────────────────────
    page.get_by_role("button", name="Export").click()
    page.wait_for_timeout(500)

    with page.expect_download() as download_info:
        page.get_by_role("menuitem", name="Excel (.xlsx)").click()

    download_excel = download_info.value
    download_excel.save_as(str(excel_path))
    page.wait_for_timeout(1000)

    assert excel_path.exists(), f"Excel file was NOT downloaded! Expected at: {excel_path}"
    assert excel_path.stat().st_size > 0, "Excel file was downloaded but is empty!"
    print(f"✅ Excel export successful: {excel_path} ({excel_path.stat().st_size} bytes)")

    # ── Export as CSV (.csv) ────────────────────────────────────────────────
    page.get_by_role("button", name="Export").click()
    page.wait_for_timeout(500)

    with page.expect_download() as download_csv_info:
        page.get_by_role("menuitem", name="CSV (.csv)").click()

    download_csv = download_csv_info.value
    download_csv.save_as(str(csv_path))
    page.wait_for_timeout(1000)

    assert csv_path.exists(), f"CSV file was NOT downloaded! Expected at: {csv_path}"
    assert csv_path.stat().st_size > 0, "CSV file was downloaded but is empty!"
    print(f"✅ CSV export successful: {csv_path} ({csv_path.stat().st_size} bytes)")

    _screenshot(page, "08_export_employees")
    print("✅ Export test completed successfully for both Excel and CSV!")
