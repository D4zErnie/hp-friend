
from playwright.sync_api import sync_playwright
import time
import os

PORT = 3000
URL = f"http://localhost:{PORT}/dirking.html"

def benchmark():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            print(f"Navigating to {URL}")
            page.goto(URL)
            page.wait_for_selector("footer", timeout=10000)

            # Dismiss cookie banner if present
            try:
                if page.is_visible("text=Einverstanden"):
                    page.click("text=Einverstanden")
                    print("Cookie banner dismissed")
            except:
                pass

            # Navigate to Legal Page (Impressum)
            print("Navigating to Impressum...")
            # We can use the text selector for the footer link
            link = page.locator("footer >> text=Impressum")
            link.scroll_into_view_if_needed()
            link.click()

            # Wait for Legal Page to load
            page.wait_for_selector("h1:has-text('Rechtliches & Information')")
            print("Legal page loaded")

            # Benchmark: Click tabs 100 times
            tabs = ["Impressum", "Datenschutz", "Erstinformation"]
            iterations = 50

            start_time = time.time()

            for i in range(iterations):
                for tab in tabs:
                    # Click the tab button
                    # The buttons are identified by their text content
                    # We scope it to the main content area to avoid clicking footer links again if they are visible
                    button = page.locator(f"main button:has-text('{tab}')")
                    button.click()

                    # Optional: wait for something to change?
                    # The content change is synchronous in React state update, but we might want to ensure DOM update.
                    # Waiting for specific content might slow down the benchmark too much with overhead,
                    # but let's at least wait for the active state class on the button or specific header.

                    if tab == "Impressum":
                        page.wait_for_selector("h2:has-text('Impressum')", timeout=1000)
                    elif tab == "Datenschutz":
                        page.wait_for_selector("h2:has-text('Datenschutzerklärung')", timeout=1000)
                    elif tab == "Erstinformation":
                        page.wait_for_selector("h2:has-text('Erstinformation')", timeout=1000)

            end_time = time.time()
            duration = end_time - start_time

            print(f"Benchmark completed: {iterations * len(tabs)} clicks in {duration:.4f} seconds")
            print(f"Average time per click: {duration / (iterations * len(tabs)) * 1000:.2f} ms")

            # Verify functionality
            print("Verifying functionality...")
            # Check if we can still switch to Datenschutz and see content
            page.click("main button:has-text('Datenschutz')")
            if page.is_visible("h2:has-text('Datenschutzerklärung')"):
                print("SUCCESS: Datenschutz tab works")
            else:
                print("FAILURE: Datenschutz tab content not found")

        except Exception as e:
            print(f"Error during benchmark: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    benchmark()
