from playwright.sync_api import sync_playwright
import time
import os

PORT = 3000

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                return

            page.wait_for_timeout(2000) # Wait for React to mount

            # check if title is correct
            title = page.title()
            print(f"Page title: {title}")

            # check if content exists
            header = page.locator("h1").first
            try:
                header.wait_for(timeout=5000)
                print(f"Header text: {header.inner_text()}")
            except:
                print("Header not found (timeout)")

            # verify navigation if header found
            if header.is_visible():
                page.click("text=Kontakt")
                page.wait_for_selector("form")
                print("Navigated to Contact page")

                screenshot_path = "verification/after_fix.png"
                os.makedirs("verification", exist_ok=True)
                page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error: {e}")
            console_errors.append(str(e))

        if console_errors:
            print("Console Errors found:")
            for err in console_errors:
                print(f"- {err}")
        else:
            print("No console errors found.")

        browser.close()

if __name__ == "__main__":
    run_test()
