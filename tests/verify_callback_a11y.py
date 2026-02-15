from playwright.sync_api import sync_playwright
import sys

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

            # Open callback modal
            print("Opening callback modal...")
            page.click("button[aria-label='Rückruf anfordern']")

            # Fill form
            print("Filling form...")
            page.fill("input[type='tel']", "0123456789")

            # Submit form
            print("Submitting form...")
            page.click("button[type='submit']")

            # Wait for toast
            print("Waiting for toast...")
            try:
                toast = page.locator("div[role='status']")
                toast.wait_for(state="visible", timeout=10000)
                print("PASS: Toast appeared.")
            except Exception as e:
                print(f"FAIL: Toast did not appear: {e}")
                sys.exit(1)

            # Find the close button inside the toast
            # The button is the one with the 'x' icon
            # We can select it by looking for the button inside the toast
            close_btn = toast.locator("button")

            # Check for aria-label
            aria_label = close_btn.get_attribute("aria-label")
            print(f"Toast close button aria-label: '{aria_label}'")

            if not aria_label:
                print("FAIL: Toast close button missing aria-label")
                sys.exit(1)
            else:
                print("PASS: Toast close button has aria-label")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
