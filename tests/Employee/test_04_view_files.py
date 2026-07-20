from test_05_delete_files import delete_uploaded_files
from playwright.sync_api import Playwright, sync_playwright
from test_01_login import login
from test_03_upload_files import upload_file


def test_view_files(playwright: Playwright) -> None:
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

    delete_uploaded_files(page)

    upload_file(page, "docx-13")

    with page.expect_popup() as popup_info:
        page.locator(".bg-blue-600").last.click()
    new_page = popup_info.value
    new_page.wait_for_load_state()
    new_page.wait_for_timeout(2000)
    new_page.close()

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_view_files(playwright)
