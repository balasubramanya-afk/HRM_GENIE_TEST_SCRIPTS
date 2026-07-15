from playwright.sync_api import Page

LOGIN_URL = "https://qa.hrmgenie.outstrive.co/login"


def assert_login_page(page: Page) -> None:
    page.wait_for_load_state("networkidle")
    assert page.url.startswith(LOGIN_URL), f"Expected login page, but got: {page.url}"
    assert page.get_by_role("button", name="Login").is_visible()


def test_login_with_empty_credentials_stays_on_login_page(page: Page) -> None:
    """Ensure empty login submission does not progress past the login page."""
    page.goto(LOGIN_URL)
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(1000)
    assert_login_page(page)


def test_login_with_invalid_credentials_stays_on_login_page(page: Page) -> None:
    """Ensure invalid credentials do not allow access to the dashboard."""
    page.goto(LOGIN_URL)
    page.get_by_role("textbox", name="Enter email").fill("invalid-email")
    page.get_by_role("textbox", name="Enter password").fill("wrong-password")
    page.get_by_role("button", name="Login").click()
    page.wait_for_timeout(2000)
    assert_login_page(page)


def test_login_flow(logged_in_page) -> None:
    """Verify login was successful by checking we're on the dashboard."""
    page = logged_in_page

    # Verify we're logged in and on the dashboard (not on login page)
    assert not page.url.startswith(LOGIN_URL), "Should not be on login page"
    assert page.url.startswith("https://qa.hrmgenie.outstrive.co/"), "Should be on dashboard"
    assert page.get_by_text("HRM Configuration").is_visible(), "Dashboard should be visible"
    print("Login verification successful. Ready for remaining tests.")
