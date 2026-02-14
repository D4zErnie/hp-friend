from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto("http://localhost:3000/dirking.html")
        except Exception as e:
            print(f"Error loading page: {e}")
            sys.exit(1)

        # Dismiss cookie banner if present
        try:
            page.click("button:text('Einverstanden')", timeout=2000)
        except:
            pass

        # Navigate to Private Page
        page.click("button:text('Privat')")
        page.wait_for_selector(".group", timeout=5000)

        # Locate the first card
        # Note: .group is the container. Inside is .flip-card-inner
        # We need to be specific to avoid finding other groups (like nav items if they use group)
        # Service cards are in a grid.
        cards = page.locator(".group:has(.flip-card-inner)")
        if cards.count() == 0:
            print("No service cards found.")
            sys.exit(1)

        card = cards.first
        inner = card.locator(".flip-card-inner")

        # Check initial state (should not be flipped)
        # We check the class attribute of the inner div
        classes = inner.get_attribute("class") or ""
        if "rotate-y-180" in classes:
            print("FAILURE: Card is initially flipped!")
            sys.exit(1)
        print("Success: Card is initially not flipped.")

        # Try to find 'Infos' button
        # It should be visible on the front
        infos_btn = card.locator("button:has-text('Infos')")
        if infos_btn.count() == 0:
            print("FAILURE: 'Infos' button not found.")
            # We expect this to fail initially
            sys.exit(1)

        # Click 'Infos'
        infos_btn.click()
        page.wait_for_timeout(500)

        # Check if flipped
        classes_flipped = inner.get_attribute("class") or ""
        if "rotate-y-180" not in classes_flipped:
             print("FAILURE: Card did not flip after clicking 'Infos'.")
             sys.exit(1)
        print("Success: Card flipped after clicking 'Infos'.")

        # Try to find 'Zurück' button (on the back)
        back_btn = card.locator("button:has-text('Zurück')")
        if back_btn.count() == 0:
             print("FAILURE: 'Zurück' button not found.")
             sys.exit(1)

        # Click 'Zurück'
        # Since the card is flipped, the back button should be visible/clickable
        back_btn.click()
        page.wait_for_timeout(500)

        # Check if flipped back
        classes_back = inner.get_attribute("class") or ""
        if "rotate-y-180" in classes_back:
             print("FAILURE: Card did not flip back after clicking 'Zurück'.")
             sys.exit(1)
        print("Success: Card flipped back after clicking 'Zurück'.")

        print("ALL TESTS PASSED")
        browser.close()

if __name__ == "__main__":
    run()
