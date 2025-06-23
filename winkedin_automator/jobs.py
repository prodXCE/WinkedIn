from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

def search_and_select_job(page: Page):
    """
    Automates the job search process using the most robust locators and
    a defensive scraping strategy.
    """
    keywords = input("\nEnter job keywords (e.g., 'Software Engineer'): ")
    location = input("Enter location (e.g., 'Remote'): ")

    print(f"\n🔍 Navigating to the jobs page...")
    page.goto("https://www.linkedin.com/jobs/search/")

    try:
        print("Locating and filling search form...")
        keywords_selector = "input[aria-label='Search by title, skill, or company']:not([disabled])"
        location_selector = "input[aria-label='City, state, or zip code']:not([disabled])"
        keywords_input = page.locator(keywords_selector)
        location_input = page.locator(location_selector)
        expect(keywords_input).to_be_visible(timeout=15000)
        expect(location_input).to_be_visible(timeout=15000)
        keywords_input.fill(keywords)
        location_input.fill(location)

        print("Clicking the specific search button...")
        search_button = page.locator("button.jobs-search-box__submit-button")
        search_button.click()
        
        print("Search submitted. Waiting for results to appear...")
        
        # Step 3: Wait directly for the first job listing to appear.
        first_job_listing_locator = page.locator("//li[.//a[contains(@href, '/jobs/view/')]]").first
        expect(first_job_listing_locator).to_be_visible(timeout=25000)
        print("✅ Job results are visible.")
        
        # Step 4: Scrape all the job listings.
        jobs = page.locator("//li[.//a[contains(@href, '/jobs/view/')]]").all()
        
        if not jobs:
            print("\nSearch successful, but no job listings were found.")
            return None

        print(f"\n--- Found {len(jobs)} listings. Scraping data... ---")
        
        scraped_jobs = []
        for i, job_card in enumerate(jobs):
            title = None
            company = "Company Not Listed" # Default value
            job_link = None
            
            try:
                title_link_element = job_card.locator("a[href*='/jobs/view/']").first
                title = title_link_element.inner_text()
                job_link = title_link_element.get_attribute("href")
            except Exception:
                print(f"  ⚠️ INFO: Item {i+1} is missing a title/link. Skipping.")
                continue

            try:
                company_link_element = job_card.locator("a[href*='/company/']").first
                company = company_link_element.inner_text()
            except Exception:
                pass
            
            if title and job_link:
                if not job_link.startswith("http"):
                    job_link = f"https://www.linkedin.com{job_link}"
                scraped_jobs.append({'title': title.strip(), 'company': company.strip(), 'link': job_link})

        if not scraped_jobs:
            print("\nCould not parse any valid job data from the results page. The layout may have changed.")
            return None
            
        print("\n--- Top Job Results ---")
        for i, job in enumerate(scraped_jobs):
             print(f"{i+1}. {job['title']} at {job['company']}")

        while True:
            choice = input("\nSelect a job number to proceed (or '0' to cancel): ")
            if choice.isdigit():
                choice_num = int(choice)
                if 0 < choice_num <= len(scraped_jobs):
                    return scraped_jobs[choice_num - 1]
                elif choice_num == 0:
                    return None
            print("Invalid selection.")

    except PlaywrightTimeoutError:
        print("\n❌ A timeout occurred. The script waited for job results, but none appeared.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during job search: {e}")
        return None
