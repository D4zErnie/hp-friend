from playwright.sync_api import sync_playwright
import sys

PORT = 3000

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                sys.exit(1)

            page.wait_for_timeout(2000) # Wait for React to mount

            # 1. Verify Cookie Banner "Infos" is a button
            print("Checking Cookie Banner 'Infos' element...")
            try:
                # Find the element with text "Infos" inside the cookie banner
                infos_el = page.locator("text=Infos").first
                infos_el.wait_for(state="visible", timeout=5000)

                tag_name = infos_el.evaluate("el => el.tagName")
                print(f"Infos element tag name: {tag_name}")

                if tag_name == "BUTTON":
                    print("PASS: Infos element is a BUTTON.")
                else:
                    print(f"FAIL: Infos element is {tag_name}, expected BUTTON.")
                    # Don't exit yet, continue to check the other improvement
            except Exception as e:
                print(f"FAIL: Cookie Banner Infos element not found: {e}")

            # 2. Verify StickyCallback Radio Focus Styles
            print("Checking StickyCallback Radio Focus Styles...")

            # Open the modal
            try:
                fab = page.locator("button[aria-label='Rückruf anfordern']")
                fab.wait_for(state="visible", timeout=5000)
                fab.click()
                print("Clicked FAB.")

                # Wait for modal
                modal = page.locator("h3:has-text('Rückruf anfordern')")
                modal.wait_for(state="visible", timeout=5000)
                print("Modal opened.")

                # Check the first radio button label (Morgens)
                # It contains text "Morgens"
                label = page.locator("label:has-text('Morgens')")
                label.wait_for(state="visible", timeout=2000)

                class_attr = label.get_attribute("class")
                print(f"Label class attribute: {class_attr}")

                if "focus-within:ring-2" in class_attr and "focus-within:ring-blue-500" in class_attr:
                    print("PASS: Label has focus-within styles.")
                else:
                    print("FAIL: Label missing focus-within styles.")

            except Exception as e:
                print(f"FAIL: StickyCallback interaction failed: {e}")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
