"""
Automated genuine screenshot capture script using installed Google Chrome.
Generates genuine screenshots of all LMS test cases on the live Streamlit app.
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP_URL = "http://localhost:8501"

TEST_CASES = [
    {
        "filename": "02_privilege_leave_question.png",
        "btn_text": "1. Privilege Leave Days",
        "question": "How many days of Privilege Leave (PL) does a permanent employee get per year?",
    },
    {
        "filename": "03_probation_period_question.png",
        "btn_text": "2. Probation Period",
        "question": "What is the probation period for employees up to Senior Manager?",
    },
    {
        "filename": "04_health_insurance_question.png",
        "btn_text": "3. Health-Insurance Premium",
        "question": "What is the company's health-insurance premium amount?",
    },
    {
        "filename": "05_gst_rate_question.png",
        "btn_text": "4. India GST Rate",
        "question": "What is the current GST rate in India?",
    },
    {
        "filename": "06_maternity_leave_question.png",
        "btn_text": "5. Maternity Leave Days",
        "question": "How many days of maternity leave are given?",
    },
]


def capture_all():
    print("📸 Starting live screenshot capture from Streamlit...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
        )
        context = browser.new_context(viewport={"width": 1366, "height": 920})
        page = context.new_page()

        # 1. Capture Home Screen
        print("Capturing 01_home_screen.png...")
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(3)
        page.screenshot(path=str(SCREENSHOTS_DIR / "01_home_screen.png"))
        print("✅ Saved 01_home_screen.png")

        # 2-6. Capture Each Question
        for tc in TEST_CASES:
            fname = tc["filename"]
            btn_txt = tc["btn_text"]
            q = tc["question"]
            print(f"\nProcessing '{btn_txt}' -> {fname}...")

            # Reset / goto page to guarantee fresh state
            page.goto(APP_URL, wait_until="networkidle")
            time.sleep(1.5)

            # Click preset button
            page.locator(f"button:has-text('{btn_txt}')").click()
            time.sleep(1.5)

            # Click Ask Question submit button
            page.locator("button:has-text('Ask Question')").click()

            # Wait for answer card to appear
            try:
                page.wait_for_selector(".answer-card", timeout=20000)
                time.sleep(2)
            except Exception as e:
                print(f"⚠️ Wait timeout for {fname}: {e}")
                time.sleep(5)

            page.screenshot(path=str(SCREENSHOTS_DIR / fname))
            print(f"✅ Saved {fname}")

            # For Q1, also capture the expanded source reference excerpt
            if "privilege_leave" in fname:
                print("Capturing 07_source_reference_excerpt.png...")
                time.sleep(1)
                page.evaluate("window.scrollBy(0, 320)")
                time.sleep(1.5)
                page.screenshot(path=str(SCREENSHOTS_DIR / "07_source_reference_excerpt.png"))
                print("✅ Saved 07_source_reference_excerpt.png")

        browser.close()
        print("\n🎉 All 7 genuine screenshots successfully captured and saved to screenshots/!")


if __name__ == "__main__":
    capture_all()
