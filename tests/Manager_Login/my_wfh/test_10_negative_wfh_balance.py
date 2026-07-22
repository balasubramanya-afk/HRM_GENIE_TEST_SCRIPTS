import re
from playwright.sync_api import expect, Page
from .config import _screenshot, login_as, select_next_available_date, get_picker_button

def test_negative_wfh_balance_validation(page: Page):
    """10. Verify Monthly WFH Balance display and negative balance calculation when applying WFH beyond limit."""
    login_as(page, "Manager")
    page.goto("https://qa.hrmgenie.outstrive.co/work-from-home")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)

    my_wfh_tab = page.get_by_role("tab", name="My WFH")
    if my_wfh_tab.is_visible():
        my_wfh_tab.click()

    # Step 1: Open Apply WFH modal
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH")).first
    expect(apply_wfh_btn).to_be_visible()
    apply_wfh_btn.click()
    page.wait_for_timeout(1000)

    # Step 2: Assert Modal and Monthly WFH Balance element are visible
    modal = page.locator("[role='dialog']").first
    expect(modal).to_be_visible()

    balance_heading = page.get_by_text(re.compile(r"Monthly WFH Balance:", re.IGNORECASE)).first
    expect(balance_heading).to_be_visible()

    balance_subtext = page.get_by_text(re.compile(r"remaining this month|monthly WFH limit|used your monthly WFH limit", re.IGNORECASE)).first
    expect(balance_subtext).to_be_visible()

    # Step 3: Apply WFH request to consume / exceed balance
    start_date_btn = get_picker_button(page, "Pick start date")
    expect(start_date_btn).to_be_visible()
    start_date_btn.click()
    select_next_available_date(page, start_offset=1)
    page.wait_for_timeout(500)

    end_date_btn = get_picker_button(page, "Pick end date")
    expect(end_date_btn).to_be_visible()
    end_date_btn.click()
    select_next_available_date(page, start_offset=1)
    page.wait_for_timeout(500)

    reason_input = page.get_by_placeholder(re.compile(r"Enter your reason", re.IGNORECASE)).or_(page.locator("textarea")).or_(page.get_by_role("textbox", name="Reason *")).first
    expect(reason_input).to_be_visible()
    reason_input.fill("Testing WFH monthly balance calculation and negative balance tracking when limit is exceeded.")

    submit_btn = page.get_by_role("button", name="Apply").first
    expect(submit_btn).to_be_visible()
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Step 4: Re-open Apply WFH modal to verify balance update (negative balance or 0 limit)
    apply_wfh_btn = page.get_by_role("button", name="Apply WFH").or_(page.get_by_role("button", name="Request WFH")).or_(page.get_by_role("button", name="Apply For WFH")).first
    expect(apply_wfh_btn).to_be_visible()
    apply_wfh_btn.click()
    page.wait_for_timeout(1000)

    expect(modal).to_be_visible()
    expect(balance_heading).to_be_visible()

    # Assert balance shows remaining/negative balance text or limit reached notice
    updated_balance_text = modal.inner_text()
    assert ("Monthly WFH Balance:" in updated_balance_text), "Monthly WFH Balance header is missing in modal"
    
    # Assert that balance reflects usage (e.g. 0, negative balance, or limit message)
    expect(
        page.get_by_text(re.compile(r"Monthly WFH Balance:\s*-?\d+", re.IGNORECASE)).or_(
            page.get_by_text(re.compile(r"remaining this month|used your monthly WFH limit", re.IGNORECASE))
        ).first
    ).to_be_visible()

    _screenshot(page, "test_10_negative_wfh_balance_validation")
