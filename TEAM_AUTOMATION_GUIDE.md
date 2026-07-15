# Playwright Automation Project Setup and Usage Guide

This document explains how to create, set up, run, and maintain the Playwright automation project in this workspace.

---

## 1. What this project does

This project automates browser-based tests for the HRM Genie application using:

- Python
- pytest
- Playwright
- pytest-playwright

It includes:

- reusable browser fixtures
- screenshot capture for each test step
- login setup for the application
- test files for modules such as login, work location, department, employment type, and region
- a custom code coverage audit script for comparing source files with automation tests

---

## 2. Project structure

```text
Playwrite Automation/
├── automation.py
├── coverage_audit.py
├── coverage_config.json
├── coverage_report.json
├── pytest.ini
├── requirements.txt
├── screenshots/
├── tests/
│   ├── __init__.py
│   ├── automation.py
│   ├── conftest.py
│   ├── test_1_login.py
│   ├── test_2_work_location.py
│   ├── test_3_Department.py
│   ├── test_4_Employment-type.py
└── .venv/            (created locally)
```

### Important files

- `requirements.txt` – Python dependencies
- `pytest.ini` – pytest configuration
- `tests/conftest.py` – shared fixtures and browser setup
- `tests/` – all automation test files
- `coverage_audit.py` – coverage audit script
- `coverage_config.json` – feature and action mapping used by the audit
- `coverage_report.json` – generated coverage report output

---

## 3. Prerequisites

Before starting, make sure the following are installed:

- Python 3.9 or higher
- pip
- Git
- Node.js (recommended for Playwright browser support)

Check versions:

```bash
python3 --version
pip --version
node --version
```

---

## 4. Create a new project folder

If you are starting from scratch:

```bash
mkdir Playwrite-Automation
cd Playwrite-Automation
```

Create these files:

- `requirements.txt`
- `pytest.ini`
- `tests/conftest.py`
- test files under `tests/`

---

## 5. Create and activate a virtual environment

Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

---

## 6. Install dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install the Playwright browser binaries:

```bash
playwright install chromium
```

If the install fails, try:

```bash
playwright install --with-deps chromium
```

---

## 7. Verify the environment

Run:

```bash
pytest --version
playwright --version
```

If both commands work, the environment is ready.

---

## 8. Running the tests

### Run all tests

```bash
pytest -q
```

### Run one test file

```bash
pytest -q tests/test_1_login.py
```

### Run a specific test

```bash
pytest -q tests/test_2_work_location.py -k create
```

### Run with visible browser output

By default, the browser can be run in headless mode. To make it visible, set:

```bash
export PLAYWRIGHT_HEADLESS=false
pytest -q
```

---

## 9. Useful environment variables

The project uses the following optional environment variables:

- `PLAYWRIGHT_HEADLESS=true|false`
- `PLAYWRIGHT_KEEP_BROWSER_OPEN=true|false`
- `PLAYWRIGHT_SLOW_MO=1000`

Example:

```bash
export PLAYWRIGHT_HEADLESS=true
export PLAYWRIGHT_KEEP_BROWSER_OPEN=false
export PLAYWRIGHT_SLOW_MO=500
pytest -q
```

---

## 10. Screenshots

Screenshots are stored in the `screenshots/` folder.

Each screenshot is saved automatically when a test step uses the `save_step` fixture.

---

## 11. How the tests are structured

The tests use:

- `pytest` for test execution
- fixtures from `tests/conftest.py`
- page objects or direct Playwright actions
- common login flow for shared sessions

The basic pattern is:

1. Open the application
2. Perform required actions
3. Assert expected behavior
4. Capture screenshots if needed

---

## 12. Running the coverage audit

This project also includes a simple code coverage-style audit that compares:

- source files from the HRMS application
- automation test files from this project

### Run the audit

```bash
python3 coverage_audit.py
```

This will:

- read `coverage_config.json`
- scan the configured source files and tests
- calculate feature and action coverage
- write the result to `coverage_report.json`

### View the coverage report

The output is saved in:

- `coverage_report.json`

You can also print a table-style summary from the terminal with a Python snippet.

---

## 13. What the coverage files mean

### `coverage_config.json`
This file defines:

- which features to audit
- which source files belong to each feature
- which test files should be matched
- action-level keywords for comparison

