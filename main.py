from automation import setup_driver_session,send_message
from tools import update_company_value
import time
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()

#attempt to login to linkedin and initialize driver
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
driver,wait=setup_driver_session(email,password)


#loading companies lists should have url and name
with open('./companies.json', 'r') as file:
    companies = json.load(file)


for index,company in enumerate(companies):
    name=company['name']
    print(f"Sending message to {name}")

    if '/in/' in company['url']:
        update_company_value( company['name'], 'status', "personal")
        continue

    send_message(driver,wait,name)
    if (index + 1) % 15 == 0:
        sleep_duration = random.randint(25, 30)
        print(f"Sleeping for {sleep_duration} seconds (after {index + 1} companies)...")
        time.sleep(sleep_duration)


time.sleep(5)
print("finished")

# Quit the driver
driver.quit()

