import os
import time
import undetected_chromedriver as uc # Import the new library

def create_driver_with_profile():
    """
    Initializes an UNDETECTED Chrome WebDriver that uses a dedicated user profile.
    This combination is our strongest approach to bypass bot detection.
    """
    print("Initializing UNDETECTED browser driver with dedicated user profile...")

    home_dir = os.path.expanduser("~")

    if os.name == 'nt':
        profile_path = "C:\\WinkedInChromeProfile"
    else:
        # Corrected the profile path from the user's log file
        profile_path = os.path.join(
            home_dir,
            "Development",
            "project4 Linekdin-ai-automator",
            "WinkedIn",
            "Browser-data"
        )


    print(f"Using profile path: {profile_path}")

    if not os.path.isdir(profile_path):
        print("\n--- ❌ ERROR: Chrome Profile Not Found! ---")
        print("Please follow the setup steps carefully:")
        # ... (error message remains the same)
        return None

    try:
        options = uc.ChromeOptions()
        # The argument format is slightly different but the principle is the same.
        options.add_argument(f'--user-data-dir={profile_path}')
        options.add_argument("--start-maximized")

        # Use uc.Chrome() instead of webdriver.Chrome()
        # It will automatically download the correct driver if needed.
        driver = uc.Chrome(options=options, use_subprocess=True)

        print("✅ Undetected driver initialized with existing profile successfully.")
        return driver
    except Exception as e:
        print("\n--- ❌ ERROR: Could not initialize Undetected Chrome Driver ---")
        print("Please ensure ALL Chrome windows are closed before running the script.")
        print(f"Error details: {e}")
        return None
