import sys
import os
from playwright.sync_api import sync_playwright

def verify_feature():
    print("Starting verification for Cookie Banner and Service Cards...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
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
        card = page.locator(f"div.group:has-text('{card_title}')").first

        # Check initial state text
        initial_text = card.locator("text=Auf die Merkliste")
        if initial_text.is_visible():
            print(f"Initial state correct: 'Auf die Merkliste' found in '{card_title}' card.")
        else:
            print(f"Initial state incorrect: 'Auf die Merkliste' NOT found in '{card_title}' card.")
            sys.exit(1)

        # Check hover effect class on icon
        # The icon is inside the card. We expect `group-hover:fill-current` on the SVG or its container?
        # My implementation added `group-hover:fill-current` to the Icon component which puts it on the SVG (or path depending on implementation)
        # The Icon component returns an SVG with `className`.
        # So we look for an SVG inside the card that has `group-hover:fill-current`.
        icon_svg = card.locator("svg.group-hover\\:fill-current")
        if icon_svg.count() > 0:
             print("Icon has 'group-hover:fill-current' class.")
        else:
             print("Icon does NOT have 'group-hover:fill-current' class.")
             # Print HTML for debug
             # print(card.inner_html())
             sys.exit(1)

        # Click the card to toggle
        print(f"Clicking card '{card_title}'...")
        card.click()

        # Check active state text
        active_text = card.locator("text=Für Gespräch vorgemerkt")
        active_text.wait_for(state="visible", timeout=2000)
        print("Active state confirmed: 'Für Gespräch vorgemerkt' is visible.")

        # Check color (text-green-600)
        # We can check if the class is present on the wrapper of the text
        text_wrapper = card.locator("div.text-green-600")
        if text_wrapper.is_visible():
            print("Active text has green color class.")
        else:
            print("Active text does NOT have green color class.")
            sys.exit(1)

        # Check bookmark badge in header (optional, but good for integration test)
        header_badge = page.locator("nav button:has-text('Kontakt') span").first
        if header_badge.is_visible() and header_badge.inner_text() == "1":
             print("Header badge updated correctly.")
        else:
             print("Header badge verification failed.")

        # Click again to untoggle
        print("Clicking card again to untoggle...")
        card.click()
        initial_text.wait_for(state="visible", timeout=2000)
        print("Returned to initial state.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_feature()
