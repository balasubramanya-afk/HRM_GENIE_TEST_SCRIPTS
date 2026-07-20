from playwright.sync_api import Playwright, sync_playwright

PDF_PATH = "/Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/Source_files/3-mb-sample-pdf-file.pdf"


def upload_file(page, input_id):
    page.wait_for_selector(f"#{input_id}", state="attached", timeout=30000)
    page.locator(f"#{input_id}").set_input_files(PDF_PATH)
    page.wait_for_timeout(1000)
    page.locator("button:has-text('Upload Selected File')").click()
    page.wait_for_timeout(3000)
    page.locator(".absolute.right-2").click()
    page.wait_for_load_state("networkidle")


def delete_uploaded_files(page):
    delete_buttons = page.locator("button.bg-red-600").all()
    for _ in range(len(delete_buttons)):
        btn = page.locator("button.bg-red-600").first
        if btn.is_visible():
            btn.click()
            page.wait_for_timeout(2000)
            page.locator(".absolute.right-2").click()
            page.wait_for_load_state("networkidle")
        else:
            break


def test_whole(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").fill("gattu.ashwitha@brilyant.com")
    page.get_by_role("textbox", name="Enter password").fill("Ramesh@12345")
    page.get_by_role("button", name="Show password").click()
    page.locator("button:has-text('Login'), button[type='submit']").first.click()
    page.wait_for_url("**/dashboard**", timeout=15000)
    page.goto("https://qa.hrmgenie.outstrive.co/employee/documents")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)

    # To clean the previously uploaded files if any.
    delete_uploaded_files(page)

    # Upload files to the input fields.
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

    # View and download the uploaded file.
    view_link = page.locator("a[download]").first
    if view_link.is_visible():
        with page.context.expect_page() as new_page_info:
            view_link.click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("networkidle")
        new_page.close()

    # Clean the uploaded files 
    delete_uploaded_files(page)

    page.goto("https://qa.hrmgenie.outstrive.co/employee/team-employee")
    page.get_by_role("textbox", name="Search...").fill("aldjfhajlkhjdfjklshf")
    page.get_by_role("textbox", name="Search...").press("ControlOrMeta+a")
    page.get_by_role("textbox", name="Search...").fill("Vulapu")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_whole(playwright)
