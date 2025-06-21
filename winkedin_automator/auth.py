import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login(driver, email, password):
    """
    Navigates to the LinkedIn login page and logs the user in.
    """
    print("Navigating to LinkedIn login page...")
    # Using the direct login page URL.
    driver.get("[https://www.linkedin.com/login](https://www.linkedin.com/login)")

    try:
        wait = WebDriverWait(driver, 15)

        # FIX: Wait for the email field to be clickable, not just present.
        email_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        email_field.send_keys(email)

        # The password field should be available at the same time.
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        print("Login submitted. Waiting for home page to load...")

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/mynetwork/')]")))

        print("✅ Login successful!")
        return True

    except TimeoutException:
        print("\n--- ❌ ERROR: Login Failed ---")
        print("Timeout occurred. This could be due to:")
        print("  - Incorrect email or password.")
        print("  - A slow internet connection.")
        print("  - A CAPTCHA verification check on the page (check the browser).")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred during login: {e}")
        return False

def get_credentials(predefined_email):
    email = predefined_email
    if not email:
        email = input("Enter your LinkedIn email: ")
    password = getpass.getpass("Enter your LinkedIn password: ")
    return email, password
