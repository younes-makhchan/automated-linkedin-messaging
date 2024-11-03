from automation import send_first_message, setup_driver_session, send_files
from create_pdf import create_updated_pdf
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


for company in companies:
    name=company['name']
    print(f"Sending message to {name}")
    driver.get(company['url'])
    send_first_message(wait,f"""Hello {name} Team

    I hope this message finds you well. i'm a Motivated  project oriented Software Engineer :D. I’m reaching out to express my interest in exploring part-time, remote development opportunities with {name}.

    Please find attached my resume and cover letter, where I highlight my experience at Oracle and CyberDefenders, as well as relevant projects and technical skills.

    For additional information, you can view my work at:

        Portfolio: makhchan.tech
        GitHub: github.com/younes-makhchan

    I look forward to any opportunity to discuss how my skills and experience can contribute to {name}.

    Warm regards
    Younes Makhchan""")

    pdf_path =create_updated_pdf(company["name"],"./Younes Makhchan Cover Letter.docx")
    send_files(wait,["./younes makhchan resume.pdf",f"./companies/{company["name"]}/Younes Makhchan Cover Letter.pdf"])
    sleep_duration = random.randint(30, 120)
    print(f"Sleeping for {sleep_duration} seconds...")
    #time.sleep(sleep_duration)


time.sleep(5)
print("finished")

# Quit the driver
driver.quit()

