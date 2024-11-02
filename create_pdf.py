
from docx import Document
from docx2pdf import convert
import os

def create_updated_pdf(company_name, original_docx_path):
    # Create a new PDF canvas
    doc = Document(original_docx_path)

    # Loop through each paragraph in the document
    for paragraph in doc.paragraphs:
        if '_company_' in paragraph.text:
            # Create a new paragraph for updated text
            for run in paragraph.runs:
                if '_company_' in run.text:
                    # Replace _company_ with the actual company name
                    run.text = run.text.replace('_company_', company_name)

    # Create a directory for the company
    directory = f"./companies/{company_name}"
    os.makedirs(directory, exist_ok=True)

    # Save the updated document with the company name in the new directory
    output_docx_path = os.path.join(directory, f"Younes Makhchan Cover Letter.docx")
    doc.save(output_docx_path)
    print(f"Updated DOCX saved as: {output_docx_path}")

    # Convert DOCX to PDF and save it in the same directory
    output_pdf_path = os.path.join(directory, f"./Younes Makhchan Cover Letter.pdf")
    convert(output_docx_path, output_pdf_path)
    print(f"Converted PDF saved as: {output_pdf_path}")
    return output_pdf_path

