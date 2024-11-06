import json

def update_company_value( company_name, key, new_value):
    file_path="./companies.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for company in data:
        if company['name'] == company_name:
            company[key] = new_value
            break
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



def validate_companies_file(file_path="./companies.json"):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    companies_with_pipe = []
    unique_companies = []
    seen_urls = set()
    
    for company in data:
        company['name'] = company['name'].strip().rstrip('.')
        if '|' in company['name']:
            companies_with_pipe.append(company['name'])
        if 'status' not in company:
            company['status'] = 'not-applied'
        
        if company['url'] not in seen_urls:
            seen_urls.add(company['url'])
            unique_companies.append(company)
    
    if companies_with_pipe:
        raise ValueError(f"remove | from the names of the following companies: {', '.join(companies_with_pipe)}")
    
    with open(file_path, 'w') as file:
        json.dump(unique_companies, file, indent=4)
    
    return unique_companies



# update the a property value in all companies  in companies.json
def update_all_companies(key, new_value):
    file_path = "./companies.json"
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for company in data['companies']:
        company[key] = new_value
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Example usage:
# print(validate_no_duplicates('companies.json'))