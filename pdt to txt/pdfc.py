import re
from pypdf import PdfReader
import json
import os
def extract_data_from_pdf(pdf_file):
    SECONDARY_EMPLOYER_INDEX = 8
    customer_data_fields = ['Name', 'SSN', 'DL Number', 'Issue Date', 'State Issued', 'Exp Date', 'Occupation', 'Employer', 'Employer', 'Address']
    c1_data = {}
    c2_data = {}
    field_number = 0
    with open(pdf_file, 'rb') as pdf:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if field_number > len(customer_data_fields) - 1:
                    break
                check_field_len = len(customer_data_fields[field_number])
                if line[:check_field_len] == customer_data_fields[field_number]:
                    # print(customer_data_fields[field_number] + ":")
                    line = line.replace(customer_data_fields[field_number], "")
                    dual_customer_info = line.split(":")
                    if field_number == SECONDARY_EMPLOYER_INDEX:
                        c1_data['Secondary Employer'] = dual_customer_info[1].strip() if len(dual_customer_info) > 1 else None  # Use a conditional expression
                        c2_data['Secondary Employer'] = dual_customer_info[2].strip() if len(dual_customer_info) > 2 else None  # Use a conditional expression
                        continue
                    c1_data[customer_data_fields[field_number]] = dual_customer_info[1].strip() if len(dual_customer_info) > 1  else None  # Use a conditional expression
                    c2_data[customer_data_fields[field_number]] = dual_customer_info[2].strip() if len(dual_customer_info) > 2 else None  # Use a conditional expression
                    field_number += 1
    return [c1_data, c2_data]
    # return customer_data_list
# Folder containing PDF files
import os
pdf_folder = os.getcwd()
# List to store customer data dictionaries
all_customer_data = []
# Iterate through PDF files in the folder
for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        pdf_file_path = os.path.join(pdf_folder, filename)
        customer_data_list = extract_data_from_pdf(pdf_file_path)
        all_customer_data.extend(customer_data_list)
# Write the customer data list to a JSON file
json_file = 'clients.json'
with open(json_file, 'w') as json_output:
    json.dump(all_customer_data, json_output, indent=4)
print(f"Data extracted and saved to {json_file}")