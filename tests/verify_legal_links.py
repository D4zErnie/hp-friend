from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    # Navigate to the page
    page.goto("http://localhost:3000/dirking.html")

    # Dismiss cookie banner
    try:
        page.click("button:text('Einverstanden')")
    except:
        pass

    # Navigate to Legal Page (Impressum is default tab)
    # Using footer link to navigate to Legal
    page.click("text=Impressum")
    time.sleep(1) # Wait for animation/render

    print("Checking Impressum links...")

    # Check IHK link
    ihk_link = page.locator("a[href*='ihk.de/osnabrueck']")
    if ihk_link.count() > 0:
        print("✅ IHK Link found")
        assert ihk_link.get_attribute("target") == "_blank", "IHK link missing target='_blank'"
        assert "noopener" in ihk_link.get_attribute("rel"), "IHK link missing rel='noopener'"
    else:
        print("❌ IHK Link NOT found (Expected for initial fail)")
        # This is expected to fail initially

    # Navigate to Erstinformation tab
    page.click("button:has-text('Erstinformation')")
    time.sleep(1)

    print("Checking Erstinformation links...")

    # Check Vermittlerregister link
    vermittler_link = page.locator("a[href*='vermittlerregister.info']")
    if vermittler_link.count() > 0:
        print("✅ Vermittlerregister Link found")
        assert vermittler_link.get_attribute("target") == "_blank"
    else:
        print("❌ Vermittlerregister Link NOT found")

    # Check Versicherungsombudsmann link
    ombudsmann_link = page.locator("a[href*='versicherungsombudsmann.de']")
    if ombudsmann_link.count() > 0:
        print("✅ Versicherungsombudsmann Link found")
        assert ombudsmann_link.get_attribute("target") == "_blank"
    else:
        print("❌ Versicherungsombudsmann Link NOT found")

    # Check PKV Ombudsmann link
    pkv_link = page.locator("a[href*='pkv-ombudsmann.de']")
    if pkv_link.count() > 0:
        print("✅ PKV Ombudsmann Link found")
        assert pkv_link.get_attribute("target") == "_blank"
    else:
        print("❌ PKV Ombudsmann Link NOT found")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
