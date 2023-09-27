import os
import hashlib
import json

def calculate_checksum(file_path):
    # Calculate the checksum of a file using SHA-256
    try:
        with open(file_path, 'rb') as file:
            return hashlib.sha256(file.read()).hexdigest()
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def process_folder(folder_path):
    # Initialize an empty dictionary to store the file names and their checksums
    checksum_dict = {}

    # Loop through each item in the folder
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            checksum = calculate_checksum(file_path)
            if checksum is not None:
                relative_path = os.path.relpath(file_path, folder_path)
                checksum_dict[relative_path] = checksum
                print(f"calcolato checksum di {file_path}")

    return checksum_dict

# Specify the folder path where your files are located
folder_path = 'D:\\ArcadeData\\LDJ-003-2022103100\\contents'

# Get the checksum dictionary for the entire folder (including subfolders)
checksum_dict = process_folder(folder_path)

# Specify the path for the JSON output file
json_output_file = 'D:\\KFC-2022122001\\contents\\local-calculated.json'

# Write the checksum dictionary to a JSON file
with open(json_output_file, 'w') as json_file:
    json.dump(checksum_dict, json_file, indent=4)

print("Checksums have been calculated and saved to the JSON file.")
