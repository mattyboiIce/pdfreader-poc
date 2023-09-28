import re
import os
import json

# Define the directory containing the .txt files
directory = '/Users/matthewmarshall/Documents/RyGuy Client Clean Proj'

# Define the regex patterns for each field
patterns = {
    'Name': re.compile(r'Name: (.+?)\s*Name:'),
    'Date of Birth': re.compile(r'Date of Birth: (\d{1,2}/\d{1,2}/\d{4})'),
    'SSN': re.compile(r'SSN: (\d{3}-\d{2}-\d{4})'),
    'DL Number': re.compile(r'DL Number: (\d+)'),
    # ... Add other fields similarly
}

# Initialize a dictionary to hold the extracted information for all files
all_extracted_data = {}

# Iterate through each .txt file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)

        # Read the file content
        with open(filepath, 'r', encoding='ISO-8859-1', errors='replace') as file:
            content = file.read()

        # Initialize a dictionary to hold the extracted information for the current file
        extracted_data = {}

        # Iterate through each pattern and search for it in the content
        for field, pattern in patterns.items():
            match = pattern.search(content)
            if match:
                extracted_data[field] = match.group(1)

        # Save the extracted data for the current file to the main dictionary
        all_extracted_data[filename] = extracted_data

# Save the extracted data to a .json file
output_file_path = os.path.join(directory, 'extracted_data.json')
with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(all_extracted_data, json_file, ensure_ascii=False, indent=4)

print(f"Extracted data saved to {output_file_path}")
