from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from .ai_generator import generate_referral_message # Import AI function

def get_connection_message(job_info=None):
    if job_info:
        message = generate_referral_message(job_info['title'], job_info['company'])
        while True:
            print("\n" + "="*50)
            print("🤖 AI-Generated Message:")
            print(f'"{message}"')
            print("="*50)
            print("\n1. Send this message as is\n2. Edit this message\n3. Regenerate message")
            edit_choice = input("Enter your choice (1, 2, or 3): ")
            if edit_choice == '1':
                return message
            elif edit_choice == '2':
                edited_message = input("New message: ")
                return edited_message if edited_message.strip() else message
            elif edit_choice == '3':
                message = generate_referral_message(job_info['title'], job_info['company'])
            else:
                print("Invalid choice.")
    else:
        return input("\nEnter your custom message for the connection request: ")


def send_connection_request(page: Page, profile_url: str, message: str):
    print(f"\nNavigating to profile: {profile_url}")
    page.goto(profile_url)
    
    try:
        expect(page.get_by_role("heading", level=1)).to_be_visible(timeout=20000)
        print("Profile page loaded.")

        connect_button = page.get_by_role("button", name="Connect")
        
        if not connect_button.is_visible():
            print("Direct 'Connect' button not found. Checking 'More...' menu.")
            page.get_by_role("button", name="More").click()
            page.get_by_role("menuitem", name="Connect").click()
        else:
             connect_button.click()

        print("Connect flow initiated. Handling invitation modal...")
        
        page.get_by_role("button", name="Add a note").click()
        page.get_by_label("Add a note").fill(message)
        page.get_by_role("button", name="Send now").click()
        
        print("\n" + "="*50 + "\n✅ Connection request sent successfully!\n" + "="*50)
        
    except PlaywrightTimeoutError:
        print("\n--- ❌ ERROR: Failed to send connection request. ---")
    except Exception as e:
        print(f"\nAn unexpected error occurred during connection request: {e}")