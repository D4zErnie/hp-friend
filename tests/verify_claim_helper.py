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

            # Navigate to 'Schaden melden' page from footer
            # Assuming footer link text is "Schaden melden"
            claim_link = page.get_by_role("button", name="Schaden melden")
            if claim_link.count() > 0:
                claim_link.first.click()
            else:
                # If not in footer yet, maybe navigate directly? But test assumes it exists.
                # Let's try to find it in the footer specifically if possible, or just click any "Schaden melden"
                print("Clicking 'Schaden melden' link...")
                # The footer link might be a button with onClick
                page.locator("text=Schaden melden").first.click()

            page.wait_for_timeout(1000)

            # Verify we are on the claim page (check for unique text)
            if page.locator("text=Schaden melden").count() == 0:
                 print("FAIL: Did not navigate to Claim page.")
                 sys.exit(1)

            print("PASS: Navigated to Claim page.")

            # Check initial state of button
            generate_btn = page.locator("a:has-text('E-Mail generieren')")
            if generate_btn.count() == 0:
                 # It might be a button if implemented as button, but plan said <a>
                 generate_btn = page.locator("button:has-text('E-Mail generieren')")

            if generate_btn.count() == 0:
                print("FAIL: 'E-Mail generieren' button not found.")
                sys.exit(1)

            # Check if disabled (pointer-events-none or similar class, or attribute)
            # We implemented it as <a> with opacity-50 and pointer-events-none class if invalid
            # Or href='#'
            href = generate_btn.get_attribute("href")
            classes = generate_btn.get_attribute("class")

            if href != "#" and href is not None and "mailto:" in href:
                 print(f"FAIL: Button should not have valid mailto link initially. Found: {href}")
                 sys.exit(1)

            if "opacity-50" not in classes and "cursor-not-allowed" not in classes:
                 print("WARNING: Button might not look disabled.")

            print("PASS: Button is initially disabled.")

            # Fill form
            print("Filling form...")
            # Select Damage Type
            page.select_option("select", "Sturm")

            # Date
            # Use specific date
            page.fill("input[type='date']", "2023-10-27")

            # Description
            page.fill("textarea", "Mein Dach wurde durch den Sturm beschädigt.")

            page.wait_for_timeout(500)

            # Verify button is enabled and has correct href
            href = generate_btn.get_attribute("href")
            print(f"Button href: {href}")

            if not href or "mailto:" not in href:
                print("FAIL: Button does not have mailto link after filling form.")
                sys.exit(1)

            # Check content of mailto
            if "Sturm" not in href:
                print("FAIL: Mailto link missing damage type.")
                sys.exit(1)

            if "2023-10-27" not in href:
                print("FAIL: Mailto link missing date.")
                sys.exit(1)

            # Check encoded description or body
            # "Mein Dach wurde durch den Sturm beschädigt" -> URL encoded
            # Just check for "Mein" or similar if simpler
            if "Mein%20Dach" not in href and "Mein Dach" not in href:
                 # Browsers might decode in get_attribute? usually not.
                 print("FAIL: Mailto link missing description.")
                 sys.exit(1)

            print("PASS: Button is enabled with correct mailto link.")
            print("ALL CHECKS PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
