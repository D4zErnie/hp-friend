from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")

        print("Navigating to Contact page...")
        # Use the navigation button
        page.get_by_text("Kontakt").first.click()

        # Wait for the form
        page.wait_for_selector("form")

        print("Checking input limits...")

        name_input = page.locator("input[name='name']")
        email_input = page.locator("input[name='email']")
        message_input = page.locator("textarea[name='message']")

        # Check maxLength attributes
        name_max = name_input.get_attribute("maxlength")
        email_max = email_input.get_attribute("maxlength")
        msg_max = message_input.get_attribute("maxlength")

        print(f"Name maxLength: {name_max}")
        print(f"Email maxLength: {email_max}")
        print(f"Message maxLength: {msg_max}")

        if name_max != "100":
            print("FAIL: Name input missing maxLength=100")
            exit(1)

        if email_max != "100":
            print("FAIL: Email input missing maxLength=100")
            exit(1)

        if msg_max != "3000":
            print("FAIL: Message input missing maxLength=3000")
            exit(1)

        print("SUCCESS: All inputs have correct length limits.")
        browser.close()

if __name__ == "__main__":
    run()
