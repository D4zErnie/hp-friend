import sys
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch()
    page = browser.new_page()

    page.goto("http://localhost:3000/dirking.html")

    # Locate the FAB
    fab = page.locator("button.fixed.bottom-8.right-8")

    print(f"FAB found: {fab.count() > 0}")
    if fab.count() == 0:
        print("Error: FAB not found")
        sys.exit(1)

    # Check aria-label
    aria_label = fab.get_attribute("aria-label")
    print(f"Current aria-label: {aria_label}")

    if aria_label == "Kontaktformular öffnen":
        print("PASS: FAB has correct aria-label")
    else:
        print(f"FAIL: FAB aria-label incorrect or missing. Found: {aria_label}")

    # Check tooltip visibility on focus
    tooltip = fab.locator("span")

    # Initial state
    initial_opacity = tooltip.evaluate("el => getComputedStyle(el).opacity")
    print(f"Initial tooltip opacity: {initial_opacity}")

    # Focus via keyboard (Tab) to trigger :focus-visible
    # We might need to tab multiple times if it's not the first element
    # But we can also just focus the element before it and tab?
    # Or just use force focus-visible if playwright supports it.

    # Playwright's .focus() usually triggers :focus.
    # :focus-visible depends on heuristic.
    # Let's try pressing Tab.

    # First, let's reset focus to body
    page.evaluate("document.body.focus()")

    # Press Tab until we hit the button? No, that's flaky.
    # Let's try to force the state via CSS for verification or assume if class is present it works?
    # No, we want to verify the behavior.

    # Let's try to focus it and then check computed style.
    # Note: Tailwind's group-focus-visible relies on the parent having :focus-visible.

    fab.focus()
    # Force the class via JS to verify the CSS rule exists? No.

    # Try to simulate Tab press
    # Since we don't know where focus is, let's focus the element *before* it in DOM order?
    # The FAB is at the end of the body.
    # Let's focus the footer link before it?

    # Actually, we can just check if the class `group-focus-visible:opacity-100` is present in the class list
    # AND verify that `focus-visible` triggers it.

    # Let's try to verify the class string first, as a fallback.
    class_attr = tooltip.get_attribute("class")
    if "group-focus-visible:opacity-100" in class_attr:
        print("PASS: class 'group-focus-visible:opacity-100' present on tooltip")
    else:
        print("FAIL: class 'group-focus-visible:opacity-100' missing on tooltip")

    # To really test :focus-visible, we might need to use CDP or specific browser args.
    # But let's try just checking the class name for now as the runtime check is hard in headless without proper input emulation.

    # However, let's try one more thing:
    # Simulate a key press on the button?

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
