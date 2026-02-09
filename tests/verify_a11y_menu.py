from playwright.sync_api import sync_playwright
import time
import sys

PORT = 3000

def run_test():
    with sync_playwright() as p:
        # Use a mobile viewport
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 375, "height": 667})

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                sys.exit(1)

            page.wait_for_timeout(2000) # Wait for React to mount

            # 1. Locate the mobile menu button
            # It has class 'md:hidden'
            menu_btn = page.locator("nav button.md\\:hidden")
            if not menu_btn.is_visible():
                print("Mobile menu button not found or not visible!")
                sys.exit(1)

            print("Mobile menu button found.")

            # 2. Check for aria-label
            aria_label = menu_btn.get_attribute("aria-label")
            if not aria_label:
                print("FAIL: Mobile menu button missing 'aria-label'.")
                sys.exit(1)
            print(f"PASS: aria-label found: '{aria_label}'")

            # 3. Check for aria-expanded
            aria_expanded = menu_btn.get_attribute("aria-expanded")
            if aria_expanded is None:
                print("FAIL: Mobile menu button missing 'aria-expanded'.")
                sys.exit(1)

            if aria_expanded != "false":
                print(f"FAIL: aria-expanded should be 'false' initially, but is '{aria_expanded}'.")
                sys.exit(1)
            print("PASS: aria-expanded is initially 'false'.")

            # 4. Check internal icon for aria-hidden="true"
            # The icon inside usually has data-lucide attribute
            icon = menu_btn.locator("i")
            if icon.count() == 0:
                 # It might be an SVG if lucide replaces it?
                 # Code says: window.lucide.createIcons();
                 # Lucide usually replaces <i> with <svg>.
                 # But the Icon component returns <i>.
                 # If lucide runs, it replaces <i> with <svg>.
                 # So we should check if <i> exists OR if <svg> exists and has aria-hidden.
                 pass

            # Let's check what's actually there.
            # If lucide runs, the <i> is replaced by <svg>.
            # The Icon component:
            # return <i data-lucide={name} className={className}></i>;
            # useEffect calls window.lucide.createIcons();

            # If replacement happens, we should look for svg.
            svg = menu_btn.locator("svg")
            if svg.count() > 0:
                print("Icon is SVG (Lucide replaced).")
                aria_hidden = svg.get_attribute("aria-hidden")
            else:
                print("Icon is <i> (Lucide might not have replaced yet?).")
                i_tag = menu_btn.locator("i")
                aria_hidden = i_tag.get_attribute("aria-hidden")

            if aria_hidden != "true":
                print(f"FAIL: Icon inside menu button missing 'aria-hidden=\"true\"'. Found: {aria_hidden}")
                sys.exit(1)
            print("PASS: Icon has aria-hidden='true'.")

            # 5. Toggle button
            print("Clicking menu button...")
            menu_btn.click()
            page.wait_for_timeout(500)

            # Check aria-expanded is now true
            aria_expanded_after = menu_btn.get_attribute("aria-expanded")
            if aria_expanded_after != "true":
                print(f"FAIL: aria-expanded should be 'true' after click, but is '{aria_expanded_after}'.")
                sys.exit(1)
            print("PASS: aria-expanded is 'true' after click.")

            print("ALL CHECKS PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()
