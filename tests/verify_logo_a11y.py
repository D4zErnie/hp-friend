from playwright.sync_api import sync_playwright, expect
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("http://localhost:3000/dirking.html")

            # Wait for content
            page.get_by_text("DIRKING").first.wait_for()

            # Press Tab to focus the first element
            page.keyboard.press("Tab")

            # Get focused element
            focused = page.locator("*:focus")

            # Check if it is a button (Expect FAIL initially)
            print("Checking role...")
            expect(focused).to_have_role("button")

            # Check label (Expect FAIL initially)
            print("Checking aria-label...")
            expect(focused).to_have_attribute("aria-label", "Zur Startseite")

            print("SUCCESS: Logo is accessible")
            page.screenshot(path="tests/success_logo_focus.png")
        except Exception as e:
            print(f"FAILURE: {e}")
            page.screenshot(path="tests/failure.png")
            # Create a failure indicator file or just exit 1
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
