from playwright.sync_api import sync_playwright
import os
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            # Assumes server is running on port 3000 (I will ensure it is)
            page.goto("http://localhost:3000/dirking.html")

            # Wait for FAB
            fab = page.locator("button[aria-label='Rückruf anfordern']")
            fab.wait_for(state="visible")

            # Click FAB
            fab.click()

            # Wait for Modal
            page.wait_for_selector("h3:has-text('Rückruf anfordern')")

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            page.screenshot(path="verification/sticky_callback.png")
            print("Screenshot saved to verification/sticky_callback.png")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
