# Updates selectors for job search inputs to be more robust.

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def search_and_select_job(driver):
    """
    Automates the job search process on LINKEDIN_EMAIL

    Returns:
        A dictionary with job details, or None if failed/cancelled.
    """
    keywords = input("\nEnter job keywords (e.g., 'Android Developer'): ")
    location = input("\nEnter location (e.g., `Banagaluru, India` or `New Delhi, India`): ")

    print(f"\n Searching for '{keywords}' jobs in '{location}'...")
    driver.get("https://www.linkedin.com/jobs/](https://www.linkedin.com/jobs/)")
    wait = WebDriverWait(driver, 10)

    try:
        search_keywords_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[arial-label='Search by title, skill, or company']")))
        search_keywords_input.clear()
        search_keywords_input.send_keys(keywords)

        search_location_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']")))
        search_location_input.clear()
        search_location_input.send_keys(location)
        search_location_input.send_keys(Keys.RETURN)

        print("Search submitted. Waiting for results...")

        job_list_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search__results-list")))
        time.sleep(2)

        jobs = job_list_element.find_elements(By.TAG_NAME, "li")

        scraped_jobs = []
        print("\n--- Top Job Results ---")
        for i, job in enumerate(jobs[:10]):
            try:
                title = job.find_element(By.CSS_SELECTOR, "h3.base-search-card__title").text
                company = job.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtite").text
                job_link = job.find_element(By.CSS_SELECTOR, "a.base-card__full-link").get_attribute("href")

                scraped_jobs.append({'title': title, 'company': company, 'link': job_link})
                print(f"{i+1}. {title} at {company}")
            except NoSuchElementException:
                continue

        if not scraped_jobs:
            print("\nNo jobs found matching your criteria. Please try a broader search.")
            return None

        while True:
            choice = input("\nSelect a job number to proceed (or '0' to cancel): ")
            if choice.isdigit():
                choice_num = int(choice)
                if 0 < choice_num <= len(scraped_jobs):
                    return scraped_jobs[choice_num - 1]
                elif choice_num == 0:
                    return None
            print("Invalid selection. Please enter a number from the list.")

    except TimeoutException:
            print("\nCould not find job listings. The page may have changed or your search returned no results.")
            return None
    except Exception as e:
            print(f"\nAn unexpected error occured during job search: {e}")
            return None
