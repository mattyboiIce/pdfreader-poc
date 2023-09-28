import os

# Get the current working directory
cwd = os.getcwd()

# Get a list of all files in the directory
for filename in os.listdir(cwd):
    # Construct the full file path
    filepath = os.path.join(cwd, filename)
    
    # Check if it is a file
    if os.path.isfile(filepath):
        # Construct the new file name with .txt extension
        base_name = os.path.splitext(filename)[0]
        new_file_name = base_name + '.txt'
        new_file_path = os.path.join(cwd, new_file_name)
        
        # Avoid overwriting the script itself
        if filename != os.path.basename(__file__):
            try:
                # Try to read the file content
                with open(filepath, 'rb') as file:
                    content = file.read()
                
                # Try to decode the content
                try:
                    decoded_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    decoded_content = str(content)
                
                # Write the content to a new .txt file
                with open(new_file_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(decoded_content)
                print(f"Converted {filename} to {new_file_name}")
            except Exception as e:
                print(f"Failed to convert {filename} due to {str(e)}")

print("Conversion process completed.")
