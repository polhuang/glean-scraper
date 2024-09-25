from linkedin_scraper import Person, actions
from selenium import webdriver
import credentials

driver = webdriver.Chrome()
email = credentials.EMAIL
password = credentials.PASSWORD
actions.login(driver, email, password)

    
person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver = driver, scrape=False)
person.scrape()

data = {
    'Name': person.name,
    'Job Title': person.job_title,
    'Company': person.company,
    'About': person.about,
    'Experience': [str(experience) for experience in person.experiences],
    'Education': [str(education) for education in person.educations],
    'Interests': [str(interest) for interests in person.interests]
    }

def scrape_linkedin_profile(url):
    try:
        person = Person(url, driver=driver, scrape=True)

        data = {
            'Name': person.name,
            'Job Title': person.job_title,
            'Company': person.company,
            'About': person.about,
            'Experience': [str(exp) for exp in person.experiences],
            'Education': [str(edu) for edu in person.educations],
            'Skills': [str(skill) for skill in person.skills],
        }

        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    
def scrape_profiles_from_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    if 'LinkedIn URL' not in df.columns:
        print("No 'LinkedIn URL' column.")
        return
    
    scraped_data = []
    
    for index, row in df.iterrows():
        url = row['LinkedIn URL']
        print(f"Scraping LinkedIn profile: {url}")
        profile_data = scrape_linkedin_profile(url)
        if profile_data:
            scraped_data.append(profile_data)
            
    scraped_df = pd.DataFrame(scraped_data)
    
    scraped_df.to_csv(output_csv, index=False)
    print(f"Scraping job is complete. Data hasbeen saved to {output_csv}.")
