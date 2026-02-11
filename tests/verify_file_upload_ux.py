import sys
import os
from playwright.sync_api import sync_playwright

PORT = 3000

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                sys.exit(1)

            page.wait_for_timeout(2000)

            # Navigate to 'Schaden melden' page from footer
            print("Navigating to Claim page...")
            page.locator("footer").get_by_text("Schaden melden").click()
            page.wait_for_timeout(1000)

            # Add a file
            print("Uploading file...")
            file_input = page.locator("input[type='file']")
            file_input.set_input_files("logo.png")

            page.wait_for_timeout(500)

            # Verify file is listed
            if page.locator("text=logo.png").count() == 0:
                print("FAIL: Uploaded file name not displayed.")
                sys.exit(1)
            print("PASS: File uploaded and listed.")

            # Check for remove button
            remove_btn = page.locator("button[aria-label='logo.png entfernen']")
            if remove_btn.count() == 0:
                print("FAIL: Remove button does not exist.")
                sys.exit(1)
            print("PASS: Remove button exists.")

            # Click remove button
            print("Removing file...")
            remove_btn.click()
            page.wait_for_timeout(500)

            # Verify file is removed
            if page.locator("text=logo.png").count() > 0:
                print("FAIL: File still displayed after removal.")
                sys.exit(1)
            print("PASS: File removed successfully.")

            print("UX VERIFICATION PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
