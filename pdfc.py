import csv
import datetime
import os
from pypdf import PdfReader
import re


IMPORTANT_LINE_NUMBERS = {
    'phys_and_mail_addy_1': 17,
    'phys_and_mail_addy_2': 18,
    'home_and_cell_1': 20,
    'office_and_cell_2': 21,
    'other_and_fax': 22,    
    'primary_email': 24,
    'secondary_email': 25,
    'finances': 31,
    'cpa_and_attorney': 33,
    'other_advisors': 34,
    'tcp_name': 36,
    'tcp_phone': 37,
    'tcp_relationship_and_addy1': 38,
    'tcp_addy2': 39,

}

def get_rexeg_pattern_from_keywords(line, keywords):
    pattern = '|'.join(keywords)
    return re.split(pattern, line) 

def get_phone_number_from_line( line, keywords ):
    pattern = '|'.join(keywords)
    numbers = re.split(pattern, line) 
    converted_numbers = [numbers[1].strip()[:12], numbers[2].strip()[:12]]
    return converted_numbers 

def extract_data_from_pdf(pdf_file):
    SECONDARY_EMPLOYER_INDEX = 8
    customer_data_fields = ['Name', 'SSN', 'DL Number', 'Issue Date', 'State Issued', 'Exp Date', 'Occupation', 'Employer', 'Employer', 'Address']
    c1_data = {}
    c2_data = {}
    indv_field_number = line_number = 0

    with open(pdf_file, 'rb') as pdf:
        pdf_reader = PdfReader(pdf)
        physical_address = mailing_address = tcp_address = ''

        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                line_number += 1
                # print(line)
                if indv_field_number <= len(customer_data_fields) - 1:
                    check_field_len = len(customer_data_fields[indv_field_number])
                    if line[:check_field_len] == customer_data_fields[indv_field_number]:
                        line = line.replace(customer_data_fields[indv_field_number], "")
                        dual_customer_info = line.split(":")
                        if indv_field_number == SECONDARY_EMPLOYER_INDEX:
                            c1_data['Secondary Employer'] = dual_customer_info[1].strip() if len(dual_customer_info) > 1 and len(dual_customer_info[1].strip()) > 1 else 'N/A'
                            c2_data['Secondary Employer'] = dual_customer_info[2].strip() if len(dual_customer_info) > 2 and len(dual_customer_info[2].strip()) > 1 else 'N/A'
                            indv_field_number += 1
                            continue
                        c1_data[customer_data_fields[indv_field_number]] = dual_customer_info[1].strip() if len(dual_customer_info) > 1 and len(dual_customer_info[1]) > 1 else 'N/A'
                        c2_data[customer_data_fields[indv_field_number]] = dual_customer_info[2].strip() if len(dual_customer_info) > 2 and len(dual_customer_info[2]) > 1 else 'N/A'
                        indv_field_number += 1
                #here's where things get janky... lol fr daddy ;)
                # get the physical and mailing addresses
                elif line_number == IMPORTANT_LINE_NUMBERS['phys_and_mail_addy_1']:
                    keywords = ['Physical', 'Mailing'] 
                    pattern = '|'.join(keywords)
                    addresses = re.split(pattern, line)
                    if len(addresses)>2:
                        physical_address += addresses[1].strip()
                        mailing_address += addresses[2] if len(addresses[2]) > 0 else  addresses[1].strip()
                    elif len(addresses) > 1:
                        physical_address += addresses[1].strip()
                        mailing_address += addresses[1].strip()
                ##        
                elif line_number == IMPORTANT_LINE_NUMBERS['phys_and_mail_addy_2']:
                    addresses = line.split('Address:')
                    physical_address += ' ' + addresses[1].strip() 
                    mailing_address += ' ' + addresses[2] if len(addresses[2]) > 0 else ' ' + addresses[1].strip()
                    c1_data['Physical Address'] = c2_data['Physical Address'] =  physical_address if len(physical_address) > 2 else 'N/A'
                    c1_data['Mailing Address'] = c2_data['Mailing Address'] = mailing_address if len(mailing_address) > 2 else 'N/A'
                # end get physical and mailing addresses
                #get phone numbers
                elif line_number == IMPORTANT_LINE_NUMBERS['home_and_cell_1']:
                    numbers = get_phone_number_from_line(line, ['Home:', 'Cell:'] )
                    home_phone = numbers[0]
                    cell_1 = numbers[1]
                    c1_data['Home Phone'] = c2_data['Home Phone'] = home_phone if len(home_phone) > 2 else 'N/A'
                    c1_data['Cell 1'] = c2_data['Cell 1'] = cell_1 if len(cell_1) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['office_and_cell_2']:
                    numbers = get_phone_number_from_line(line, ['Office:', 'Cell:'] )
                    office_phone = numbers[0] 
                    cell_2 = numbers[1]
                    c1_data['Office Phone'] = c2_data['Office Phone'] = office_phone 
                    c1_data['Cell 2'] = c2_data['Cell 2'] = cell_2
                elif line_number == IMPORTANT_LINE_NUMBERS['other_and_fax']:
                    numbers = get_phone_number_from_line(line, ['Other:', 'Fax:'] )
                    other = numbers[0]
                    fax = numbers[1]
                    c1_data['Other'] = c2_data['Other'] = other if len(other) > 2 else 'N/A'
                    c1_data['Fax'] = c2_data['Fax'] = fax  if len(fax) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['primary_email']:
                    primary_email = line.split('E-mail:')[1].strip()
                    c1_data['Primary Email'] = c2_data['Primary Email'] = primary_email if len(primary_email) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['secondary_email']:
                    secondary_email = line.split('E-mail:')[1].strip() if len(line.split('E-mail:')) > 1 else 'N/A'
                    c1_data['Secondary Email'] = c2_data['Secondary Email'] = secondary_email if len(secondary_email) > 2 else 'N/A'
                #end get phone numbers
                elif line_number == IMPORTANT_LINE_NUMBERS['finances']:
                    numbers = get_rexeg_pattern_from_keywords(line, ['Annual Income:', 'Liquid Assets:', 'Net Worth'])
                    c1_data['Annual Income'] = c2_data['Annual Income'] = numbers[1].strip() if len(numbers[1].strip()) > 1 else 'N/A'
                    c1_data['Liquid Assets'] = c2_data['Liquid Assets'] = numbers[2].strip() if len(numbers[2].strip()) > 1 else 'N/A'
                    c1_data['Net Worth'] = c2_data['Net Worth'] = numbers[3].strip() if len(numbers[3].strip()) > 1 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['cpa_and_attorney']:
                    converted_line = line.replace("LOA", "")
                    names = get_rexeg_pattern_from_keywords(converted_line, ['CPA:', 'Attorney:'])
                    c1_data['CPA'] = c2_data['CPA'] = names[1].strip() if len(names[1].strip()) > 2 else 'N/A'
                    c1_data['Attorney'] = c2_data['Attorney'] = names[2].strip() if len(names[2].strip()) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['other_advisors']:
                    converted_line = line.replace("LOA", "")
                    names = get_rexeg_pattern_from_keywords(converted_line, ['Other:'])
                    c1_data['Other Advisors'] = c2_data['Other Advisors'] = names[1].strip() if len(names[1].strip()) > 2 else 'N/A'

                elif line_number == IMPORTANT_LINE_NUMBERS['tcp_name']:
                    c1_data['TCP Name'] = c2_data['TCP Name'] = line.split('Name:')[1].strip() if len(line.split('Name:')[1].strip()) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['tcp_phone']:
                    c1_data['TCP Phone'] = c2_data['TCP Phone'] = line.split('Phone:')[1].strip() if len(line.split('Phone:')[1].strip()) > 2 else 'N/A'
                elif line_number == IMPORTANT_LINE_NUMBERS['tcp_relationship_and_addy1']:
                    info = get_rexeg_pattern_from_keywords(line, ['Relationship :', 'Address:'])
                    c1_data['TCP Relationship'] = c2_data['TCP Relationship'] = info[1].strip() if len(info[1].strip()) > 2 else 'N/A'
                    tcp_address = info[2].strip() 
                elif line_number == IMPORTANT_LINE_NUMBERS['tcp_addy2']:
                    tcp_address += ' ' + line.strip()
                    c1_data['TCP Address'] = c2_data['TCP Address'] = tcp_address if len(tcp_address) > 2  else 'N/A'

                # elif line_number > 35:
                #     print(line_number)
                #     print(line)


    # print(c1_data)
    # print(c2_data)
    if len(c1_data) < len(customer_data_fields)  :
        return False
    return [c1_data, c2_data]


def convert_all_pdfs():
    all_customer_data = []
    pdf_folder = os.path.join(os.getcwd(), 'pdfs-to-convert')
    current_time = int(datetime.datetime.now().timestamp())
    csv_file = f'pdf-to-csv-{current_time}.csv'
    converted_pdfs_folder = os.path.join(os.getcwd(), 'converted-pdfs')
    os.makedirs(converted_pdfs_folder, exist_ok=True)
    csv_file_path = os.path.join(converted_pdfs_folder, csv_file)
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            try:
                pdf_file_path = os.path.join(pdf_folder, filename)
                customer_data_list = extract_data_from_pdf(pdf_file_path)
                if customer_data_list:
                    all_customer_data.extend(customer_data_list)
            except Exception as e:
                print(e)
                continue

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = all_customer_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_customer_data:
            writer.writerow(data)


convert_all_pdfs()



