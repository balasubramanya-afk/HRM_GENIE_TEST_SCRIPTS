import os
import re
from datetime import datetime
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright


def _get_test_screenshot_dir(config, item):
    """Create a single screenshot directory per test session run.

    Previously this created nested folders per test file.
    Now we always store screenshots under:
      screenshots/<run_id>/
    """
    root = Path(config.rootpath)
    screenshots_root = root / "screenshots"
    screenshots_root.mkdir(parents=True, exist_ok=True)

    now = datetime.now()
    run_id = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
    run_dir = screenshots_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir



def pytest_sessionstart(session):
    """Initialize run metadata without creating screenshot folders up front."""
    now = datetime.now()
    session.config.run_date = now.strftime("%d/%m/%Y")
    session.config.run_time = now.strftime("%I:%M:%S %p")


@pytest.fixture(scope="session")
def browser():
    """Launch browser once per test session."""
    with sync_playwright() as p:
        headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() == "true"
        keep_open = os.getenv("PLAYWRIGHT_KEEP_BROWSER_OPEN", "false").lower() == "true"
        slow_mo = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo)
        yield browser
        if not keep_open:
            browser.close()


@pytest.fixture(scope="session")
def page(browser):
    """Create page once per session - reuse across all tests."""
    context = browser.new_context(viewport=None)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def save_step(page, request):
    """Record a named step without taking screenshots during successful runs."""
    def _save_step(name: str):
        steps = getattr(request.node, "_captured_steps", [])
        steps.append(name)
        request.node._captured_steps = steps
    return _save_step


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot and record the failing line in a report when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        screenshots_dir = _get_test_screenshot_dir(item.config, item)
        failure_report = screenshots_dir / "failure_report.md"
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        item.config.screenshots_dir = str(screenshots_dir)
        item.config.failure_report = str(failure_report)
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%Y_%I-%M-%S_%p")
        safe_name = item.name.replace("/", "_").replace("\\", "_")
        filename = f"{safe_name}__failed__{timestamp}.png"
        screenshot_path = screenshots_dir / filename
        screenshot_text = str(screenshot_path.relative_to(item.config.rootpath))

        if report.when == "call":
            page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
            if page is not None:
                try:
                    page.screenshot(path=str(screenshot_path), full_page=True)
                except Exception as exc:
                    print(f"Failed to save screenshot for {item.name}: {exc}")

        file_path = item.fspath
        line_no = "n/a"
        excinfo = getattr(call, "excinfo", None)
        if excinfo is not None and getattr(excinfo, "value", None) is not None:
            traceback_obj = excinfo.value.__traceback__
            while traceback_obj is not None:
                frame_path = traceback_obj.tb_frame.f_code.co_filename
                frame_line = traceback_obj.tb_lineno
                if "site-packages" not in frame_path:
                    file_path = frame_path
                    line_no = frame_line
                    break
                traceback_obj = traceback_obj.tb_next
            else:
                file_path = excinfo.value.__traceback__.tb_frame.f_code.co_filename
                line_no = excinfo.value.__traceback__.tb_lineno

        if line_no == "n/a":
            match = re.search(r"(?P<file>.+?\.py):(?P<line>\d+)", report.captext or "", re.MULTILINE)
            if match:
                file_path = match.group("file")
                line_no = int(match.group("line"))

        if line_no == "n/a":
            location = getattr(item, "location", None)
            if location:
                file_path = location[0]
                line_no = location[1]
            elif report.location:
                file_path = report.location[0]
                line_no = report.location[1]

        try:
            rel_file = Path(file_path).relative_to(item.config.rootpath)
        except ValueError:
            rel_file = Path(file_path)

        with failure_report.open("a", encoding="utf-8") as handle:
            handle.write(f"## {item.nodeid}\n")
            handle.write(f"- File: {rel_file.as_posix()}\n")
            handle.write(f"- Line: {line_no}\n")
            handle.write(f"- When: {report.when}\n")
            handle.write(f"- Summary: {report.head_line}\n")
            handle.write(f"- Run Date: {item.config.run_date}\n")
            handle.write(f"- Run Time: {item.config.run_time}\n")
            handle.write(f"- Screenshot: {screenshot_text}\n\n")

        print(f"Failure report updated: {failure_report.name}")


@pytest.fixture(scope="session")
def logged_in_page(page):
    """Login once at session start, reuse page for all tests."""
    page.goto("https://qa.hrmgenie.outstrive.co/login")
    page.get_by_role("textbox", name="Enter email").fill("hr@out-strive.com")
    page.get_by_role("textbox", name="Enter password").fill("HR@dmin06")
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    print("Login successful. Reusing page for all tests.")
    yield page
