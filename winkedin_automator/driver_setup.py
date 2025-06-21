from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    """
    Initializes and returns a Selenium chrome WebDriver instance.
    """

    print("Initialzing browser driver...")
    try:
        options = webdriver.ChromeOptions()

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        print('Driver initialized successfully')
        return driver
    except Exception as e:
        print("\n--- ERROR: Could not Initialize Chrome Driver ---")
        print("This can happedn if Google Chrome is not installed or if there is a network issue.")
        print(f"Error details: {e}")
        return None
