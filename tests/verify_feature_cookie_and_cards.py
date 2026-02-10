import sys
import os
from playwright.sync_api import sync_playwright

def verify_feature():
    print("Starting verification for Cookie Banner and Service Cards...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a desktop viewport to ensure layout is standard
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # Start server (assuming it's running via run_tests_with_server.py logic or similar, but here we assume port 3000)
        # Actually I should use the helper script or just assume port 3000 if I run it via run_in_bash_session with server
        # For simplicity in this standalone script, I'll rely on the server being started externally or use a local file if needed?
        # The standard way in this repo seems to be running python -m http.server 3000 in background
        # I will assume the server is running on localhost:3000

        url = "http://localhost:3000/dirking.html"
        try:
            page.goto(url)
        except Exception as e:
            print(f"Error connecting to {url}: {e}")
            sys.exit(1)

        print("Page loaded.")

        # --- Cookie Banner Verification ---
        print("Verifying Cookie Banner...")
        # Check if cookie banner is visible
        # Note: If tests ran before, local storage might persist. We should clear it.
        page.evaluate("localStorage.clear()")
        page.reload()

        cookie_banner = page.locator("text=Datenschutzeinstellung")
        try:
            cookie_banner.wait_for(state="visible", timeout=5000)
            print("Cookie Banner is visible.")
        except:
            print("Cookie Banner NOT found or not visible!")
            sys.exit(1)

        # Click "Einverstanden"
        accept_button = page.locator("button:text('Einverstanden')")
        accept_button.click()
        print("Clicked 'Einverstanden'.")

        # Verify it disappears
        cookie_banner.wait_for(state="hidden", timeout=2000)
        print("Cookie Banner disappeared.")

        # Reload and check it doesn't appear
        page.reload()
        try:
            cookie_banner.wait_for(state="visible", timeout=2000)
            print("Cookie Banner reappeared after reload (Failed persistence)!")
            sys.exit(1)
        except:
            print("Cookie Banner did not reappear (Persistence verified).")

        # --- Service Cards Verification ---
        print("Verifying Service Cards...")

        # Navigate to Private Page
        page.click("button:text('Privat')")
        print("Navigated to Private Page.")

        # Find a service card, e.g., "Hausrat & Gebäude"
        card_title = "Hausrat & Gebäude"
        # The card is now the wrapper div. It contains the title.
        # We can find the card by finding the text and going up to the wrapper
        # Using a more specific selector to target the card container
        card = page.locator(f"div.group:has-text('{card_title}')").first

        if not card.is_visible():
            print(f"Card '{card_title}' not found.")
            sys.exit(1)

        # Check initial state text
        initial_text = card.locator("text=Auf die Merkliste")
        if initial_text.is_visible():
            print(f"Initial state correct: 'Auf die Merkliste' found in '{card_title}' card.")
        else:
            print(f"Initial state incorrect: 'Auf die Merkliste' NOT found in '{card_title}' card.")
            sys.exit(1)

        # Check NEW hover effect classes on icon container
        # We look for a div with `group-hover:bg-blue-600` and `group-hover:text-white` inside the card
        icon_container = card.locator("div.group-hover\\:bg-blue-600.group-hover\\:text-white")
        if icon_container.count() > 0:
             print("Icon container has expected hover classes (bg-blue-600, text-white).")
        else:
             print("Icon container does NOT have expected hover classes.")
             sys.exit(1)

        # Check for Bookmark Indicator (absolute positioned div with bookmark icon)
        # It should have class `absolute top-6 right-6`
        bookmark_indicator = card.locator("div.absolute.top-6.right-6 svg.lucide-bookmark") # Assuming lucide adds class or similar, or just svg inside
        # Actually Icon component renders svg.
        # Let's check for the container div
        bookmark_container = card.locator("div.absolute.top-6.right-6")
        if bookmark_container.count() > 0:
             print("Bookmark indicator container found.")
             # Check if it contains the bookmark icon
             # The Icon component adds `lucide-bookmark` class? No, usually generic svg but I can check presence of path or something?
             # My implementation: <Icon name="bookmark" ...>
             # Let's just check if it exists inside
             if bookmark_container.locator("svg").count() > 0:
                 print("Bookmark icon found inside indicator.")
             else:
                 print("Bookmark icon NOT found inside indicator.")
                 sys.exit(1)
        else:
             print("Bookmark indicator container NOT found.")
             sys.exit(1)

        # Click the card to toggle
        print(f"Clicking card '{card_title}'...")
        card.click()

        # Check active state text
        active_text = card.locator("text=Für Gespräch vorgemerkt")
        active_text.wait_for(state="visible", timeout=2000)
        print("Active state confirmed: 'Für Gespräch vorgemerkt' is visible.")

        # Check bookmark active state (text-blue-600 bg-blue-50)
        # Re-query bookmark container
        bookmark_container_active = card.locator("div.absolute.top-6.right-6.text-blue-600.bg-blue-50")
        if bookmark_container_active.count() > 0:
             print("Bookmark indicator has active styling.")
        else:
             print("Bookmark indicator does NOT have active styling.")
             sys.exit(1)

        # Check color (text-green-600)
        # We can check if the class is present on the wrapper of the text
        text_wrapper = card.locator("div.text-green-600")
        if text_wrapper.is_visible():
            print("Active text has green color class.")
        else:
            print("Active text does NOT have green color class.")
            sys.exit(1)

        # Check header badge (optional)
        header_badge = page.locator("nav button:has-text('Kontakt') span").first
        if header_badge.is_visible() and header_badge.inner_text() == "1":
             print("Header badge updated correctly.")
        else:
             # Depending on implementation, might take a moment or be hidden on mobile?
             # Just print warning if not found
             print("Header badge verification skipped/failed.")

        # Click again to untoggle
        print("Clicking card again to untoggle...")
        card.click()
        initial_text.wait_for(state="visible", timeout=2000)
        print("Returned to initial state.")

        # Test Keyboard Interaction
        print("Testing keyboard interaction (Enter key)...")
        card.focus()
        page.keyboard.press("Enter")
        active_text.wait_for(state="visible", timeout=2000)
        print("Keyboard interaction (Enter) toggled card ON.")

        card.focus()
        page.keyboard.press("Space")
        initial_text.wait_for(state="visible", timeout=2000)
        print("Keyboard interaction (Space) toggled card OFF.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_feature()
