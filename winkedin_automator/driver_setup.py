import os
from playwright.sync_api import Playwright

def create_playwright_context(playwright: Playwright):
    """
    Launches a browser and creates a new context with the saved
    authentication state, effectively starting the session already logged in.
    """
    auth_file = "auth.json"
    if not os.path.exists(auth_file):
        print("\n--- ❌ ERROR: Authentication file not found! ---")
        print("Please run the one-time setup first: `python setup_auth.py`")
        return None

    print("Initializing browser and loading session...")
    browser = playwright.chromium.launch(headless=False)
    
    context = browser.new_context(storage_state=auth_file)
    print("✅ Browser context created with saved login session.")
    return context