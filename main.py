from playwright.sync_api import sync_playwright
from winkedin_automator import (
    driver_setup,
    jobs,
    interaction,
    people
)

def main_menu():
    print("\n" + "="*30 + "\n      WinkedIn Main Menu\n" + "="*30)
    print("1. Search for a job and ask for a referral")
    print("2. Send a connection request to a specific profile URL")
    print("3. Exit")
    print("="*30)
    while True:
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice.")

def job_search_workflow(page):
    selected_job = jobs.search_and_select_job(page)
    if not selected_job:
        return
    
    person_profile_url = people.search_and_select_person(page, selected_job)
    if not person_profile_url:
        return
        
    message = interaction.get_connection_message(job_info=selected_job)
    interaction.send_connection_request(page, person_profile_url, message)

def direct_connection_workflow(page):
    profile_url = input("\nEnter the full LinkedIn profile URL: ")
    if profile_url.startswith("https://www.linkedin.com/in/"):
        message = interaction.get_connection_message()
        interaction.send_connection_request(page, profile_url, message)
    else:
        print("❌ Invalid URL.")

def main():
    with sync_playwright() as playwright:
        context = driver_setup.create_playwright_context(playwright)
        if not context:
            return

        # FIX: Instead of trying to access an existing page (which doesn't exist),
        # we create a new one. This is the correct approach.
        page = context.new_page()
        
        try:
            while True:
                print("\nNavigating to LinkedIn feed to ensure a clean state...")
                page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded")
                
                choice = main_menu()
                if choice == '1':
                    job_search_workflow(page)
                elif choice == '2':
                    direct_connection_workflow(page)
                elif choice == '3':
                    print("\nThank you for using WinkedIn!")
                    break
                else:
                    print("Invalid choice.")
                
                input("\nPress Enter to return to the main menu...")
        except Exception as e:
            print(f"\nAn unexpected and critical error occurred: {e}")
        finally:
            print("\nClosing the browser...")
            context.close()

if __name__ == "__main__":
    main()
