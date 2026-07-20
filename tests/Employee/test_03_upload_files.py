from playwright.sync_api import Playwright, sync_playwright
from test_01_login import login
from test_05_delete_files import delete_uploaded_files

PDF_PATH = "/Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/Source_files/3-mb-sample-pdf-file.pdf"


def upload_file(page, input_id):
    page.wait_for_selector(f"#{input_id}", state="attached", timeout=15000)
    page.locator(f"#{input_id}").set_input_files(PDF_PATH)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Upload Selected File").click()
    page.wait_for_timeout(1000)
    page.locator(".absolute.right-2").click()
    page.wait_for_timeout(1000)


def test_upload_files(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    login(page)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/general")
    page.wait_for_timeout(1000)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/documents")
    page.wait_for_timeout(1000)

    # Delete the uploaded files if any
    delete_uploaded_files(page)

    upload_file(page, "docx-8")
    upload_file(page, "docx-9")
    upload_file(page, "docx-12")
    upload_file(page, "docx-13")
    upload_file(page, "docx-14")
    upload_file(page, "docx-15")
    upload_file(page, "docx-16")
    upload_file(page, "docx-17")
    upload_file(page, "docx-18")
    upload_file(page, "docx-39")
    upload_file(page, "docx-40")
    upload_file(page, "docx-41")

    # Delete the uploaded files
    delete_uploaded_files(page)

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_upload_files(playwright)
