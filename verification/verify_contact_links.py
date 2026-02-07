
from playwright.sync_api import sync_playwright
import os

if not os.path.exists("verification"):
    os.makedirs("verification")

def verify_contact_links():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})
        page.goto("http://localhost:3000/dirking.html")

        # Navigate to Contact Page
        page.click('nav button:has-text("Kontakt")')

        # Wait for the contact page header
        page.wait_for_selector('h1:has-text("Lernen wir uns kennen")')

        # Scroll to the contact section
        contact_section = page.locator('h3:has-text("Direkter Kontakt")')
        contact_section.scroll_into_view_if_needed()

        # Check Phone Link
        phone_link = page.locator('a[href="tel:+49123456789"][aria-label="Rufen Sie uns an"]')

        # Check Email Link
        email_link = page.locator('a[href="mailto:beratung@dirking.de"][aria-label="Schreiben Sie uns eine E-Mail"]')

        # Check WhatsApp Link
        wa_link = page.locator('a[href="https://wa.me/49123456789"][aria-label="Chatten Sie mit uns auf WhatsApp"]')

        # Highlight elements for screenshot
        if phone_link.count() > 0:
            phone_link.evaluate("el => el.style.border = '5px solid red'")
        if email_link.count() > 0:
            email_link.evaluate("el => el.style.border = '5px solid red'")
        if wa_link.count() > 0:
            wa_link.evaluate("el => el.style.border = '5px solid red'")

        # Take screenshot
        screenshot_path = "verification/contact_page_links.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    verify_contact_links()
