from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Ensure verification directory exists
        os.makedirs("verification", exist_ok=True)

        try:
            print("Navigating to http://localhost:3000/dirking.html")
            page.goto("http://localhost:3000/dirking.html")
            page.wait_for_selector("#root")

            # 1. Desktop Home Active
            page.set_viewport_size({"width": 1280, "height": 800})
            page.wait_for_timeout(500)
            page.screenshot(path="verification/desktop_home_active.png")
            print("Captured desktop_home_active.png")

            # 2. Desktop Private Active
            # Use specific selector for desktop nav button to avoid ambiguity
            page.click("nav div.hidden.md\\:flex button:has-text('Privat')")
            page.wait_for_timeout(500)
            page.screenshot(path="verification/desktop_private_active.png")
            print("Captured desktop_private_active.png")

            # 3. Mobile Home Active
            page.set_viewport_size({"width": 375, "height": 667})
            page.reload() # Reload to reset state to home
            page.wait_for_selector("#root")
            page.wait_for_timeout(500)

            # Open menu
            page.click("button[aria-label='Menü öffnen']")
            page.wait_for_selector("nav .md\\:hidden.bg-white.border-t")
            page.wait_for_timeout(500) # Wait for animation/render

            page.screenshot(path="verification/mobile_home_active.png")
            print("Captured mobile_home_active.png")

            # 4. Mobile Private Active
            # Click Private in mobile menu
            page.click("nav .md\\:hidden.bg-white.border-t >> button:has-text('Privat')")
            page.wait_for_timeout(500)

            # Re-open menu to see active state (navigating closes it)
            page.click("button[aria-label='Menü öffnen']")
            page.wait_for_selector("nav .md\\:hidden.bg-white.border-t")
            page.wait_for_timeout(500)

            page.screenshot(path="verification/mobile_private_active.png")
            print("Captured mobile_private_active.png")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    run()
