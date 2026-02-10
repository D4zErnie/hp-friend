import sys
import time
from playwright.sync_api import sync_playwright

def verify_watchlist_persistence():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 720})
        page = context.new_page()

        try:
            print("Navigating to home...")
            page.goto('http://localhost:3000/dirking.html')

            print("Navigating to Private Page...")
            page.locator('nav').get_by_text("Privat", exact=True).click()
            time.sleep(1)

            print("Adding item to watchlist...")
            bookmark_btn = page.locator('button[aria-label="Auf Merkliste setzen"]').first
            bookmark_btn.click()

            item_name = "Hausrat & Gebäude" # First item

            # Verify added
            badge = page.locator('nav').get_by_text("1", exact=True).first
            if not badge.is_visible():
                print("FAILED: Badge not visible initially")
                sys.exit(1)

            print("Reloading page...")
            page.reload()
            time.sleep(1)

            print("Verifying persistence...")
            # Check badge again
            # Note: without persistence, this will fail
            badge = page.locator('nav').get_by_text("1", exact=True).first
            if not badge.is_visible():
                print("FAILED: Badge lost after reload (Persistence Failed)")
                sys.exit(1)

            print("Navigating to Contact Page...")
            page.locator('nav').locator('button', has_text="Kontakt").first.click()
            time.sleep(1)

            if not page.get_by_text(item_name).is_visible():
                print(f"FAILED: Item '{item_name}' not visible after reload")
                sys.exit(1)

            # Test Clear All Button (which we will add)
            print("Testing Clear All button...")
            # We expect a button with text "Alle löschen"
            clear_btn = page.get_by_text("Alle löschen")
            if not clear_btn.is_visible():
                print("FAILED: 'Alle löschen' button not visible")
                sys.exit(1)

            clear_btn.click()
            time.sleep(0.5)

            if page.get_by_text(item_name).is_visible():
                print(f"FAILED: Item '{item_name}' still visible after Clear All")
                sys.exit(1)

            # The section is conditional on savedServices.length > 0
            if page.get_by_text("Ihre Merkliste").is_visible():
                 print("FAILED: 'Ihre Merkliste' section still visible (should be hidden if empty)")
                 sys.exit(1)

            print("SUCCESS: Watchlist persistence and Clear All verified!")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Don't print stack trace for expected failures during dev, just the error
            # import traceback
            # traceback.print_exc()
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    verify_watchlist_persistence()
