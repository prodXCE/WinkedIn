import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def search_and_select_person(driver, job_info):
    """
    Searches for a relevant person at the company from the job info.
    """
    role = input(f"\nWhat type of person do you want to find at {job_info['company']}? (e.g., 'Recruiter', 'Hiring Manager'): ")
    search_query = f'"{role}" "{job_info["company"]}"'

    print(f" Searching for people with query: {search_query}")
    wait = WebDriverWait(driver, 15)

    try:
        search_bar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='People']")))
        search_bar.clear()
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)

        people_filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='People']")))
        people_filter_button.click()

        print("Applied 'People' filter. Waiting for results...")

        wait.until(EC.presence_of_element_located((By.ID, "main")))
        time.sleep(2)

        people_list_element = driver.find_element(By.CLASS_NAME, "reusable-search__entity-result-list")
        people = people_list_element.find_elements(By.TAG_NAME, "li")

        scraped_people = []
        print("\n--- People Found ---")
        for i, person_card in enumerate(people[:5]):
            try:
                name_element = person_card.find_element(By.CSS_SELECTOR, "span[aria-hidden='true']")
                name = name_element.text
                if not name or name == "LinkedIn Member": continue

                profile_link_element = person_card.find_element(By.CSS_SELECTOR, "a.app-aware-link")
                profile_link = profile_link_element.get_attribute("href")

                scraped_people.append({'name': name, 'profile_url': profile_link})
                print(f"{i+1}. {name}")
            except NoSuchElementException:
                continue

        if not scraped_people:
            print("\nNo relevant people found. You might want to try a different role (e.g., 'Talent Acquisition').")
            return None

        while True:
            choice = input("\nSelect a person to connect with (or '0' to cancel): ")
            if choice.isdigit():
                choice_num = int(choice)
                if 0 < choice_num <= len(scraped_people):
                    return scraped_people[choice_num - 1]['profile_url']
                elif choice_num == 0:
                    return None
            print("Invalid selection. Please enter a number from the list")

    except TimeoutException:
        print("\nCould not find people results. The page may have changed or the search returned no results.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occured during person search: {e}")
        return None
