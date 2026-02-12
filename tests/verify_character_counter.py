from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")

        # --- Test Contact Page ---
        print("Navigating to Contact page...")
        # Try finding the contact button in nav, handling potential ambiguity
        page.locator("nav").get_by_text("Kontakt").first.click()
        page.wait_for_selector("form")

        print("Testing Contact Page Character Counter...")
        message_input = page.locator("textarea[name='message']")
        message_input.fill("Hello")

        # Check for counter text
        # Expect "5 / 3000 Zeichen"
        # We look for the text explicitly.
        # Note: The component renders "{current} / {max} Zeichen"
        counter = page.locator("text=5 / 3000 Zeichen")

        # Wait a bit for React to update if needed (though sync usually works)
        page.wait_for_timeout(500)

        if counter.count() > 0:
            print("PASS: Contact page counter updated correctly.")
        else:
            print("FAIL: Contact page counter not found or incorrect.")
            # Debug: print all text content of the parent container
            # The parent of textarea should contain the counter
            print(f"Container text: {message_input.locator('..').text_content()}")
            exit(1)

        # --- Test Claim Page ---
        print("Navigating to Claim page...")
        # Use footer link to be safe
        page.locator("footer").get_by_text("Schaden melden").click()

        # Wait for the claim form header
        page.get_by_role("heading", name="Schaden melden").wait_for()

        print("Testing Claim Page Character Counter...")
        # The placeholder is unique enough
        desc_input = page.locator("textarea[placeholder*='Was ist passiert?']")
        desc_input.fill("Damage report") # 13 chars

        # Expect "13 / 3000 Zeichen"
        counter_claim = page.locator("text=13 / 3000 Zeichen")

        page.wait_for_timeout(500)

        if counter_claim.count() > 0:
            print("PASS: Claim page counter updated correctly.")
        else:
            print("FAIL: Claim page counter not found or incorrect.")
            print(f"Container text: {desc_input.locator('..').text_content()}")
            exit(1)

        print("SUCCESS: All character counters verified.")
        browser.close()

if __name__ == "__main__":
    run()
