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
            page.get_by_role("button", name="Schaden melden").first.click()
            page.wait_for_timeout(1000)

            # Check initial state: Submit button disabled
            # Scope to the form or main content to avoid footer link
            submit_btn = page.locator("#main-content button:has-text('Schaden melden')")

            if not submit_btn.is_disabled():
                print("FAIL: Submit button should be disabled initially.")
                sys.exit(1)
            print("PASS: Submit button is initially disabled.")

            # Fill form
            print("Filling form...")
            page.select_option("select", "Sturm")
            page.fill("input[type='date']", "2023-10-27")
            page.fill("textarea", "Mein Dach wurde durch den Sturm beschädigt.")

            # Add a file
            print("Uploading file...")
            # We can use logo.png which exists in the root
            file_input = page.locator("input[type='file']")
            file_input.set_input_files("logo.png")

            page.wait_for_timeout(500)

            # Verify file is listed
            if page.locator("text=logo.png").count() == 0:
                print("FAIL: Uploaded file name not displayed.")
                sys.exit(1)
            print("PASS: File uploaded and listed.")

            # Verify button is enabled
            if submit_btn.is_disabled():
                print("FAIL: Submit button should be enabled after filling form.")
                sys.exit(1)
            print("PASS: Submit button is enabled.")

            # Submit
            print("Submitting form...")
            submit_btn.click()

            # Check for Success Message
            # Wait for "Meldung erhalten" text
            try:
                page.get_by_text("Meldung erhalten").wait_for(timeout=5000)
                print("PASS: Success message appeared.")
            except:
                print("FAIL: Success message did not appear.")
                sys.exit(1)

            # Check confirmation text
            if page.locator("text=1 Bilder").count() == 0:
                 print("WARNING: Expected to see '1 Bilder' in success message.")

            print("ALL CHECKS PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
