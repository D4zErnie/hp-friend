from playwright.sync_api import sync_playwright

def verify_render():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Go to local server
        page.goto("http://localhost:3000/dirking.html")

        # Wait for the page to be ready (look for footer or sticky callback)
        page.wait_for_selector("footer")

        # Scroll to bottom to see footer
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

        # Take screenshot of the bottom of the page
        page.screenshot(path="verification/render_check.png")

        browser.close()

if __name__ == "__main__":
    verify_render()
