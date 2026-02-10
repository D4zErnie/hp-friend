import sys
import os
from playwright.sync_api import sync_playwright

def verify_commercial():
    print("Starting verification for Commercial Cards...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        url = "http://localhost:3000/dirking.html"
        try:
            page.goto(url)
        except Exception as e:
            print(f"Error connecting to {url}: {e}")
            sys.exit(1)

        print("Page loaded.")

        # Navigate to Commercial Page
        page.click("button:text('Gewerbe')")
        print("Navigated to Commercial Page.")

        # Find a service card, e.g., "Betriebshaftpflicht"
        card_title = "Betriebshaftpflicht"
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

        # Check for Bookmark Indicator
        bookmark_container = card.locator("div.absolute.top-6.right-6")
        if bookmark_container.count() > 0:
             print("Bookmark indicator container found.")
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

        # Check bookmark active state
        bookmark_container_active = card.locator("div.absolute.top-6.right-6.text-blue-600.bg-blue-50")
        if bookmark_container_active.count() > 0:
             print("Bookmark indicator has active styling.")
        else:
             print("Bookmark indicator does NOT have active styling.")
             sys.exit(1)

        # Check active text color
        text_wrapper = card.locator("div.text-green-600")
        if text_wrapper.is_visible():
            print("Active text has green color class.")
        else:
            print("Active text does NOT have green color class.")
            sys.exit(1)

        # Test Keyboard Interaction
        print("Testing keyboard interaction (Enter key)...")
        # Toggle OFF first via click
        card.click()
        initial_text.wait_for(state="visible", timeout=2000)

        # Toggle ON via Enter
        card.focus()
        page.keyboard.press("Enter")
        active_text.wait_for(state="visible", timeout=2000)
        print("Keyboard interaction (Enter) toggled card ON.")

        # Toggle OFF via Space
        card.focus()
        page.keyboard.press("Space")
        initial_text.wait_for(state="visible", timeout=2000)
        print("Keyboard interaction (Space) toggled card OFF.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_commercial()
