import sys
import os
from playwright.sync_api import sync_playwright

def verify_feature():
    print("Starting verification for Cookie Banner and Service Cards...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a desktop viewport to ensure layout is standard
        page = browser.new_page(viewport={"width": 1280, "height": 720})

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
            # Depending on environment, maybe it was accepted before.
            # But we cleared localStorage.
            sys.exit(1)

        # Verify "Infos" link click
        print("Testing 'Infos' link in Cookie Banner...")
        infos_link = page.locator("a:text('Infos')")
        infos_link.click()

        # Check if navigated to Privacy Policy (or at least triggered the action)
        # We expect to see the "Datenschutzerklärung" headline
        privacy_headline = page.locator("h2:text('Datenschutzerklärung')")
        try:
            privacy_headline.wait_for(state="visible", timeout=2000)
            print("Successfully navigated to Privacy Policy via 'Infos' link.")
        except:
            print("Failed to navigate to Privacy Policy via 'Infos' link!")
            sys.exit(1)

        # Click "Einverstanden"
        accept_button = page.locator("button:text('Einverstanden')")
        accept_button.click()
        print("Clicked 'Einverstanden'.")

        # Verify it disappears
        cookie_banner.wait_for(state="hidden", timeout=2000)
        print("Cookie Banner disappeared.")

        # --- Service Cards Verification ---
        print("Verifying Service Cards...")

        # Navigate to Private Page
        page.click("button:text('Privat')")
        print("Navigated to Private Page.")

        # Find a service card, e.g., "Hausrat & Gebäude"
        card_title = "Hausrat & Gebäude"
        # Using a more specific selector to target the card container
        card = page.locator(f"div.group:has-text('{card_title}')").first

        if not card.is_visible():
            print(f"Card '{card_title}' not found.")
            sys.exit(1)

        # Check initial state text - expecting hidden
        initial_text = card.locator("text=Auf die Merkliste")

        # Check opacity
        try:
            opacity = float(initial_text.evaluate("element => window.getComputedStyle(element).opacity"))
            if opacity < 0.1:
                print(f"Initial state correct: 'Auf die Merkliste' is hidden (opacity: {opacity}).")
            else:
                print(f"Initial state INCORRECT: 'Auf die Merkliste' is visible (opacity: {opacity}).")
                sys.exit(1)
        except Exception as e:
            print(f"Could not check opacity: {e}")
            sys.exit(1)

        # Check hover
        card.hover()
        page.wait_for_timeout(1000)

        try:
            opacity_hover = float(initial_text.evaluate("element => window.getComputedStyle(element).opacity"))
            if opacity_hover > 0.9:
                print(f"Hover state correct: 'Auf die Merkliste' became visible (opacity: {opacity_hover}).")
            else:
                print(f"Hover state INCORRECT: 'Auf die Merkliste' opacity is {opacity_hover}.")
                sys.exit(1)
        except:
            print("Error checking hover state")
            sys.exit(1)

        # Check NEW hover effect classes on icon container
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

        # Check color
        text_wrapper = card.locator("div.text-green-600")
        if text_wrapper.is_visible():
            print("Active text has green color class.")
        else:
            print("Active text does NOT have green color class.")
            sys.exit(1)

        # Click again to untoggle
        print("Clicking card again to untoggle...")
        card.click()

        # After untoggle, text returns to 'Auf die Merkliste'.
        # Since we clicked, mouse is likely hovering, so opacity should be 1.
        page.wait_for_timeout(1000)
        initial_text.wait_for(state="visible", timeout=2000)

        opacity_final = float(initial_text.evaluate("element => window.getComputedStyle(element).opacity"))
        if opacity_final > 0.9:
            print(f"Returned to initial state (hovered): visible.")
        else:
            print(f"Returned to initial state but NOT visible? Opacity: {opacity_final}")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_feature()
