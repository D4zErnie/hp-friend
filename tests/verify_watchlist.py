import sys
import time
from playwright.sync_api import sync_playwright

def verify_watchlist():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            print("Navigating to home...")
            page.goto('http://localhost:3000/dirking.html')

            # Navigate to Private Page
            print("Navigating to Private Page...")
            page.locator('nav').get_by_text("Privat", exact=True).click()
            time.sleep(1) # Wait for navigation

            # Find the first 'Merken' button and click it
            print("Clicking 'Merken' on first item...")
            # Using the new text logic for card
            bookmark_btn = page.locator('text=Auf die Merkliste').first
            bookmark_btn.click()

            # Verify badge in navigation
            print("Verifying badge in navigation...")
            # The badge contains "1"
            badge = page.locator('nav').get_by_text("1", exact=True).first
            if not badge.is_visible():
                print("FAILED: Badge not visible in navigation")
                sys.exit(1)

            # Navigate to Contact Page
            print("Navigating to Contact Page...")
            page.locator('nav').locator('button', has_text="Kontakt").first.click()
            time.sleep(1)

            # Verify "Ihre Merkliste" section exists
            print("Verifying Merkliste section...")
            if not page.locator("h3:has-text('Ihre Merkliste')").is_visible():
                print("FAILED: 'Ihre Merkliste' section not visible")
                sys.exit(1)

            # Verify the item is listed
            # We assume the first item on Private Page is "Hausrat & Gebäude"
            item_name = "Hausrat & Gebäude"
            if not page.get_by_text(item_name).is_visible():
                print(f"FAILED: Item '{item_name}' not visible in Merkliste")
                sys.exit(1)

            # Verify removing item
            print("Removing item from Merkliste...")
            remove_btn = page.locator(f'button[aria-label="{item_name} entfernen"]')
            remove_btn.click()

            # Verify item is gone
            if page.get_by_text(item_name).is_visible():
                print(f"FAILED: Item '{item_name}' still visible after removal")
                sys.exit(1)

            print("SUCCESS: Watchlist feature verified!")

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_watchlist()
