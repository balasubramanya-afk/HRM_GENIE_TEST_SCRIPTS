# 📊 Code Coverage Audit: Employee Module

This document presents the code coverage analysis for the **Employee** module in the HRM Genie application, comparing the developer source code files against the Playwright automated test scripts.

---

## 📈 Coverage Summary

* **Feature Name:** `employee`
* **Role:** `BUH`
* **Coverage Status:** 🟢 **Covered (100%)**
* **Total Actions:** 7 of 7 covered
* **Source Files Discovered:** 9 files
* **Test Files Discovered:** 7 files

---

## 📋 Action Coverage Details

| Feature Action | Status | Coverage % | Source Files Covered | Automation Test Scripts | Covered Details & Verified Keywords |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Login as BUH** | `Covered` | **100%** | <ul><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li></ul> | <ul><li>[test_01_login.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_01_login.py)</li></ul> | Logging into the application with the **Business Unit Head (BUH)** role to test module access and specific dashboard endpoints like [getBUHTeamEmployeeByEmployeeId](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L1827). |
| **Load Submodules** | `Covered` | **100%** | <ul><li>[general.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/general.tsx)</li><li>[employee-details.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/employee-details.tsx)</li><li>[details-tab.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/Details/details-tab.tsx)</li></ul> | <ul><li>[test_02_submodules.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_02_submodules.py)</li></ul> | Navigating and verifying the main tabs under employee: `General`, `Documents`, `Education`, `Experience`, `Promotions`, `Team Members`, and `Indirect Reportees`. |
| **Upload Documents** | `Covered` | **100%** | <ul><li>[employeeRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/employeeRoutes.js)</li><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li><li>[documents.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/documents.tsx)</li></ul> | <ul><li>[test_03_upload_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_03_upload_files.py)</li></ul> | Uploading required documents such as degree certificates, address proof, payslips, and others using multi-part upload middleware (`uploadDocuments.single`). |
| **View Documents** | `Covered` | **100%** | <ul><li>[employeeRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/employeeRoutes.js)</li><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li><li>[documents.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/documents.tsx)</li></ul> | <ul><li>[test_04_view_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_04_view_files.py)</li></ul> | Retrieving document attachment files in a new window/popup dynamically through the backend [getEmployeeDocument](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L732) and [getByIdEmployeeDocument](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L84) controllers. |
| **Delete Documents** | `Covered` | **100%** | <ul><li>[employeeRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/employeeRoutes.js)</li><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li></ul> | <ul><li>[test_05_delete_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_05_delete_files.py)</li></ul> | Deleting uploaded files and confirming deletions through verification dialogs. Relies on state modification APIs (`updateStatusEmployeeDocument`). |
| **Team Members View & Filter** | `Covered` | **100%** | <ul><li>[team-members.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/team-members.tsx)</li><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li></ul> | <ul><li>[test_06_team_members.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_06_team_members.py)</li></ul> | Accessing, searching, and filtering the team directory by **Designation**, **Department**, and **Location**. Clicks and inspects individual team member profile summaries. |
| **Indirect Reportees View & Filter** | `Covered` | **100%** | <ul><li>[indirect-report.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/indirect-report.tsx)</li><li>[employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)</li></ul> | <ul><li>[test_07_indirect_reportees.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_07_indirect_reportees.py)</li></ul> | Querying the list of indirect reports and filtering them dynamically under the BUH Login context via the [getBUHTeamEmployeeByEmployeeId](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L1827) endpoint. |

---

## ⚠️ Uncovered / Missing Functions

### Covered in HR Admin login - Employee module by Chandrika

The following features/functions present in the source files are not covered by current automation scripts:
* **Update Employee Profile Details**: Updating Personal Information ([personal-info.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/personal-info.tsx)), Address Details ([addressInfo.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/addressInfo.tsx)), Emergency Contact ([emergencyInfo.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/emergencyInfo.tsx)), and Bank Details ([bank-details.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/bank-details.tsx)) via backend controller [updateEmployee](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L226).
* **Employee Onboarding**: Processing new employee onboarding flow via backend controller [onBoardEmployee](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L574).
* **Employee Probation Management**: Managing probation records via [addEmployeeProbation](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L1962), [updateEmployeeProbation](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L2058), and [deleteEmployeeProbation](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js#L2068).

---

## 🗂️ Audited Files

### 💻 Source Files (Developer Repository)
1. **Frontend View Shell:** [general.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/general.tsx)
2. **Frontend Details Panel:** [employee-details.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/employee-details.tsx)
3. **Tabs Layout Coordinator:** [details-tab.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/Details/details-tab.tsx)
4. **Header Profile info card:** [userInfo.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/userInfo.tsx)
5. **Personal Information Forms:** [personal-info.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/personal-info.tsx)
6. **Address Forms:** [addressInfo.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/addressInfo.tsx)
7. **Emergency Contact Forms:** [emergencyInfo.tsx](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/frontend/src/pages/Employee/components/UpdateEmployee/emergencyInfo.tsx)
8. **Backend API Router:** [employeeRoutes.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/routes/employeeRoutes.js)
9. **Backend Business Logic:** [employeeController.js](file:///Users/bits-blr-sangiliboopathi/HRMS_NodeJs/backend/controllers/employeeController.js)

### 🧪 Automation Test Files
1. [test_01_login.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_01_login.py)
2. [test_02_submodules.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_02_submodules.py)
3. [test_03_upload_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_03_upload_files.py)
4. [test_04_view_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_04_view_files.py)
5. [test_05_delete_files.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_05_delete_files.py)
6. [test_06_team_members.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_06_team_members.py)
7. [test_07_indirect_reportees.py](file:///Users/bits-blr-sangiliboopathi/HRM_GENIE_TEST_SCRIPTS/tests/Employee/test_07_indirect_reportees.py)

---
*Report generated on 2026-07-22.*
