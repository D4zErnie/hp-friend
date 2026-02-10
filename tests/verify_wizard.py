import sys
import time
from playwright.sync_api import sync_playwright

def verify_wizard():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            print("Navigating to home...")
            page.goto('http://localhost:3000/dirking.html')

            # Navigate to Bedarfs-Check
            print("Navigating to Bedarfs-Check...")
            page.get_by_text("Bedarfs-Check", exact=True).click()
            time.sleep(1)

            # Step 1: Select "Student"
            print("Step 1: Selecting 'Student'...")
            student_btn = page.get_by_text("Student", exact=True)
            if not student_btn.is_visible():
                print("FAILED: 'Student' option not visible")
                sys.exit(1)
            student_btn.click()
            time.sleep(0.5)

            # Step 2: Select "Gesundheit"
            print("Step 2: Selecting 'Gesundheit'...")
            health_btn = page.get_by_text("Gesundheit", exact=True)
            if not health_btn.is_visible():
                print("FAILED: 'Gesundheit' option not visible")
                sys.exit(1)
            health_btn.click()
            time.sleep(0.5)

            # Step 3: Verify Recommendations
            print("Step 3: Verifying Recommendations...")
            expected_rec = "Studentische Krankenversicherung"
            if not page.get_by_text(expected_rec).is_visible():
                print(f"FAILED: Expected recommendation '{expected_rec}' not visible")
                sys.exit(1)

            # Click "Angebot anfordern"
            print("Clicking 'Angebot anfordern'...")
            page.get_by_text("Angebot anfordern", exact=True).click()
            time.sleep(1)

            # Verify we are on Contact Page
            print("Verifying Contact Page...")
            if not page.get_by_text("Lernen wir uns kennen").is_visible():
                print("FAILED: Not redirected to contact page")
                sys.exit(1)

            # Verify Item in Merkliste
            print("Verifying Item in Merkliste...")
            if not page.get_by_text("Ihre Merkliste").is_visible():
                print("FAILED: 'Ihre Merkliste' section not visible")
                sys.exit(1)

            if not page.get_by_text(expected_rec).is_visible():
                print(f"FAILED: Item '{expected_rec}' not in Merkliste")
                sys.exit(1)

            print("SUCCESS: Wizard feature verified!")

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_wizard()
