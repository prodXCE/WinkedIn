from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError

def search_and_select_person(page: Page, job_info: dict):
    """
    Searches for a relevant person at the company using Playwright.
    """
    role = input(f"\nWhat type of person do you want to find at {job_info['company']}? (e.g., 'Recruiter', 'Hiring Manager'): ")
    search_query = f'"{role}" "{job_info["company"]}"'
    
    print(f"🔍 Searching for people with query: {search_query}")

    try:
        search_bar = page.get_by_placeholder("Search")
        search_bar.fill(search_query)
        search_bar.press("Enter")

        page.get_by_role("button", name="People").click()
        print("Applied 'People' filter. Waiting for results...")
        
        results_list = page.locator("ul.reusable-search__entity-result-list")
        expect(results_list).to_be_visible(timeout=20000)

        people = results_list.locator("li").all()
        
        scraped_people = []
        print("\n--- People Found ---")
        for i, person_card in enumerate(people[:5]):
            try:
                name_element = person_card.locator("span[aria-hidden='true']").first
                name = name_element.inner_text()
                if not name or name == "LinkedIn Member": continue
                
                profile_link_element = person_card.locator("a.app-aware-link").first
                profile_link = profile_link_element.get_attribute("href")
                
                scraped_people.append({'name': name, 'profile_url': profile_link})
                print(f"{i+1}. {name}")
            except Exception:
                continue
                
        if not scraped_people:
            print("\nNo relevant people found.")
            return None
        
        while True:
            choice = input("\nSelect a person to connect with (or '0' to cancel): ")
            if choice.isdigit():
                choice_num = int(choice)
                if 0 < choice_num <= len(scraped_people):
                    return scraped_people[choice_num - 1]['profile_url']
                elif choice_num == 0:
                    return None
            print("Invalid selection.")

    except PlaywrightTimeoutError:
        print("\nCould not find people results. The page may have changed or the search returned no results.")
        return None
    except Exception as e:
        print(f"\nAn unexpected error occurred during person search: {e}")
        return None