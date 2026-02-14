import sys
import os
from playwright.sync_api import sync_playwright

PORT = 3000

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # Create 6 dummy files
            files = []
            for i in range(6):
                filename = f"test_img_{i}.png"
                with open(filename, "wb") as f:
                    # Minimal valid PNG header
                    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB\x60\x82')
                files.append(filename)

            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            page.goto(f"http://localhost:{PORT}/dirking.html")

            # Navigate to Claim page
            print("Navigating to Claim page...")
            page.get_by_text("Schaden melden").first.click()
            page.wait_for_selector("input[type='file']")

            # Upload 6 files
            print("Uploading 6 files...")
            page.set_input_files("input[type='file']", files)

            # Wait for potential error message
            page.wait_for_timeout(1000)

            # Check if error message is displayed
            # We expect a new error message about max files
            error_msg = page.locator("text=Maximal 5 Dateien erlaubt.")

            if error_msg.count() > 0:
                print("PASS: Error message displayed for too many files.")
                sys.exit(0)
            else:
                print("FAIL: No error message displayed for too many files.")
                # Also check if files were accepted
                uploaded_count = page.locator(".bg-blue-50.text-blue-700").count()
                print(f"Uploaded files count: {uploaded_count}")
                sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()
            # Cleanup
            for f in files:
                if os.path.exists(f):
                    os.remove(f)

if __name__ == "__main__":
    run()
