from playwright.sync_api import sync_playwright
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            print("Navigating to http://localhost:3000/dirking.html")
            page.goto("http://localhost:3000/dirking.html")
            page.wait_for_selector("#root")

            # Give React a moment to hydrate/render
            page.wait_for_timeout(1000)

            # Check Desktop Nav
            print("Checking Desktop Navigation...")
            # Note: The desktop nav is visible on wide screens, but we can query it anyway
            home_link = page.locator("nav div.hidden.md\\:flex button:has-text('Startseite')")

            if home_link.count() == 0:
                print("Could not find desktop home link. Check selectors.")
                return

            # Initial state: Home
            aria_current = home_link.get_attribute("aria-current")
            print(f"Home link aria-current: {aria_current}")

            # Navigate to Private
            print("Navigating to Private...")
            # We can use the desktop link to navigate
            home_link.click() # Ensure we are on home first? No, we are already there.

            private_link = page.locator("nav div.hidden.md\\:flex button:has-text('Privat')")
            private_link.click()
            page.wait_for_timeout(500)

            aria_current = private_link.get_attribute("aria-current")
            print(f"Private link aria-current: {aria_current}")

            # Check Mobile Nav Visuals
            print("Checking Mobile Navigation Visuals...")
            # Set viewport to mobile
            page.set_viewport_size({"width": 375, "height": 667})

            # Open Menu
            menu_button = page.locator("button[aria-label='Menü öffnen']")
            if menu_button.is_visible():
                menu_button.click()

                # Wait for the mobile menu container to appear
                mobile_menu = page.locator("nav .md\\:hidden.bg-white.border-t")
                mobile_menu.wait_for(state="visible")

                # Check Private link in mobile menu (should be active because we navigated to Private earlier)
                mobile_private_link = mobile_menu.locator("button:has-text('Privat')")
                mobile_private_link.wait_for(state="visible")

                # Check for visual class (e.g., text-blue-600 or font-bold)
                class_attr = mobile_private_link.get_attribute("class")
                print(f"Mobile Private link class: {class_attr}")

                aria_current_mobile = mobile_private_link.get_attribute("aria-current")
                print(f"Mobile Private link aria-current: {aria_current_mobile}")

                if "bg-blue-50" in class_attr and "font-bold" in class_attr:
                    print("SUCCESS: Mobile Private link has correct active styles.")
                else:
                    print("FAIL: Mobile Private link missing active styles.")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()

if __name__ == "__main__":
    run()
