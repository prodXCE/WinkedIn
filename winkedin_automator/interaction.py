import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def get_connection_message(job_info=None):
    """
    Handles the logic for choosing and customizing the connection message.
    """

    from .ai_generator import generate_referral_message

    if job_info:
        message = generate_referral_message(job_info['title'], job_info['company'])
        while True:
            print("\n" + "="*50)
            print("AI-Generated Message: ")
            print("="*50)
            print("\n1.Send this message as is")
            print("2. Edit this message")
            print("3. Regenerate message")
            edit_choice = input("Enter your choice (1, 2, or 3): ")

            if edit_choice == '1':
                return message
            elif edit_choice == '2':
                print("\nPlease type your new message below and press Enter when done.")
                edited_message = input("New message: ")
                return edited_message if edited_message.strip() else message
            elif edit_choice == '3':
                message = generate_referral_message(job_info['title'], job_info['company'])
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        else:
            return input("\nEnter your custom message for the connection request: ")

def send_connection_request(driver, profile_url, message):
    """
    Navigates to a profile and sends a connection request with a custom message.
    """
    print(f"\nNavigating to profile: {profile_url}")
    driver.get(profile_url)
    wait = WebDriverWait(driver, 15)

    try:
        # REVISED LOGIC: LinkedIn has many variations of the connect button.
        # This sequence attempts to find the most common ones.

        # Look for the 'pvs-profile-actions' container which holds the buttons.
        profile_actions_area = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pvs-profile-actions")))

        connect_button = None
        # Try to find a button with a "Connect" label directly. This is common.
        try:
            connect_button = profile_actions_area.find_element(By.XPATH, ".//button[contains(@aria-label, 'Connect with')]")
        except NoSuchElementException:
            print("Primary 'Connect' button not found. Checking 'More...' menu.")
            # If not found, it might be inside the "More" dropdown.
            more_button = profile_actions_area.find_element(By.XPATH, ".//button[contains(@aria-label, 'More actions')]")
            more_button.click()
            time.sleep(1) # Wait for dropdown animation

            # Find the 'Connect' option inside the opened menu.
            connect_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='dialog']//span[text()='Connect']")))
            connect_option.click()

        if connect_button:
            connect_button.click()

        # At this point, the connection modal should be open, regardless of which button was clicked.
        print("Connect flow initiated. Handling the invitation modal...")

        add_note_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Add a note']")))
        add_note_button.click()
        print("'Add a note' button clicked.")

        message_box = wait.until(EC.presence_of_element_located((By.ID, "custom-message")))
        message_box.send_keys(message)
        print("Message entered into the text box.")
        time.sleep(1)

        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send now']")))
        send_button.click()

        print("\n" + "="*50)
        print("✅ Connection request sent successfully!")
        print("="*50)

    except (TimeoutException, NoSuchElementException) as e:
        print("\n--- ❌ ERROR: Failed to send connection request. ---")
        print("Could not complete the connection process. This could mean:")
        print("  - You are already connected or have a pending request.")
        print("  - The person does not accept connections.")
        print("  - LinkedIn's website layout has changed, breaking the script.")
        print(f"Debug Info: {e}")
