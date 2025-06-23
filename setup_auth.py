from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        print("\n--- WinkedIn First-Time Setup ---")
        print("A browser window will now open.")
        print("Please log in to your LinkedIn account manually.")
        print("After you have successfully logged in and are on the main feed page, this script will save your session.")

        page.goto("[https://www.linkedin.com/login](https://www.linkedin.com/login)")

        print("\nWaiting for you to log in...")
        try:
            # This robust check waits for a URL containing "/feed/".
            page.wait_for_url("**/feed/**", timeout=300000)
            print("✅ Login successful! You are on the feed page.")
        except Exception as e:
            print(f"❌ Timed out waiting for login. Please try running the script again. Error: {e}")
            browser.close()
            return

        print("Saving authentication state to 'auth.json'...")
        context.storage_state(path="auth.json")
        print("✅ Authentication state saved successfully!")
        
        print("\n--- Setup Complete ---")
        print("You can now close this browser window and run the main program using `python main.py`.")
        time.sleep(10)
        browser.close()

if __name__ == "__main__":
    run()