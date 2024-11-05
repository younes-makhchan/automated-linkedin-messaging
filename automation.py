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

def save_cookies(driver, filename):
    with open(filename, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filename):
    with open(filename, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
            
def setup_driver_session(email, password):
    # Set up Chrome options for headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Enable headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Bypass OS security model, required for running as root (Linux only)
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    
    # Set up the service and driver with options
    service = Service(executable_path="./chromedriver/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Navigate to LinkedIn (homepage)
    driver.get("https://www.linkedin.com/login")
    email_field = driver.find_element(By.NAME, "session_key")
    email_field.send_keys(email)
    password_field = driver.find_element(By.NAME, "session_password")
    password_field.send_keys(password)
    password_field.submit()
    time.sleep(10)
    # Create a WebDriverWait instance
    wait = WebDriverWait(driver, 10)
    return driver, wait



def send_first_message(wait,message):
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


def send_files(wait,files):
    #assuming we are at the page where we want to send the files and we already sent the first message

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


