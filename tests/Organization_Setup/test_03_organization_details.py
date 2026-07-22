import re
from playwright.sync_api import Playwright, sync_playwright
from config import login_as, navigate_to_organization_setup, _screenshot


def test_organization_details(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome", headless=False, args=["--start-maximized"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    login_as(page, "HR")
    navigate_to_organization_setup(page)
    _screenshot(page, "test_03_before_org_details")

    # Navigate to Organization Details section
    page.locator("div").filter(has_text=re.compile(r"^Logo Light$")).first.click()
    page.locator(
        ".tracking-tight.text-xl.font-medium.border-b-2.border-gray-100.pb-4.flex.flex-row > .inline-flex"
    ).first.click()
    page.wait_for_timeout(1500)

    # Fill organization details and save
    page.get_by_role("textbox", name="Company Name *").click()
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Company Name *").fill(
        "Brilyant IT Solutions Pvt Ltd"
    )
    page.get_by_role("textbox", name="Company Name *").press("Enter")
    page.get_by_role("textbox", name="Company Website *").click()
    page.get_by_role("textbox", name="Company Website *").fill("www.brilyant.com")
    page.get_by_role("textbox", name="Company Website *").press("Enter")
    page.get_by_role("textbox", name="Company Email *").click()
    page.get_by_role("textbox", name="Company Email *").fill("info@out-strive.com")
    page.get_by_role("textbox", name="Company Email *").press("Enter")
    page.get_by_role("textbox", name="Mobile Number *").click()
    page.get_by_role("textbox", name="Mobile Number *").fill("8901234567")
    page.get_by_role("textbox", name="Domain Name *").click()
    page.get_by_role("textbox", name="Domain Name *").fill("outstrive.com")
    page.get_by_role("button", name="Save").click()
    page.wait_for_timeout(2000)  # wait for save to complete and section to settle
    _screenshot(page, "test_03_org_details_saved")

    # Edit - change values and discard
    page.locator(
        ".tracking-tight.text-xl.font-medium.border-b-2.border-gray-100.pb-4.flex.flex-row > .inline-flex"
    ).first.click()
    page.wait_for_timeout(1500)
    page.get_by_role("textbox", name="Company Name *").click()
    page.get_by_role("textbox", name="Company Name *").click()
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowLeft")
    page.get_by_role("textbox", name="Company Name *").press("Alt+ArrowRight")
    page.get_by_role("textbox", name="Company Name *").fill(
        "Outstrive Solutions Pvt Ltd"
    )
    page.get_by_role("textbox", name="Company Website *").click()
    page.get_by_role("textbox", name="Company Email *").click()
    page.get_by_role("textbox", name="Mobile Number *").click()
    page.get_by_role("textbox", name="Mobile Number *").fill("9087654321")
    page.get_by_role("textbox", name="Domain Name *").click()
    page.get_by_role("textbox", name="Domain Name *").fill("brilyant.com")
    page.get_by_role("button", name="Discard").first.click()
    _screenshot(page, "test_03_org_details_discarded")

    # Verify original values persisted after discard
    page.get_by_text("outstrive.com").click()
    page.get_by_text("8901234567").click()

    # Edit Mobile and Domain, then save
    page.locator(
        ".tracking-tight.text-xl.font-medium.border-b-2.border-gray-100.pb-4.flex.flex-row > .inline-flex"
    ).first.click()
    page.wait_for_timeout(1500)
    page.get_by_role("textbox", name="Mobile Number *").click()
    page.get_by_role("textbox", name="Mobile Number *").fill("9087654321")
    page.get_by_role("textbox", name="Mobile Number *").press("Enter")
    page.get_by_role("textbox", name="Domain Name *").click()
    page.get_by_role("textbox", name="Domain Name *").fill("outstrive.com")
    page.get_by_role("button", name="Save").click()
    _screenshot(page, "test_03_org_details_updated")

    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_organization_details(playwright)
