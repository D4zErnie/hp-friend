from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1280, 'height': 800})

        print("Navigating to home page...")
        page.goto("http://localhost:3000/dirking.html")
        page.wait_for_timeout(1000)

        print("Navigating to Private page...")
        page.get_by_text("Privat", exact=True).first.click()
        page.wait_for_timeout(1000)

        print("Scrolling to Quick Estimator...")
        estimator = page.locator("div.bg-slate-900").filter(has_text="Hausrat-Schnellcheck")
        estimator.scroll_into_view_if_needed()

        # Adjust slider to change values
        print("Adjusting slider...")
        slider = page.locator("input[type='range']")
        slider.fill("120") # 120 sqm
        page.wait_for_timeout(500)

        print("Taking screenshot...")
        page.screenshot(path="verification/estimator_visual.png", full_page=False)

        browser.close()

if __name__ == "__main__":
    run()
