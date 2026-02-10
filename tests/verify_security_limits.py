from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:3000/dirking.html")

        # Navigate to Contact page
        page.get_by_text("Kontakt").first.click()
        page.wait_for_selector("form")

        name_input = page.locator("input[name='name']")

        # Create a long string (200 chars)
        long_string = "a" * 200

        # Simulate bypass: dispatch input event with long value
        # This bypasses the HTML maxLength attribute but triggers React's onChange
        page.evaluate(f"""
            const input = document.querySelector("input[name='name']");
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(input, "{long_string}");
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        """)

        # Wait for React to process the event and potentially reset the value
        page.wait_for_timeout(500)

        current_value = name_input.input_value()
        print(f"Current value length: {len(current_value)}")

        if len(current_value) > 100:
            print("FAIL: Input accepted > 100 chars (Bypass successful).")
            sys.exit(1)
        else:
            print("PASS: Input was rejected or truncated to limit.")
            sys.exit(0)

        browser.close()

if __name__ == "__main__":
    run()
