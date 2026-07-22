# 📊 Code Coverage Audit: Region Module

This document presents the code coverage analysis for the **Region** module in the HRM Genie application, comparing the developer source code files against the Playwright automated test scripts.

---

## 📈 Coverage Summary

* **Feature Name:** `region`
* **Role:** `HR Admin`
* **Coverage Status:** 🟢 **Covered (100%)**
* **Total Actions:** 6 of 6 covered
* **Source Files Discovered:** 6 files
* **Test Files Discovered:** 9 files

---

## 📋 Action Coverage Details

| Feature Action | Status | Coverage % | Source Files Covered | Automation Test Scripts | Covered Details & Verified Keywords |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Login & Navigate to Region** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li></ul> | <ul><li>[test_01_login.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_01_login.py)</li></ul> | Logs into the application as the **HR Admin** role and navigates to the Region page via the `HRM Configuration` menu. Validates page load state and captures initial screenshot. |
| **Create Region** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li><li>[create-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/create-region-sheet.tsx)</li><li>[regionController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/regionController.js)</li><li>[regionRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/regionRoutes.js)</li></ul> | <ul><li>[test_02_create_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_02_create_region.py)</li></ul> | Covers the full region creation flow: opening and dismissing the dialog via **Close** and **Cancel** buttons, creating a region with `Country`, `Region Name`, and `Branch` selections via `POST /region`, verifying the `Region created successfully` toast, and asserting the duplicate name error `Region name already exists`. |
| **Search & Filters** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li></ul> | <ul><li>[test_03_search_branch.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_03_search_branch.py)</li><li>[test_04_search_text.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_04_search_text.py)</li><li>[test_05_combined_search.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_05_combined_search.py)</li></ul> | Full coverage of the filter toolbar: **Branch dropdown** search and selection (Tumkur, Kerala/Kozhikode, Mumbai/Kolkata/Pune), keyboard navigation (ArrowDown/ArrowUp/Enter/Escape), **text search** (`South West`, `Bala` – no match, `Warehouse`), **combined branch + text filters**, and **Reset Filters** clearing both `setSearchQuery` and `selectedBranch` state. |
| **Edit Region** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li><li>[edit-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/edit-region-sheet.tsx)</li><li>[regionController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/regionController.js)</li><li>[regionRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/regionRoutes.js)</li></ul> | <ul><li>[test_06_edit_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_06_edit_region.py)</li></ul> | Covers dismissal flows (**Close** / **Cancel**) and three update scenarios via `PUT /region`: (1) changing **Country** to USA, (2) switching Country back to India and updating **Region Name**, (3) updating Region Name and adding a **Branch**. Verifies `Region updated successfully` toast after each change. *(Region Head assignment is out of scope for this phase.)* |
| **Delete Region** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li><li>[delete-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/delete-region-sheet.tsx)</li><li>[regionController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/regionController.js)</li><li>[regionRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/regionRoutes.js)</li></ul> | <ul><li>[test_07_delete_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_07_delete_region.py)</li></ul> | Validates the delete confirmation dialog: dismissal via **Close** (X button), dismissal via **Cancel**, and successful deletion via `DELETE /region` using `handleDeleteConfirm` → `deleteRegion`. Confirms the `Region has been successfully deleted` toast is displayed. |
| **Pagination** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li></ul> | <ul><li>[test_08_pagination.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_08_pagination.py)</li></ul> | End-to-end pagination test: seeds the table to ≥ 11 records if needed, verifies `Showing 1 to 10 of N entries` on **Page 1**, navigates to **Page 2** (`Showing 11 to N of N entries`), uses **Go to previous page** and **Go to next page** aria-labelled controls via `onPageChange`, verifies `aria-current="page"` attribute on active page buttons. Also explicitly tests **page size switching** via `onEntriesPerPageChange`: selects 20 → 30 → 10 per page, asserting the `Showing X to Y of N` text adapts correctly for each size and page 2 reappears on revert to 10. Cleans up test data afterwards. |
| **Empty State UI** | `Covered` | **100%** | <ul><li>[page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)</li><li>[data-body.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/components/table/data-body.tsx)</li></ul> | <ul><li>[test_09_empty_state.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_09_empty_state.py)</li></ul> | Verifies the **`"No records found"`** empty-state cell (rendered by `DynamicTable` → `emptyMessage` default) across four scenarios: (1) text search with a non-existent term, (2) branch filter with a non-existent branch query, (3) combined text + branch filter yielding zero results, (4) **Reset Filters** clears the empty state and restores the full list — asserting `All Branch` combobox reset and empty search value. |

---

## ✅ All Actions Covered

All 6 actions defined for the Region module are now fully covered by the automation test suite. No outstanding gaps remain for this phase:

* **Region Head** — removed from scope in this phase; the `Head` (`designation_name`) column remains in the UI but no test is required.
* **Page Size Selection (`onEntriesPerPageChange`)** — now **explicitly tested** in `test_08_pagination.py` (Step 8): switches 10 → 20 → 30 → 10 per page, asserting the `Showing 1 to X of N` text adapts correctly for each size and that page 2 reappears on revert to 10.
* **Empty State UI** — now covered by `test_09_empty_state.py` (added in this iteration).

---

## 🗂️ Audited Files

### 💻 Source Files (Developer Repository)
1. **Region Page (List + Actions Shell):** [page.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/region/page.tsx)
2. **Create Region Sheet Component:** [create-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/create-region-sheet.tsx)
3. **Edit Region Sheet Component:** [edit-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/edit-region-sheet.tsx)
4. **Delete Region Dialog Component:** [delete-region-sheet.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/HRM-Config/components/delete-region-sheet.tsx)
5. **Backend API Router:** [regionRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/regionRoutes.js)
6. **Backend Business Logic:** [regionController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/regionController.js)

### 🧪 Automation Test Files
1. [test_01_login.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_01_login.py) — Login as HR Admin & navigate to Region page
2. [test_02_create_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_02_create_region.py) — Create region (full flow + duplicate error)
3. [test_03_search_branch.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_03_search_branch.py) — Branch dropdown search & filter
4. [test_04_search_text.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_04_search_text.py) — Text search filter (match, no-match, clear)
5. [test_05_combined_search.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_05_combined_search.py) — Combined branch + text search & reset
6. [test_06_edit_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_06_edit_region.py) — Edit region (country, name, branch)
7. [test_07_delete_region.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_07_delete_region.py) — Delete region (close, cancel, confirm)
8. [test_08_pagination.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_08_pagination.py) — Pagination (page 1/2, prev/next navigation)
9. [test_09_empty_state.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/test_09_empty_state.py) — Empty state UI (text, branch, combined filter → "No records found", reset)

### ⚙️ Test Configuration
* [config.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/HRM_Configuration/Region/config.py) — Role credentials, `login_as`, `navigate_to_region`, `close_toast`, `_screenshot` helpers

---
*Report generated on 2026-07-22.*
