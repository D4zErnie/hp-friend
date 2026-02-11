from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Use a large viewport to see the whole component
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")

        print("Navigating to Private page...")
        page.get_by_text("Privat", exact=True).first.click()

        # Wait for transition
        time.sleep(1)

        print("Interacting with Quick Estimator...")
        # Scroll to the estimator
        estimator = page.locator("div.bg-slate-900").filter(has_text="Geschätzter Jahresbeitrag")
        estimator.scroll_into_view_if_needed()

        # Change slider value to 100
        slider = page.locator("input[type='range']")
        slider.evaluate("""
            e => {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                nativeInputValueSetter.call(e, 100);
                e.dispatchEvent(new Event('input', { bubbles: true }));
                e.dispatchEvent(new Event('change', { bubbles: true }));
            }
        """)

        time.sleep(1)

        # Take screenshot of the component area
        print("Taking screenshot...")
        if not os.path.exists("verification"):
            os.makedirs("verification")

        # Screenshot the whole page or just the component? The component is better.
        # But let's take the whole viewport to see context.
        page.screenshot(path="verification/quick_estimator.png")

        # Also screenshot just the component for detail
        estimator.screenshot(path="verification/quick_estimator_component.png")

        print("Screenshots saved to verification/")
        browser.close()

if __name__ == "__main__":
    run()
