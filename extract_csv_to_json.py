import csv
import json

# Function to read CSV and create the companies list
def process_csv(input_file, output_file):
    companies = []
    
    # Open and read the CSV file
    with open(input_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        
        for row in csvreader:
            # Extract company name and URL (assuming name is in the first column and URLs are in the 6th and 7th columns)
            company_name = row[1]
            url = row[7]
            company_name = company_name.replace("GmbH", "")
            print(f"Company Name: {company_name}, URL: {url}")
            # Check if the company has a name and at least one URL
            if company_name and url!= '-':  # Assuming at least one URL is required
                companies.append({
                    'name': company_name,
                    'urls': url  # Filter out empty URLs
                })
    
    # Store the companies in a JSON file
    with open(output_file, 'w', encoding='utf-8') as jsonfile:
        json.dump(companies, jsonfile, ensure_ascii=False, indent=4)
    
    print(f"Companies data has been written to {output_file}")

# File paths
input_csv = 'companies.csv'  # Your CSV file path
output_json = 'companies.json'  # Output JSON file path

# Run the function
process_csv(input_csv, output_json)
