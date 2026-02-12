from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")

        # --- Contact Page ---
        print("Navigating to Contact page...")
        page.get_by_text("Kontakt").first.click()
        page.wait_for_selector("textarea[name='message']")

        message_input = page.locator("textarea[name='message']")
        message_input.fill("Hello World") # 11 chars

        # Scroll to view
        message_input.scroll_into_view_if_needed()

        # Take screenshot of the form area
        print("Taking screenshot of Contact form...")
        # Locate the container of the textarea (parent of textarea's parent div)
        # The structure is: div > (label, textarea, counter)
        # So we can screenshot the parent div.

        # Let's just screenshot the whole form
        form = page.locator("form")
        form.screenshot(path="verification/contact_counter.png")

        # --- Claim Page ---
        print("Navigating to Claim page...")
        page.locator("footer").get_by_text("Schaden melden").click()
        page.wait_for_selector("textarea[placeholder*='Was ist passiert?']")

        desc_input = page.locator("textarea[placeholder*='Was ist passiert?']")
        desc_input.fill("Roof damage") # 11 chars

        # Scroll to view
        desc_input.scroll_into_view_if_needed()

        print("Taking screenshot of Claim form...")
        # Screenshot the claim form
        # Need to be specific as there might be other forms? No, ClaimWizard has a form.
        # Sticky callback has a form too but it's hidden usually.
        # Let's target the visible form.
        visible_form = page.locator("form").filter(has_text="Art des Schadens").first
        visible_form.screenshot(path="verification/claim_counter.png")

        browser.close()

if __name__ == "__main__":
    run()
