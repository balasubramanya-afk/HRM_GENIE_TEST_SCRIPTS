# 📊 Code Coverage Audit: Organisation Info

This document presents the code coverage analysis for the **Organisation Info** module in the HRM Genie application, comparing the developer source code files against the Playwright automated test scripts.

---

## 📈 Coverage Summary

* **Feature Name:** `organisation_info`
* **Role:** `HR Admin`
* **Coverage Status:** 🟢 **Covered (100%)**
* **Total Actions:** 4 of 4 covered
* **Source Files Discovered:** 5 files
* **Test Files Discovered:** 5 files

---

## 📋 Action Coverage Details

| Feature Action | Status | Coverage % | Source Files Covered | Automation Test Scripts | Covered Details & Verified Keywords |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Logo Upload & Edit** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/setup/organisation-info/page.tsx)</li><li>[profileController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/profileController.js)</li></ul> | <ul><li>[test_02_logo_upload.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_02_logo_upload.py)</li><li>[test_06_logo_edit.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_06_logo_edit.py)</li></ul> | Uploading and editing of company assets: Dark Logo (`#logo-dark`), Light Logo (`#logo-light`), and Favicon (`#favicon`). Verified file stream logic in backend controller upload middleware. |
| **Company Information** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/setup/organisation-info/page.tsx)</li><li>[profileController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/profileController.js)</li></ul> | <ul><li>[test_03_organization_details.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_03_organization_details.py)</li></ul> | Fetching and updating text settings: `company_name`, `company_website`, `company_email`, `company_mobile`, and `company_domain_name`. Checks edit, discard, and save flows. |
| **System Settings** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/setup/organisation-info/page.tsx)</li><li>[profileController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/profileController.js)</li></ul> | <ul><li>[test_04_regional_settings.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_04_regional_settings.py)</li></ul> | Regional settings options: `employee_prefix`, `site_date_format`, and `site_time_format`. |
| **Primary Address** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/setup/organisation-info/page.tsx)</li><li>[profileController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/profileController.js)</li></ul> | <ul><li>[test_05_primary_address.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_05_primary_address.py)</li></ul> | Primary address parameters: `company_address`, `company_country`, `company_state`, `company_city`, and `company_zipcode`. |

---

## ⚠️ Uncovered / Missing Functions

* **None** (All identified features, endpoints, and actions for Organisation Info are fully covered by test scripts `test_01` through `test_06`).

---

## 🗂️ Audited Files

### 💻 Source Files (Developer Repository)
1. **Frontend UI Component:** [page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/setup/organisation-info/page.tsx)
2. **Redux Store Slice:** [company-setting-slice.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/store/slice/company-setting-slice.tsx)
3. **TypeScript Types:** [organisation-info.d.ts](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/types/organisation-info.d.ts)
4. **Backend Routes:** [profileRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/profileRoutes.js)
5. **Backend Controllers:** [profileController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/profileController.js)

### 🧪 Automation Test Files
1. [test_02_logo_upload.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_02_logo_upload.py)
2. [test_03_organization_details.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_03_organization_details.py)
3. [test_04_regional_settings.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_04_regional_settings.py)
4. [test_05_primary_address.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_05_primary_address.py)
5. [test_06_logo_edit.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Organization_Setup/test_06_logo_edit.py)

---
*Report generated on 2026-07-21.*
