from config import LINKEDIN_EMAIL
from winkedin_automator import (
    driver_setup,
    auth,
    jobs,
    people,
    interaction
)

def main_menu():
    """Displays the main menu and gets the user's choice."""
    print("\n" + "="*30)
    print("      WinkedIn Main Menu")
    print("="*30)
    print("1. Search for a job and ask for a referral")
    print("2. Send a connection request to a specific profile URL")
    print("3. Exit")
    print("="*30)

    while True:
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def job_search_workflow(driver):
    """Handles the entire workflow for finding a job and asking for a referral."""
    print("\n--- Starting Job Search Workflow ---")
    selected_job = jobs.search_and_select_job(driver)
    if not selected_job:
        print("\nJob search cancelled or failed. Returning to main menu.")
        return

    person_profile_url = people.search_and_select_person(driver, selected_job)
    if not person_profile_url:
        print("\nPerson search cancelled or failed. Returning to main menu.")
        return

    message = interaction.get_connection_message(job_info=selected_job)
    if not message:
        print("\nMessage creation cancelled. Returning to main menu.")
        return

    interaction.send_connection_request(driver, person_profile_url, message)

def direct_connection_workflow(driver):
    """Handles the workflow for connecting to a specific profile URL."""
    print("\n--- Starting Direct Connection Workflow ---")
    profile_url = input("\nEnter the full LinkedIn profile URL: ")
    if not profile_url.startswith("https://www.linkedin.com/in/"):
        print("❌ Invalid URL. It should start with 'https://www.linkedin.com/in/'.")
        return

    message = interaction.get_connection_message() # No job_info for a general message
    interaction.send_connection_request(driver, profile_url, message)


def main():
    """The main function that runs the application."""
    print("\n--- Welcome to WinkedIn: Your AI-Powered Career Assistant ---")

    driver = None
    try:
        email, password = auth.get_credentials(LINKEDIN_EMAIL)

        driver = driver_setup.create_driver()
        if not driver:
            return

        if not auth.login(driver, email, password):
            return

        while True:
            choice = main_menu()
            if choice == '1':
                job_search_workflow(driver)
            elif choice == '2':
                direct_connection_workflow(driver)
            elif choice == '3':
                print("\nThank you for using WinkedIn!")
                break

            input("\nPress Enter to return to the main menu...")

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Shutting down.")
    except Exception as e:
        print(f"\nAn unexpected and critical error occurred: {e}")
    finally:
        if driver:
            print("\nClosing the browser...")
            driver.quit()
            print("Browser closed. Goodbye!")

if __name__ == "__main__":
    main()
