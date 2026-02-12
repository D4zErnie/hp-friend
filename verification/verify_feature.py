from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 800}) # Desktop viewport

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")
        page.wait_for_timeout(1000)

        # Dismiss cookie banner if present
        try:
            page.click("button:text('Einverstanden')", timeout=2000)
        except:
            pass

        print("Navigating to Private page...")
        page.get_by_text("Privat", exact=True).first.click()
        page.wait_for_timeout(1000)

        print("Taking screenshot of Quick Estimator...")
        # Scroll to the element to ensure it's in view
        price_container = page.locator("div.bg-slate-900").filter(has_text="Geschätzter Jahresbeitrag")
        price_container.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        page.screenshot(path="verification/quick_estimator.png")
        print("Screenshot saved to verification/quick_estimator.png")

        browser.close()

if __name__ == "__main__":
    run()
