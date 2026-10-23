"""
Automated genuine screenshot capture script using installed Google Chrome.
Generates genuine screenshots of all UI states and LMS questions on the live Streamlit app.
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
        "question": "How many days of Privilege Leave (PL) does a permanent employee get per year?",
    },
    {
        "filename": "03_probation_period_question.png",
        "question": "What is the probation period for employees up to Senior Manager?",
    },
    {
        "filename": "04_health_insurance_question.png",
        "question": "What is the company's health-insurance premium amount?",
    },
    {
        "filename": "05_gst_rate_question.png",
        "question": "What is the current GST rate in India?",
    },
    {
        "filename": "06_maternity_leave_question.png",
        "question": "How many days of maternity leave are given?",
    },
]


def ask_question_and_capture(page, question_text, output_filename):
    print(f"\nSubmitting: '{question_text}' -> {output_filename}...")
    page.goto(APP_URL, wait_until="networkidle")
    time.sleep(2)

    # Ensure light mode
    light_btn = page.query_selector('button:has-text("Light Mode")')
    if light_btn:
        light_btn.click()
        time.sleep(1.5)

    inp = page.wait_for_selector('input[data-testid="stTextInputField"]')
    inp.fill(question_text)
    time.sleep(0.5)
    inp.press("Enter")

    # Wait for bot response to render
    time.sleep(6.5)

    page.screenshot(path=str(SCREENSHOTS_DIR / output_filename))
    print(f"✅ Saved {output_filename}")


def capture_all():
    print("📸 Starting live UI screenshot capture from Streamlit...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 880})
        page = context.new_page()

        # 1. Capture 01_home_screen.png and light_mode_ui.png
        print("\nCapturing 01_home_screen.png & light_mode_ui.png...")
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(2.5)

        # Ensure light mode
        light_btn = page.query_selector('button:has-text("Light Mode")')
        if light_btn:
            light_btn.click()
            time.sleep(2)

        page.screenshot(path=str(SCREENSHOTS_DIR / "01_home_screen.png"))
        page.screenshot(path=str(SCREENSHOTS_DIR / "light_mode_ui.png"))
        page.screenshot(path=str(SCREENSHOTS_DIR / "app_ui.png"))
        page.screenshot(path=str(SCREENSHOTS_DIR / "current_live_ui.png"))
        print("✅ Saved 01_home_screen.png, light_mode_ui.png, app_ui.png")

        # 2. Capture Dark Mode
        print("\nCapturing dark_mode_ui.png & 08_dark_mode_interface.png...")
        dark_btn = page.query_selector('button:has-text("Dark Mode")')
        if dark_btn:
            dark_btn.click()
            time.sleep(2.5)
            page.screenshot(path=str(SCREENSHOTS_DIR / "dark_mode_ui.png"))
            page.screenshot(path=str(SCREENSHOTS_DIR / "08_dark_mode_interface.png"))
            print("✅ Saved dark_mode_ui.png & 08_dark_mode_interface.png")

            # Reset back to light mode
            light_btn = page.query_selector('button:has-text("Light Mode")')
            if light_btn:
                light_btn.click()
                time.sleep(2)

        # 3. Capture Each Test Case Question
        for tc in TEST_CASES:
            ask_question_and_capture(page, tc["question"], tc["filename"])

        # 4. Capture not_found_ui.png
        print("\nCapturing not_found_ui.png...")
        ask_question_and_capture(
            page,
            "What is the corporate income tax rate in India?",
            "not_found_ui.png",
        )

        # 5. Capture close-up of source reference subcard
        print("\nCapturing 07_source_reference_excerpt.png...")
        page.goto(APP_URL, wait_until="networkidle")
        time.sleep(2)
        ref_card = page.query_selector(".reference-subcard")
        if ref_card:
            ref_card.screenshot(path=str(SCREENSHOTS_DIR / "07_source_reference_excerpt.png"))
            print("✅ Saved 07_source_reference_excerpt.png (element screenshot)")
        else:
            page.screenshot(path=str(SCREENSHOTS_DIR / "07_source_reference_excerpt.png"))

        browser.close()

    print("\n🎉 All current UI screenshots updated successfully in screenshots/ folder!")


if __name__ == "__main__":
    capture_all()
