from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        console_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        try:
            page.goto("http://localhost:3000/dirking.html")
            page.wait_for_timeout(2000) # Wait for React to mount
        except Exception as e:
            console_errors.append(str(e))

        if console_errors:
            print("Errors found:")
            for err in console_errors:
                print(f"- {err}")
        else:
            print("No errors found.")

        browser.close()

if __name__ == "__main__":
    run()
