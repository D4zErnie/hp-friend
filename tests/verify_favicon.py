import sys
from playwright.sync_api import sync_playwright

def run(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            response = page.goto(page_url)
            if not response or response.status != 200:
                print(f"Error: Could not load page {page_url} (status: {response.status if response else 'None'})")
                sys.exit(1)

            # Check link tag
            link = page.locator('link[rel="icon"]')
            if link.count() == 0:
                print("Error: No favicon link found.")
                sys.exit(1)

            href = link.get_attribute("href")
            print(f"Favicon href found: {href}")

            if href != "./favicon.png":
                print(f"Error: Expected './favicon.png', found '{href}'")
                sys.exit(1)

            # Verify fetching the favicon via fetch inside the page context
            # This ensures relative paths are resolved correctly relative to the page
            status = page.evaluate("""async () => {
                const response = await fetch('./favicon.png');
                return response.status;
            }""")

            print(f"Favicon fetch status: {status}")
            if status != 200:
                print(f"Error: Favicon returned non-200 status: {status}")
                sys.exit(1)

        except Exception as e:
            print(f"Exception during verification: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    url = "http://localhost:3000/dirking.html"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    run(url)