### `coverage_audit.py`
This is the logic that:

- loads the config
- searches for matching source and test content
- calculates coverage percentage
- writes the report to JSON

### `coverage_report.json`
This is the generated result file that stores the coverage output.

---

## 14. Folder and file explanation

### Root folder

- `automation.py`  
  Main automation entry point or helper script. It is useful when you want to run automation logic from a central script.

- `coverage_audit.py`  
  Custom audit script for comparing the application source code and automation tests to estimate feature and action coverage.

- `coverage_config.json`  
  Configuration file that tells the audit which features, source files, and tests should be compared.

- `coverage_report.json`  
  Output produced by the audit. This contains the computed results for all configured features.

- `pytest.ini`  
  Pytest configuration file. It tells pytest where tests are located and what file naming pattern to use.

- `requirements.txt`  
  Lists the Python packages required to run the project.

- `screenshots/`  
  Stores screenshots captured during test runs. Helpful for debugging and review.

### `tests/` folder

- `tests/__init__.py`  
  Python package marker for the tests folder.

- `tests/automation.py`  
  Helper module for automation logic. It may contain reusable logic shared across test files.

- `tests/conftest.py`  
  Shared fixtures and setup code. This file contains the browser fixture, page fixture, login fixture, and screenshot helper.

- `tests/test_1_login.py`  
  Tests the login flow such as entering credentials, submitting the form, and verifying login behavior.

- `tests/test_2_work_location.py`  
  Covers work location operations such as searching, creating, editing, deleting, and pagination.

- `tests/test_3_Department.py`  
  Covers department-related flows such as department creation/update, sub-department actions, practice actions, and designation handling.

- `tests/test_4_Employment-type.py`  
  Covers employment type operations like create, edit, delete, and dialog handling.

- `tests/test_5_region.py`  
  Intended for region module coverage once the test file is created and mapped in the configuration.

---

## 15. Why each test file is needed

### Login tests
These verify that users can log in successfully and that the login page behaves as expected. They protect the entry point of the application.

### Work location tests
These confirm that HR configuration users can manage work locations. This is important because location data affects business hierarchy and configuration.

### Department tests
These validate department and organizational configuration. They ensure the core HR configuration features continue to work correctly.

### Employment type tests
These check employment-type configuration, which is commonly used in employee setup and HR master data.

### Region tests
These ensure region-based configuration works properly. They are important for business structure and related HR configuration logic.

---

## 16. Why the fixtures are important

The fixtures in `tests/conftest.py` are important because they:

- avoid repeating setup code in every test
- ensure browser session reuse
- make login reusable across tests
- store screenshots in a consistent location
- reduce duplication and improve maintainability

---

## 17. Adding a new module or feature

If you add a new module, follow this approach:

1. Create a new test file in `tests/`
2. Add the feature and actions in `coverage_config.json`
3. Include relevant source paths and keywords
4. Run the audit again

Example idea:

- new test file: `tests/test_5_region.py`
- new feature entry in `coverage_config.json`
- run:

```bash
python3 coverage_audit.py
```

---

## 15. Common issues and fixes

### Issue: `pytest` not found

Run:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Playwright browser not installed

Run:

```bash
playwright install chromium
```

### Issue: tests fail to login

Check:

- application URL in the test or fixture
- username/password values
- network access
- whether the app changed its UI labels

### Issue: coverage report shows missing items

Check:

- whether the new test file exists
- whether the feature is added to `coverage_config.json`
- whether the keywords match the actual test/source content

### Issue: screenshots folder not created

Make sure the tests use the `save_step` fixture or create the folder manually.

---

## 16. Recommended daily workflow

1. Activate the virtual environment
2. Run tests
3. Review failures and screenshots
4. Update or add tests if needed
5. Run the coverage audit
6. Share the updated report with the team

Example:

```bash
cd '/Users/bits-blr-bala/Playwrite Automation'
source .venv/bin/activate
pytest -q
python3 coverage_audit.py
```

---

## 17. Summary

To work with this project successfully:

- create or open the workspace
- activate the virtual environment
- install dependencies
- run tests with pytest
- use the coverage audit when needed
- keep `coverage_config.json` updated for new modules

This setup is enough to run and maintain the automation suite for the team.
