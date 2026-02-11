
from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        try:
            # Navigate to the page
            page.goto("http://localhost:3000/dirking.html")

            # Wait for hydration
            page.wait_for_selector("#root", state="attached")
            # Wait for potential lazy loading or rendering
            page.wait_for_timeout(2000)

            # Check for console errors
            if console_errors:
                print("FAILED: Console errors found:")
                for err in console_errors:
                    print(f"- {err}")
                sys.exit(1)

            # Check if SVGs are rendered
            # We look for SVGs that are NOT the logo (which is inline SVG in source)
            # The logo uses <svg ...><circle ...></svg>
            # The lucide icons use <svg ... class="lucide lucide-...">

            # Helper to check if any lucide icon is rendered
            # We look for the 'menu' icon (hamburger) which is visible on mobile,
            # OR the 'shield' icon in the header on desktop.

            # Let's look for any SVG with stroke="currentColor" (standard for Lucide icons in this app)
            # This distinguishes them from the logo which doesn't have this attribute.
            lucide_icons_count = page.evaluate("""() => {
                return document.querySelectorAll('svg[stroke="currentColor"]').length;
            }""")

            if lucide_icons_count == 0:
                print("FAILED: No Lucide icons found rendered on the page.")
                sys.exit(1)

            print(f"SUCCESS: Found {lucide_icons_count} Lucide icons rendered.")

        except Exception as e:
            print(f"FAILED: Exception during test: {e}")
            sys.exit(1)

        browser.close()

if __name__ == "__main__":
    run()
