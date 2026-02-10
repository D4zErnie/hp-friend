from playwright.sync_api import sync_playwright
import sys
import time

PORT = 3000

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Use desktop viewport to ensure FAB is visible and not obscured by mobile menu
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            print(f"Navigating to http://localhost:{PORT}/dirking.html")
            response = page.goto(f"http://localhost:{PORT}/dirking.html")
            if response.status != 200:
                print(f"Failed to load page: status {response.status}")
                sys.exit(1)

            page.wait_for_timeout(2000) # Wait for React to mount

            # 1. Locate the FAB button
            fab = page.locator("button.fixed.bottom-8.right-8")
            if fab.count() == 0:
                print("FAIL: FAB button not found.")
                sys.exit(1)

            print("PASS: FAB button found.")

            # 2. Check for aria-label
            aria_label = fab.get_attribute("aria-label")
            if not aria_label:
                print("FAIL: FAB button missing 'aria-label'.")
                # We want to verify the rest of the logic too, but this is a critical failure.
                # However, for the purpose of reproducing the issue, failing here is correct.
                sys.exit(1)
            print(f"PASS: FAB button has aria-label='{aria_label}'.")

            # 3. Check tooltip visibility logic
            tooltip = fab.locator("span")
            if tooltip.count() == 0:
                print("FAIL: Tooltip span inside FAB not found.")
                sys.exit(1)

            # Check initial opacity (should be 0)
            initial_opacity = tooltip.evaluate("el => window.getComputedStyle(el).opacity")
            print(f"Initial opacity: {initial_opacity}")
            if float(initial_opacity) > 0.1:
                print("FAIL: Tooltip should be initially hidden.")
                sys.exit(1)
            print("PASS: Tooltip is initially hidden.")

            # Focus the button
            print("Focusing the button...")
            fab.focus()
            page.wait_for_timeout(500) # Wait for transition

            # Check opacity after focus
            focused_opacity = tooltip.evaluate("el => window.getComputedStyle(el).opacity")
            print(f"Opacity after focus: {focused_opacity}")

            if float(focused_opacity) < 0.9:
                print("FAIL: Tooltip should be visible on focus (opacity ~1).")
                sys.exit(1)

            print("PASS: Tooltip is visible on focus.")
            print("ALL CHECKS PASSED!")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    run()
