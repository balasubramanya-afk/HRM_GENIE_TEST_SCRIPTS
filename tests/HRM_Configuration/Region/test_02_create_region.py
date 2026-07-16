from playwright.sync_api import Playwright, sync_playwright
from test_01_login import login, navigate_to_region


def test_create_region(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        channel="chrome",
        headless=False,
        args=["--start-maximized"]
    )
    context = browser.new_context(
        no_viewport=True
    )
    page = context.new_page()
    login(page)
    navigate_to_region(page)

    ## Creating region with all values given

    # Clicking the Create region button
    page.get_by_role("main").get_by_role("button", name="Region").click()

    # Selecting the country
    page.get_by_role("combobox", name="Country *").click()
    page.get_by_role("option", name="India").click()

    # Entering the region name
    page.get_by_role("textbox", name="Region *").click()
    page.get_by_role("textbox", name="Region *").fill("South West")
    page.get_by_role("textbox", name="Region *").press("Enter")

    # Selecting the branches
    page.get_by_text("Loading branches...").click()
    page.get_by_role("checkbox", name="Kerala").click()
    page.get_by_role("checkbox", name="Kozhikode -").click()
    page.get_by_role("checkbox", name="Tumkur -").click()

    # Clicking create button
    page.get_by_role("button", name="Create").click()

    # Closing the success pop up
    page.locator(".absolute.right-2").click()

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_create_region(playwright)
