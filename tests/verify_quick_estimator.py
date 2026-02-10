from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")

        # Wait for React to mount
        page.wait_for_timeout(1000)

        print("Navigating to Private page...")
        page.get_by_text("Privat", exact=True).first.click()

        # Wait for page transition
        page.wait_for_timeout(500)

        print("Checking for Quick Estimator...")
        # Scope to the estimator card
        price_container = page.locator("div.bg-slate-900").filter(has_text="Geschätzter Jahresbeitrag")
        price_display = price_container.locator(".text-5xl")

        if not price_display.is_visible():
             # Fallback
             print("Locating price via text-5xl only...")
             price_display = page.locator(".text-5xl", has_text=",00")

        print("Checking initial calculation...")
        # Default 60 sqm * 650 * 0.002 = 78
        initial_price = price_display.inner_text().strip()
        print(f"Initial price: {initial_price}")
        if "78,00" not in initial_price:
             print(f"FAIL: Expected ~78,00, got {initial_price}")

        print("Adjusting slider...")
        slider = page.locator("input[type='range']")

        # Set to 100 sqm
        # 100 * 650 * 0.002 = 130
        slider.evaluate("""
            e => {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                nativeInputValueSetter.call(e, 100);
                e.dispatchEvent(new Event('input', { bubbles: true }));
                e.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

        # Wait for react update
        page.wait_for_timeout(1000)

        new_price = price_display.inner_text().strip()
        print(f"New price: {new_price}")

        if "130,00" not in new_price:
             print(f"FAIL: Expected ~130,00, got {new_price}")
             exit(1)

        print("Clicking Lock Price button...")
        page.get_by_text("Preis jetzt sichern").click()

        print("Verifying navigation to Contact...")
        page.wait_for_timeout(500)
        # Check if we are on contact page. "Lernen wir uns kennen" header.
        if not page.locator("h1", has_text="Lernen wir uns kennen").is_visible():
             print("FAIL: Did not navigate to Contact page")
             exit(1)

        print("SUCCESS: Quick Estimator works as expected.")
        browser.close()

if __name__ == "__main__":
    run()
