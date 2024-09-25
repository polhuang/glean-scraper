from linkedin_scraper import Person,actions
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
