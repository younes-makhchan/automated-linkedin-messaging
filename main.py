from automation import send_first_message, setup_driver_session, send_files
from create_pdf import create_updated_pdf
import time
from dotenv import load_dotenv
import os


#companies lists
companies = [
    {'url': 'https://www.linkedin.com/company/%E5%AE%A2%E6%88%B7/?viewAsMember=true', 'name': 'kehu'},
]

load_dotenv()
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

driver,wait=setup_driver_session(email,password)

for company in companies:
    driver.get(company['url'])
    send_first_message(wait,"""Hello Team

    I hope this message finds you well. i'm a Motivated Fast Learning project oriented Software Engineer :D. I’m reaching out to express my interest in exploring part-time, remote development opportunities with your company.

    Please find attached my resume and cover letter, where I highlight my experience at Oracle and CyberDefenders, as well as relevant projects and technical skills.

    For additional information, you can view my work at:

        Portfolio: makhchan.tech
        GitHub: github.com/younes-makhchan

    I look forward to any opportunity to discuss how my skills and experience can contribute to your team.

    Warm regards
    Younes Makhchan""")

    pdf_path =create_updated_pdf(company["name"],"./Younes Makhchan Cover Letter.docx")
    send_files(wait,["./younes makhchan resume.pdf",f"./companies/{company["name"]}/Younes Makhchan Cover Letter.pdf"])

time.sleep(5)
print("finished")

# Quit the driver
driver.quit()

