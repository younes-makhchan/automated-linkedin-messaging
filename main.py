from automation import send_first_message, setup_driver_session, send_files
from create_pdf import create_updated_pdf
from tools import update_company_value
import time
from dotenv import load_dotenv
import os
import json
import random

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
driver,wait=setup_driver_session(email,password)


#companies lists
with open('./companies.json', 'r') as file:
    companies = json.load(file)


for index,company in enumerate(companies):
    name=company['name']
    print(f"Sending message to {name}")
    if '/in/' in company['url']:
        print("It's personal, passing-------")
        continue
    driver.get(company['url'])
    

    is_sent= send_first_message(wait,f"""Hello {name} Team

    I hope this message finds you well. i'm a Motivated  project oriented Software Engineer :D. I’m reaching out to express my interest in exploring part-time, remote development opportunities with {name}.

    Please find attached my resume and cover letter, where I highlight my experience at Oracle and CyberDefenders, as well as relevant projects and technical skills.

    For additional information, you can view my work at:

        Portfolio: makhchan.tech
        GitHub: github.com/younes-makhchan

    I look forward to any opportunity to discuss how my skills and experience can contribute to {name}.

    Warm regards
    Younes Makhchan""")
    if not is_sent:
        print("timeoutexception: page doesn't allow sending messages")
        continue
    
    pdf_path =create_updated_pdf(company["name"],"./Younes Makhchan Cover Letter.docx")
    send_files(wait,["./younes makhchan resume.pdf",f"./companies/{company["name"]}/Younes Makhchan Cover Letter.pdf"])
    update_company_value('./companies.json', company['name'], 'status', "applied")
    if (index + 1) % 15 == 0:
        sleep_duration = random.randint(25, 30)
        print(f"Sleeping for {sleep_duration} seconds (after {index + 1} companies)...")
        time.sleep(sleep_duration)


time.sleep(5)
print("finished")

# Quit the driver
driver.quit()

