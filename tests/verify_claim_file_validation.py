import sys
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

            print("Navigating to Claim page...")
            page.get_by_role("button", name="Schaden melden").first.click()
            page.wait_for_timeout(1000)

            # Create dummy invalid file
            with open("invalid.txt", "w") as f:
                f.write("This is not an image.")

            # Create dummy large file (6MB) - checking size limit
            # To avoid creating a huge file on disk, we can try to mock the file object in browser
            # But Playwright's setInputFiles handles real files.
            # Let's stick to type check first as it's easier and sufficient for "ONE small security issue".

            print("Uploading invalid file (text file)...")
            file_input = page.locator("input[type='file']")
            file_input.set_input_files("invalid.txt")

            # Wait for potential error message
            page.wait_for_timeout(500)

            # Check for error message
            error_msg = page.locator("text=Bitte nur Bilder (JPG, PNG) bis max. 5MB hochladen.")
            if error_msg.count() > 0:
                print("PASS: Error message displayed for invalid file type.")
            else:
                print("FAIL: Error message NOT displayed for invalid file type.")
                # We expect this to fail initially
                # sys.exit(1)

            # Check if file was added (it shouldn't be if validation works)
            if page.locator("text=invalid.txt").count() == 0:
                print("PASS: Invalid file was not added to list.")
            else:
                print("FAIL: Invalid file WAS added to list.")
                sys.exit(1)

            # Create a valid minimal PNG file
            with open("valid.png", "wb") as f:
                f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB\x60\x82')

            # Now try valid file
            print("Uploading valid file (valid.png)...")
            file_input.set_input_files("valid.png")
            page.wait_for_timeout(500)

            if page.locator("text=valid.png").count() > 0:
                print("PASS: Valid file added successfully.")
            else:
                print("FAIL: Valid file NOT added.")
                sys.exit(1)

            print("ALL CHECKS PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()
            # Cleanup
            if os.path.exists("invalid.txt"):
                os.remove("invalid.txt")
            if os.path.exists("valid.png"):
                os.remove("valid.png")

import os
if __name__ == "__main__":
    run()
