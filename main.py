from automation import setup_driver_session,send_message
from tools import update_company_value,validate_companies_file
import time
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()
# Loading companies lists should have url and name and init status 
companies=validate_companies_file()

#attempt to login to linkedin and initialize driver
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
cover_letter_docs_path = os.getenv('COVER_LETTER_DOCS_PATH')
resume_letter_pdf_path = os.getenv('RESUME_LETTER_PDF_PATH')
driver,wait=setup_driver_session(email,password)



for index,company in enumerate(companies):
    name=company['name']
    print(f"Sending message to {name}")

    if '/in/' in company['url']:
        update_company_value( company['name'], 'status', "personal")
        continue

    if company['status'] != 'not-applied':
        print(f"Already gone into  {name}, we passing")
        continue

    send_message(driver,wait,company,cover_letter_docs_path,resume_letter_pdf_path)
    if (index + 1) % 15 == 0:
        sleep_duration = random.randint(25, 30)
        print(f"Sleeping for {sleep_duration} seconds (after {index + 1} companies)...")
        time.sleep(sleep_duration)


time.sleep(5)
print("finished")

# Quit the driver
driver.quit()

