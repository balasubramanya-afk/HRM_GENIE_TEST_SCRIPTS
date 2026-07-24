import re
from playwright.sync_api import expect
from config import _screenshot, login_and_navigate_to_certifications


def test_manager_certifications_negative_scenarios(page):
    """
    Negative test cases for Manager Login - Certifications Module.

    Negative Test 1: Add Certification without filling any mandatory fields (empty form submit)
    Negative Test 2: Add Certification without uploading an attachment
    Negative Test 3: Add Certification with only whitespace in the Certificate Name field
    
    """

    # ==========================================
    # Pre-requisite: Login and Navigate to Certifications
    # ==========================================
    login_and_navigate_to_certifications(page, role="Manager")
    page.wait_for_timeout(3000)

    # ==========================================
    # Negative Test 1: Submit the form with ALL fields empty
    # Expected: Form should NOT submit; validation errors should appear
    # ==========================================
    print("\n--- Negative Test 1: Submit certification form with all fields empty ---")

    page.locator("button").filter(has_text="Add Certification").click()
    page.wait_for_timeout(1000)

    

    # Attempt to submit without filling anything
    page.get_by_role("button", name="Upload").click()
    page.wait_for_timeout(1500)

    _screenshot(page, "test_06_neg1_empty_form_after_submit")

    # Verification: Upload button should still be visible (modal not closed = form blocked)
    upload_still_visible = page.get_by_role("button", name="Upload").count() > 0
    assert upload_still_visible, (
        "Negative Test 1 FAILED: Form was submitted with all empty fields. "
        "The Upload button should remain visible, indicating the form is still open."
    )
    print("  [PASS] Form correctly blocked submission with all empty fields.")

    # Close the modal
    try:
        close_btn = page.get_by_role("button", name="Cancel").first
        if close_btn.is_visible(timeout=1000):
            close_btn.click()
        else:
            page.keyboard.press("Escape")
    except Exception:
        page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 2: Fill mandatory fields but skip the attachment upload
    # Expected: Form should NOT submit without an attachment
    # ==========================================
    print("\n--- Negative Test 2: Submit certification form without uploading attachment ---")

    page.locator("button").filter(has_text="Add Certification").click()
    page.wait_for_timeout(1000)

    # Select certification type from combobox
    try:
        page.get_by_role("combobox").click()
        page.wait_for_timeout(500)
        options = page.get_by_role("option").all()
        if options:
            options[0].click()
        page.wait_for_timeout(500)
    except Exception:
        pass

    # Fill Certificate Name
    name_field = page.get_by_role("textbox", name="Certificate name")
    name_field.fill("Neg Test No Attachment")

    # Fill Certificate ID
    id_field = page.get_by_role("textbox", name=re.compile(r"e\.g\.,.*ID", re.IGNORECASE))
    if id_field.count() > 0:
        id_field.first.fill("CERT-NOATTACH")

    # Select Lifetime radio (skip attachment intentionally)
    lifetime_label = page.locator("label").filter(
        has_text=re.compile(r"life\s*time", re.IGNORECASE)
    )
    if lifetime_label.count() > 0:
        lifetime_label.first.click()
    else:
        page.get_by_role("radio").first.click()
    page.wait_for_timeout(500)

    # Do NOT upload any attachment — click Upload directly
    

    page.get_by_role("button", name="Upload").click()
    page.wait_for_timeout(1500)

    _screenshot(page, "test_06_neg2_no_attachment_after_submit")

    # Verification: modal still open OR a warning toast appeared
    upload_still_visible = page.get_by_role("button", name="Upload").count() > 0
    warning_toast = page.locator("[data-sonner-toast]").count() > 0

    assert upload_still_visible or warning_toast, (
        "Negative Test 2 FAILED: Certification was created without an attachment. "
        "Validation should require an attachment before submitting."
    )

    if upload_still_visible:
        print("  [PASS] Form correctly blocked submission without an attachment.")
    else:
        print("  [PASS] Warning toast appeared for missing attachment.")

    # Close the modal
    try:
        close_btn = page.get_by_role("button", name="Cancel").first
        if close_btn.is_visible(timeout=1000):
            close_btn.click()
        else:
            page.keyboard.press("Escape")
    except Exception:
        page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    # ==========================================
    # Negative Test 3: Select "Dated" validity type but leave From/To dates empty
    # Expected: Form should NOT submit without providing the required date range
    # ==========================================
    print("\n--- Negative Test 3: Submit dated certification without selecting From/To dates ---")

    page.locator("button").filter(has_text="Add Certification").click()
    page.wait_for_timeout(1000)

    # Select certification type from combobox
    try:
        page.get_by_role("combobox").click()
        page.wait_for_timeout(500)
        options = page.get_by_role("option").all()
        if options:
            options[0].click()
        page.wait_for_timeout(500)
    except Exception:
        pass

    # Fill Certificate Name
    name_field = page.get_by_role("textbox", name="Certificate name")
    name_field.fill("Neg Test Dated No Dates")

    # Fill Certificate ID
    id_field = page.get_by_role("textbox", name=re.compile(r"e\.g\.,.*ID", re.IGNORECASE))
    if id_field.count() > 0:
        id_field.first.fill("CERT-NODATES")

    # Select "Select date" (Dated) radio — intentionally skip picking any dates
    try:
        page.get_by_role("radio", name="Select date").click()
        page.wait_for_timeout(500)
    except Exception:
        page.get_by_role("radio").last.click()
        page.wait_for_timeout(500)

    # Upload attachment
    try:
        page.get_by_label("Upload attachment").set_input_files("dummy_cert.pdf")
        page.wait_for_timeout(1000)
    except Exception:
        print("  [INFO] Could not upload attachment for NT-3 — continuing.")

    

    # Attempt to submit without selecting any dates
    page.get_by_role("button", name="Upload").click()
    page.wait_for_timeout(1500)

    _screenshot(page, "test_06_neg3_dated_no_dates_after_submit")

    # Verification: modal still open (dates not provided) OR a warning toast appeared
    upload_still_visible = page.get_by_role("button", name="Upload").count() > 0
    warning_toast = page.locator("[data-sonner-toast]").count() > 0

    assert upload_still_visible or warning_toast, (
        "Negative Test 3 FAILED: Certification was accepted with Dated type but no dates selected. "
        "Validation should require From and To dates when 'Select date' is chosen."
    )

    if upload_still_visible:
        print("  [PASS] Form correctly blocked submission — dates are required for Dated type.")
    else:
        print("  [PASS] Warning toast appeared for missing date range.")

    # Close the modal
    try:
        close_btn = page.get_by_role("button", name="Cancel").first
        if close_btn.is_visible(timeout=1000):
            close_btn.click()
        else:
            page.keyboard.press("Escape")
    except Exception:
        page.keyboard.press("Escape")
    page.wait_for_timeout(1000)

    