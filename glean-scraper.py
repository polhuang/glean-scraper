from linkedin_scraper import Person, actions
from selenium import webdriver
import pandas as pd
import credentials

driver = webdriver.Chrome()
email = credentials.EMAIL
password = credentials.PASSWORD
actions.login(driver, email, password)
input_csv = "linkedin-urls.csv"
output_csv = "scraped-linkedin_profiles.csv"

# person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver = driver, scrape=False)
# person.scrape()

# data = {
#     'Name': person.name,
#     'Job Title': person.job_title,
#     'Company': person.company,
#     'About': person.about,
#     'Experience': [str(experience) for experience in person.experiences],
#     'Education': [str(education) for education in person.educations],
#     'Interests': [str(interest) for interests in person.interests]
#     }

def format_experience(experiences):
    formatted_experiences = []
    for exp in experiences:
        exp_str = (
            f"Position: {exp.position_title}\n"
            f"Company: {exp.institution_name}\n"
            f"From: {exp.from_date} - To: {exp.to_date}\n"
            f"Duration: {exp.duration}\n"
            f"Location: {exp.location}\n"
            f"Description: {exp.description}\n"
            f"LinkedIn URL: {exp.linkedin_url}\n"
        )
        formatted_experiences.append(exp_str)
    
    return "\n\n".join(formatted_experiences)

def format_education(educations):
    formatted_educations = []
    for edu in educations:
        edu_str = (
            f"Institution: {edu.institution_name}\n"
            f"Degree: {edu.degree}\n"
            f"From: {edu.from_date} - To: {edu.to_date}\n"
            f"Description: {edu.description}\n"
            f"LinkedIn URL: {edu.linkedin_url}\n"
        )
        formatted_educations.append(edu_str)
    
    return "\n\n".join(formatted_educations)

def scrape_linkedin_profile(url):
    try:
        person = Person(url, driver=driver, scrape=True)

        data = {
            'Name': person.name,
            'Job Title': person.job_title,
            'Company': person.company,
            'About': person.about,
            'Experience': format_experience(person.experiences),
            'Education': format_education(person.educations), 
        }
        
        return data

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
    
def scrape_profiles_from_csv(input_csv, output_csv):
    # Read the input CSV into a DataFrame
    df = pd.read_csv(input_csv)
    
    # Make sure the CSV has a 'LinkedIn URL' column
    if 'LinkedIn URL' not in df.columns:
        print("Error: Input CSV must contain a 'LinkedIn URL' column.")
        return
    
    # Create new columns for the scraped data
    df['Name'] = None
    df['Job Title'] = None
    df['Company'] = None
    df['About'] = None
    df['Experience'] = None
    df['Education'] = None
    
    # Scrape each LinkedIn profile and add the data to the DataFrame
    for index, row in df.iterrows():
        url = row['LinkedIn URL']
        print(f"Scraping LinkedIn profile: {url}")
        profile_data = scrape_linkedin_profile(url)
        df.at[index, 'Name'] = profile_data['Name']
        df.at[index, 'Job Title'] = profile_data['Job Title']
        df.at[index, 'Company'] = profile_data['Company']
        df.at[index, 'About'] = profile_data['About']
        df.at[index, 'Experience'] = profile_data['Experience']
        df.at[index, 'Education'] = profile_data['Education']
    
    # Save the updated DataFrame to the output CSV
    df.to_csv(output_csv, index=False)
    print(f"Scraping complete. Data saved to {output_csv}.")

scrape_profiles_from_csv(input_csv, output_csv)
driver.quit()
