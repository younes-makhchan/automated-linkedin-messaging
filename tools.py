import json

def update_company_value(file_path, company_name, key, new_value):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for company in data:
        if company['name'] == company_name:
            company[key] = new_value
            break
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def validate_companies_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    seen_ids = set()
    for company in data['companies']:
        if company['id'] in seen_ids:
            return False
        seen_ids.add(company['id'])
    
    return True

# Example usage:
# print(validate_no_duplicates('companies.json'))