from playwright.sync_api import sync_playwright
import sys

PORT = 3000

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # Capture console messages
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                sys.exit(1)

            page.wait_for_timeout(2000) # Wait for React to mount

            # 1. Verify FAB exists
            print("Looking for FAB...")
            try:
                fab = page.locator("button[aria-label='Rückruf anfordern']")
                fab.wait_for(state="visible", timeout=5000)
                print("PASS: FAB button found.")
            except Exception as e:
                print(f"FAIL: FAB button not found: {e}")
                sys.exit(1)

            # 2. Click FAB
            fab.click()
            page.wait_for_timeout(500)

            # 3. Verify Modal opens
            print("Looking for Modal...")
            try:
                modal = page.locator("h3:has-text('Rückruf anfordern')")
                modal.wait_for(state="visible", timeout=5000)
                print("PASS: Modal opened.")
            except Exception as e:
                print(f"FAIL: Modal not found: {e}")
                sys.exit(1)

            # 4. Fill form
            print("Filling form...")
            page.fill("input[type='tel']", "0123456789")

            # Select 'Mittags' (lunch)
            # Find the input by value
            lunch_input = page.locator("input[value='lunch']")
            # Click the parent label because input is hidden
            # Or force click the input
            lunch_input.click(force=True)
            print("Selected lunch option.")

            # 5. Submit
            print("Submitting form...")
            submit_btn = page.locator("button[type='submit']")
            submit_btn.click()
            print("Form submitted.")

            # 6. Verify Toast
            # Wait for submission delay (1.5s) + animation
            print("Waiting for toast...")

            try:
                toast = page.locator("text=Rückruf angefordert!")
                toast.wait_for(state="visible", timeout=10000)
                print("PASS: Toast notification appeared.")
            except Exception as e:
                print(f"FAIL: Toast notification not found: {e}")
                # Take screenshot for debugging
                page.screenshot(path="debug_failure.png")
                sys.exit(1)

            # Verify time text in toast
            # "Wir melden uns mittags bei Ihnen."
            # Check explicitly for the text
            if page.get_by_text("Wir melden uns mittags bei Ihnen.").count() > 0:
                 print("PASS: Toast text is correct.")
            else:
                 print("FAIL: Toast text is incorrect.")
                 print("Page content dump:")
                 print(page.content())
                 sys.exit(1)

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
