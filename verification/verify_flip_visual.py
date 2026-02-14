import sys
import os
from playwright.sync_api import sync_playwright

def verify_flip_visual():
    print("Starting visual verification for Flip Cards...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a reasonable desktop size
        page = browser.new_page(viewport={"width": 1280, "height": 800})

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

        # Navigate to Private Page
        page.click("button:text('Privat')")
        print("Navigated to Private Page.")
        page.wait_for_timeout(1000)

        # Find the first SERVICE card (has .flip-card-inner)
        card = page.locator(".group:has(.flip-card-inner)").first

        # Scroll to card
        card.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

        # Take screenshot of initial state (Front)
        # We assume card is found. If not, next line fails.
        if card.count() == 0:
            print("Card not found!")
            sys.exit(1)

        page.screenshot(path="verification/card_front.png", clip=card.bounding_box())
        print("Captured card_front.png")

        # Click "Infos"
        infos_btn = card.locator("button:has-text('Infos')")
        infos_btn.click()
        page.wait_for_timeout(1000) # Wait for animation (500ms duration)

        # Take screenshot of flipped state (Back)
        page.screenshot(path="verification/card_back.png", clip=card.bounding_box())
        print("Captured card_back.png")

        # Click "Zurück"
        back_btn = card.locator("button:has-text('Zurück')")
        back_btn.click()
        page.wait_for_timeout(1000) # Wait for animation

        # Take screenshot of final state (Front again)
        page.screenshot(path="verification/card_front_after.png", clip=card.bounding_box())
        print("Captured card_front_after.png")

        browser.close()

if __name__ == "__main__":
    verify_flip_visual()
