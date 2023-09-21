import json
import os
import hashlib
import subprocess

# Function to calculate the checksum of a file
def calculate_checksum(file_path, algorithm="sha256"):
    hasher = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

# Load checksums from "output.json"
try:
    with open("known-good-0912.json", "r") as json_file:
        checksum_data = json.load(json_file)
except FileNotFoundError:
    print("Error: The 'output.json' file is not found.")
    exit(1)

# Specify the folder containing files to verify
folder_path = "D:\\KFC-2022122001\\contents"

# Verify checksums for files in the specified folder
for filename, expected_checksum in checksum_data.items():
    file_path = os.path.join(folder_path, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: File '{filename}' not found in the specified folder.")
    else:
        actual_checksum = calculate_checksum(file_path)
        if actual_checksum == expected_checksum:
            print(f"Checksum for '{filename}' is valid.")
        else:
            print(f"Error: Checksum for '{filename}' does not match the expected value.")
            print(f"Expected: {expected_checksum}")
            print(f"Actual  : {actual_checksum}")

# Start spice64.exe in the same folder as "output.json"
spice_exe_path = os.path.join("D:\\KFC-2022122001\\contents\\spice64.exe")

if os.path.exists(spice_exe_path):
    subprocess.Popen([spice_exe_path])
else:
    print("Error: 'spice64.exe' not found in the same folder as 'output.json'.")

