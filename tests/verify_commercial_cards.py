import sys
import os
from playwright.sync_api import sync_playwright, expect

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

        # Dismiss cookie banner
        try:
            page.click("button:text('Einverstanden')")
        except:
            pass

        # Navigate to Commercial Page
        page.click("button:text('Gewerbe')")
        print("Navigated to Commercial Page.")

        # Find a service card, e.g., "Betriebshaftpflicht"
        card_title = "Betriebshaftpflicht"

        # Robust locator strategy
        # Find the card front that contains the title
        card_front = page.locator(f".card-front:has(h3:has-text('{card_title}'))").first

        if not card_front.is_visible():
            print(f"Card '{card_title}' not found.")
            sys.exit(1)

        # 1. Verify "Infos" button exists
        infos_btn = card_front.locator("button").filter(has_text="Infos").first
        if infos_btn.is_visible():
            print("'Infos' button found.")
        else:
            print("'Infos' button NOT found.")
            print(f"Card HTML: {card_front.inner_html()}")
            sys.exit(1)

        # 2. Verify Bookmark button hover effect
        bookmark_btn = card_front.locator("button[aria-label*='auf Merkliste setzen']")
        if not bookmark_btn.is_visible():
             print("Bookmark button not found.")
             sys.exit(1)

        # Check for + Merkliste span (it might be a sibling now)
        # We look in the parent container
        bookmark_container = bookmark_btn.locator("xpath=..")
        print(f"Bookmark Container HTML: {bookmark_container.inner_html()}")

        merkliste_span = bookmark_container.locator("span:has-text('+ Merkliste')")

        if merkliste_span.count() > 0:
            print("'+ Merkliste' span found.")
        else:
            print("'+ Merkliste' span NOT found.")
            sys.exit(1)

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_commercial()
