import getpass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def login(driver, email, password):
    """
    Naviagates to the LinkedIn Login page and logs the user in.
    Args:
        driver: The selenium WebDriver Instance
        email (str): The user's LinkedIn email
        password (str): The user's LinkedIn password

    Return:
        bool: True if login is successful, False otherwise.
    """

    print("Navigating to LinkedIn login page...")
    driver.get("[https://www.linkedin.com/login](https://www.linkedin.com/login)")

    try:
        wait = WebDriverWait(driver, 15)
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field.send_keys(email)

        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        print("Login submitted. Waiting for home page to load...")

        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, `/mynetwork/')]")))

        print("Login successful!")
        return True

    except TimeoutException:
        print("\n--- ERROR: Login Failed ---")
        print("Timeout occured. This could be due to: ")
        print(" - Incorrect email or password - ")
        print(" - A slow internet connection - ")
        print(" - A CAPTCHA verification check on the page (check the browser). - ")
        return False
    except Exception as e:
        print(f"\nAn Unexpected error occurred during login: {e}")
        return False

def get_credentials(predefined_email):
    """
    Prompts the user for their email and password
    Args:
        predefined_email (str): An email address from the config file.

    Returns:
        tuple: A tuple containing the email and password
    """
    email = predefined_email
    if not email:
        email = input("Enter your LinkedIn email: ")

    password = getpass.getpass("Enter your LinkedIn password: ")
    return email, password
