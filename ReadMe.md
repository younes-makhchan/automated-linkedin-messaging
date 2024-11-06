# LinkedIn Message Sender

This repository contains a script to send LinkedIn messages to companies with customized cover letters and messages. It uses Selenium to simulate interaction on LinkedIn.

## How to Use

### 1. Create a `.env` File

Create a `.env` file in the root directory and add the following values:

```plaintext
EMAIL=<your-linkedin-email>
PASSWORD=<your-linkedin-password>
COVER_LETTER_DOCS_PATH=<path to your cover letter>
RESUME_LETTER_PDF_PATH=<path to your CV or resume>
```

### 2. Customize the Message

Go to the `message_body` section in the script and customize the message that will be sent to the company. The placeholder `_name_` will automatically be replaced with the company's name.

### 3. Prepare the Cover Letter

Your cover letter should be in a Word file (DOCX format). The script will edit it and replace the placeholder `_company_` with the company name before sending it.

### 4. Create `companies.json`

Create a `companies.json` file in the root directory with the following format:

```json
[
    {
        "name": "COMPANY_NAME",
        "url": "COMPANY_LINKEDIN_LINK"
    }
    // more companies
]
```
### 5. Install the Requirements

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```
### 5. run the script

Run the automation

```python
python main.py
```