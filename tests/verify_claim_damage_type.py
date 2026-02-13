from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:3000/dirking.html")

        # Navigate to Claim page
        page.get_by_role("button", name="Schaden melden").first.click()
        page.wait_for_selector("form")

        # Fill other required fields with valid data
        page.fill("input[type='date']", "2023-10-27")
        page.fill("textarea", "Test description")

        # Inject an invalid option and select it
        print("Injecting invalid option 'HACK'...")
        page.evaluate("""
            const select = document.querySelector('select');
            const opt = document.createElement('option');
            opt.value = 'HACK';
            opt.text = 'HACK';
            select.add(opt);
            select.value = 'HACK';
            select.dispatchEvent(new Event('change', { bubbles: true }));
        """)

        # Wait for React to process
        page.wait_for_timeout(500)

        # Check Submit button state
        submit_btn = page.locator("#main-content button:has-text('Schaden melden')")

        if not submit_btn.is_disabled():
            print("FAIL: Submit button enabled with invalid 'HACK' value!")
            sys.exit(1)

        print("PASS: Submit button remained disabled with invalid value.")

        # Now select a valid option
        print("Selecting valid option 'Sturm'...")
        page.select_option("select", "Sturm")

        page.wait_for_timeout(500)

        if submit_btn.is_disabled():
            print("FAIL: Submit button disabled with valid 'Sturm' value!")
            sys.exit(1)

        print("PASS: Submit button enabled with valid value.")
        browser.close()

if __name__ == "__main__":
    run()
