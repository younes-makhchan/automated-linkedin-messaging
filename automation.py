from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import pickle
from create_pdf import create_updated_pdf
from tools import update_company_value

COOKIE_FILE = "linkedin_cookies.pkl"

def save_cookies(driver, filename=COOKIE_FILE):
    with open(filename, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filename=COOKIE_FILE):
    if os.path.exists(filename):
        with open(filename, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

def setup_driver_session(email, password):
    # Set up the service and driver with options
    service = Service(executable_path="./chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    # Load saved cookies, if any
    
    # Navigate to LinkedIn (homepage)
    driver.get("https://www.linkedin.com/login")
    load_cookies(driver)
    driver.refresh()
    # Check if we're already logged in
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "global-nav")))
        print("Logged in successfully using saved cookies.")
        return driver, wait
    except:
        pass
    
    # If not logged in, login with email and password
    email_field = driver.find_element(By.NAME, "session_key")
    email_field.send_keys(email)
    password_field = driver.find_element(By.NAME, "session_password")
    password_field.send_keys(password)
    password_field.submit()
    
    # Wait for the feed page to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "global-nav")))
    
    # Save the cookies for future use
    save_cookies(driver)
    
    print("Logged in successfully.")
    return driver, wait

def send_first_message(wait,name):
    message = ""
    with open("./message_body.txt", "r",encoding="utf-8") as file:
        message = file.read().replace("_name_", name)
    try:
        button_with_message_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Message']]")))
    except TimeoutException  as e :
        return False
    print(button_with_message_span.text)
    button_with_message_span.click()

    select_topic = wait.until(EC.element_to_be_clickable((By.ID, "org-message-page-modal-conversation-topic")))
    select = Select(select_topic)
    try:
        select.select_by_visible_text("Careers")
    except:
        try:
            select.select_by_visible_text("Other")
        except:
            print("could not select topic")
            return False

    textarea = wait.until(EC.presence_of_element_located((By.ID, "org-message-page-modal-message")))
    textarea.clear()
    
    textarea.send_keys(message)
    send_message_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//button[.//span[text()="Send message"]]')))
    send_message_btn.click()
    time.sleep(0.5)
    return True


def send_files(wait,company,resume_letter_pdf_path,cover_letter_docs_path):
    
    
    if not os.path.exists(resume_letter_pdf_path) or not os.path.exists(cover_letter_docs_path):
        raise FileNotFoundError(f"The file '{resume_letter_pdf_path}' or '{cover_letter_docs_path}'  does not exist.")
 
    #updating the docs with company name and converting them to pdf 
    pdf_path =create_updated_pdf(company["name"],cover_letter_docs_path)
    files = [resume_letter_pdf_path,pdf_path]

    
    # Wait for the button with the message span to be present and click it
    button_with_message_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Message']]")))
    print(button_with_message_span.text)
    button_with_message_span.click()
    for file in files:
        print("Uploading file")
        file_path = os.path.abspath(file)

        # Wait for the file input to be present
        file_input1 = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Attach a file')]/preceding-sibling::input[@type='file']")))
        print(file_input1)

        # Send the file path to the input
        file_input1.send_keys(file_path)
        time.sleep(1)

    # Wait for the send message button to be present and click it
    send_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and text()='Send']")))
    send_message.click()

    #close the conversation window
    time.sleep(0.5)
    class_name = "msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"
    close_btn = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f".{class_name.replace(' ', '.')}")))
    
    close_btn.click()
    time.sleep(1)



def send_message(driver,wait,company,cover_letter_docs_path,resume_letter_pdf_path):
    driver.get(company['url'])   
    
    #sending the first career message 
    is_sent= send_first_message(wait,company['name'])
    if not is_sent:
        print("timeoutexception: page doesn't allow sending messages")
        update_company_value( company['name'], 'status', "failed")
        return False
    

    #sending the pdfs
    send_files(wait,company,resume_letter_pdf_path,cover_letter_docs_path)
    
    update_company_value( company['name'], 'status', "applied")
    return True
    
