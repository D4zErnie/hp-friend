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

        # 1. Click Infos to flip
        print("Clicking 'Infos'...")
        infos_btn = card_front.locator("button").filter(has_text="Infos").first
        infos_btn.click()

        # Wait for flip
        page.wait_for_timeout(1000)

        # Find the inner container
        card_inner = card_front.locator("xpath=..")

        # Check class on inner
        if "rotate-y-180" in card_inner.get_attribute("class"):
            print("Card flipped (rotate-y-180 present).")
        else:
            print("Card DID NOT flip.")
            sys.exit(1)

        # 2. Verify Bookmark button on Back Side
        # The back side is now visible.
        # We need to find the bookmark container on the back side.
        # card_inner is the container.
        card_back = card_inner.locator(".card-back")

        bookmark_btn_back = card_back.locator("button[aria-label*='auf Merkliste setzen']")
        if not bookmark_btn_back.is_visible():
             print("Bookmark button (back) not found.")
             sys.exit(1)

        # Check for + Merkliste span (it might be a sibling now)
        bookmark_container_back = bookmark_btn_back.locator("xpath=..")
        merkliste_span_back = bookmark_container_back.locator("span:has-text('+ Merkliste')")

        # Check opacity or visibility
        # It should exist in DOM if !isSaved (which is default)
        if merkliste_span_back.count() == 0:
            print("'+ Merkliste' span (back) NOT found in DOM.")
            sys.exit(1)

        # Check computed opacity
        opacity = float(merkliste_span_back.evaluate("el => window.getComputedStyle(el).opacity"))
        print(f"Initial Opacity of '+ Merkliste' (back): {opacity}")

        if opacity > 0:
             print("FAIL: '+ Merkliste' (back) is visible without hover!")
             sys.exit(1)
        else:
             print("PASS: '+ Merkliste' (back) is hidden initially.")

        # Hover over the bookmark container
        print("Hovering over bookmark container (back)...")
        bookmark_container_back.hover()
        page.wait_for_timeout(500) # Wait for transition

        opacity_hover = float(merkliste_span_back.evaluate("el => window.getComputedStyle(el).opacity"))
        print(f"Hover Opacity of '+ Merkliste' (back): {opacity_hover}")

        if opacity_hover < 1:
             print("FAIL: '+ Merkliste' (back) is NOT visible on hover!")
             sys.exit(1)
        else:
             print("PASS: '+ Merkliste' (back) is visible on hover.")

        print("Verification SUCCESS!")
        browser.close()

if __name__ == "__main__":
    verify_commercial()
