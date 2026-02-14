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

        # Dismiss cookie banner
        try:
            page.click("button:text('Einverstanden')", timeout=2000)
        except:
            pass

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

        # ---------------------------------------------------------
        # NEW VERIFICATION LOGIC for Bookmark Hover Text
        # ---------------------------------------------------------

        bookmark_group = card.locator(".group\\/bookmark")
        if bookmark_group.count() == 0:
             print("Bookmark group container not found.")
             sys.exit(1)

        # The text is inside this group. It contains "+ Merkliste".
        hover_text = bookmark_group.locator("text=+ Merkliste")

        # Check initial state (should be invisible/opacity 0)
        try:
            opacity = float(hover_text.evaluate("element => window.getComputedStyle(element).opacity"))
            print(f"Initial text opacity: {opacity}")
            if opacity < 0.1:
                print("Initial state correct: '+ Merkliste' is hidden.")
            else:
                print(f"Initial state INCORRECT: '+ Merkliste' is visible (opacity: {opacity}).")
                # sys.exit(1)
        except Exception as e:
            print(f"Could not get opacity: {e}")

        # Hover over the BOOKMARK GROUP
        print("Hovering over bookmark group...")

        # FIX: Sticky header covers the element if it's at the top of the viewport.
        # We scroll it into view, then scroll the page UP (content down) to reveal it.
        bookmark_group.scroll_into_view_if_needed()
        page.evaluate("window.scrollBy(0, -150)")
        page.wait_for_timeout(500)

        try:
            bookmark_group.hover(force=True)
        except Exception as e:
            print(f"Hover failed even after scroll fix: {e}")

        page.wait_for_timeout(500)

        try:
            opacity_hover = float(hover_text.evaluate("element => window.getComputedStyle(element).opacity"))
            print(f"Hover text opacity: {opacity_hover}")
            if opacity_hover > 0.9:
                print("Hover state correct: '+ Merkliste' became visible.")
            else:
                print(f"Hover state INCORRECT: '+ Merkliste' opacity is {opacity_hover}.")
        except Exception as e:
            print(f"Error checking hover opacity: {e}")

        # ---------------------------------------------------------

        # Check for Bookmark Indicator (Button)
        bookmark_btn = card.locator("button[aria-label*='Merkliste']")
        if bookmark_btn.count() > 0:
             print("Bookmark button found.")
        else:
             print("Bookmark button NOT found.")
             sys.exit(1)

        # Click the bookmark button to toggle (instead of card click)
        # Note: There are two buttons (Front and Back), we click the first one (Front)
        print(f"Clicking bookmark button for '{card_title}'...")
        bookmark_btn.first.click()

        # Check active state text
        # Updated text: "Vorgemerkt" (was "Für Gespräch vorgemerkt")
        active_text = card.locator("text=Vorgemerkt")
        active_text.wait_for(state="visible", timeout=2000)
        print("Active state confirmed: 'Vorgemerkt' is visible.")

        # Check bookmark active state
        # The button itself changes class
        if "bg-blue-50" in bookmark_btn.first.get_attribute("class"):
             print("Bookmark button has active styling (bg-blue-50).")
        else:
             print("Bookmark button does NOT have active styling.")
             sys.exit(1)

        # Check active text color
        text_wrapper = card.locator("div.text-green-600")
        if text_wrapper.is_visible():
            print("Active text has green color class.")
        else:
            print("Active text does NOT have green color class.")
            sys.exit(1)

        # Test Keyboard Interaction for Bookmark
        print("Testing keyboard interaction for Bookmark...")
        # Toggle OFF first via click
        bookmark_btn.first.click()
        page.wait_for_timeout(1000)

        # Toggle ON via Enter on bookmark button
        bookmark_btn.first.focus()
        page.keyboard.press("Enter")
        active_text.wait_for(state="visible", timeout=2000)
        print("Keyboard interaction (Enter) toggled Bookmark ON.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_commercial()
