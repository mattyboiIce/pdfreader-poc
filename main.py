import re
import PyPDF2
import json
import os

 

def extract_data_from_pdf(pdf_file):

    customer_data_list = []

    

    with open(pdf_file, 'rb') as pdf:

        pdf_reader = PyPDF2.PdfReader(pdf)

        

        for page in pdf_reader.pages:

            text = page.extract_text()

            lines = text.split('\n')

            

            # Initializing customer data for each page

            customer_data_1 = {}

            customer_data_2 = {}

            current_customer_data = customer_data_1  # Start with the first customer

            

            for line in lines:

                # Matching Names

                name_matches = re.findall(r"Name:\s*(.+?)(?:\s*Name:|$)", line)

                if name_matches:

                    customer_data_1["Name"] = name_matches[0].strip()

                    if len(name_matches) > 1:

                        customer_data_2["Name"] = name_matches[1].strip()

                        current_customer_data = customer_data_2

                

                # Matching Annual Income, Liquid Assets, Net Worth

                match_income = re.search(r"Annual Income:\s*([\d,]+)", line)

                match_assets = re.search(r"Liquid Assets:\s*([\d,-]+)", line)

                match_net_worth = re.search(r"Net Worth:\s*([\d,]+)", line)

                

                if match_income:

                    current_customer_data["Annual Income"] = match_income.group(1).replace(',', '').strip()

                if match_assets:

                    current_customer_data["Liquid Assets"] = match_assets.group(1).replace(',', '').strip()

                if match_net_worth:

                    current_customer_data["Net Worth"] = match_net_worth.group(1).replace(',', '').strip()

            

            # Append customer data for the page to the list

            if customer_data_1:

                customer_data_list.append(customer_data_1)

            if customer_data_2:

                customer_data_list.append(customer_data_2)

                

    return customer_data_list

 

 

# Folder containing PDF files

pdf_folder = '/Users/matthewmarshall/Documents/RyGuy Client Clean Proj'

 

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