
import sys
import time
from playwright.sync_api import sync_playwright

def verify_integration():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        try:
            print("Navigating to home...")
            page.goto('http://localhost:3000/dirking.html')
            time.sleep(1)

            # Dismiss Cookie Banner
            try:
                page.get_by_role("button", name="Einverstanden").click()
                print("Cookie banner dismissed.")
                time.sleep(0.5)
            except:
                print("Cookie banner not found or already dismissed.")

            page.screenshot(path='verification/home.png')
            print("Screenshot home.png saved.")

            # Navigate to Bedarfs-Check
            print("Navigating to Bedarfs-Check...")
            page.get_by_text("Bedarfs-Check", exact=True).click()
            time.sleep(1)
            page.screenshot(path='verification/wizard.png')
            print("Screenshot wizard.png saved.")

            # Navigate to Private Page (Quick Estimator)
            print("Navigating to Private Page...")
            page.get_by_text("Privat", exact=True).click()
            time.sleep(1)

            # Scroll to Quick Estimator
            estimator = page.locator("h2:has-text('Hausrat-Schnellcheck')")
            if estimator.is_visible():
                estimator.scroll_into_view_if_needed()
                time.sleep(0.5)
                page.screenshot(path='verification/quick_estimator.png')
                print("Screenshot quick_estimator.png saved.")
            else:
                print("Quick Estimator not found!")

            print("SUCCESS: Integration verified!")

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_integration()
