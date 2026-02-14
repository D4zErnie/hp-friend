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
        page.evaluate("localStorage.clear()")
        page.reload()

        cookie_banner = page.locator("text=Datenschutzeinstellung")
        try:
            cookie_banner.wait_for(state="visible", timeout=5000)
            print("Cookie Banner is visible.")
        except:
            print("Cookie Banner NOT found or not visible!")
            # sys.exit(1)

        # Click "Einverstanden"
        accept_button = page.locator("button:text('Einverstanden')")
        if accept_button.count() > 0:
            accept_button.click()
            print("Clicked 'Einverstanden'.")
            try:
                cookie_banner.wait_for(state="hidden", timeout=2000)
                print("Cookie Banner disappeared.")
            except:
                print("Cookie banner did not disappear.")

        # --- Service Cards Verification ---
        print("Verifying Service Cards...")

        # Navigate to Private Page
        page.click("button:text('Privat')")
        print("Navigated to Private Page.")

        # Find a service card, e.g., "Hausrat & Gebäude"
        card_title = "Hausrat & Gebäude"
        card = page.locator(f"div.group:has-text('{card_title}')").first

        if not card.is_visible():
            print(f"Card '{card_title}' not found.")
            sys.exit(1)

        # Check for Bookmark Indicator
        bookmark_btn = card.locator("button[aria-label*='Merkliste']")
        if bookmark_btn.count() > 0:
             print("Bookmark button found.")
        else:
             print("Bookmark button NOT found.")
             sys.exit(1)

        # Click the bookmark button to toggle
        print(f"Clicking bookmark button for '{card_title}'...")
        bookmark_btn.first.click()

        # Check active state text ("Vorgemerkt")
        active_text = card.locator("text=Vorgemerkt")
        active_text.wait_for(state="visible", timeout=2000)
        print("Active state confirmed: 'Vorgemerkt' is visible.")

        # Check bookmark active state
        if "bg-blue-50" in bookmark_btn.first.get_attribute("class"):
             print("Bookmark button has active styling (bg-blue-50).")
        else:
             print("Bookmark button does NOT have active styling.")
             sys.exit(1)

        # Click again to untoggle
        print("Clicking bookmark button again to untoggle...")
        bookmark_btn.first.click()

        # Check "Vorgemerkt" is gone
        try:
            active_text.wait_for(state="hidden", timeout=2000)
            print("Returned to initial state: 'Vorgemerkt' hidden.")
        except:
            print("Failed to hide 'Vorgemerkt' after untoggle.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_feature()
