import os
import time
import psutil
import json
import xml.etree.ElementTree as ET

def get_model_from_xml(xml_path):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        model_element = root.find(".//model")
        if model_element is not None:
            return model_element.text.strip()
        else:
            return None
    except Exception as e:
        print(f"Error reading XML: {str(e)}")
        return None

def load_json(json_filename):
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as json_file:
            return json.load(json_file)
    return {}

def main():
    spice_process = None
    model = None
    json_filename = None
    total_runtime = 0.0
    session_runtime = 0.0

    while True:
        # Check if Spice64 is running
        if spice_process is None or not spice_process.is_running():
            # Find the Spice64 process by name
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if proc.info['name'] == 'spice64.exe':
                    spice_process = psutil.Process(proc.info['pid'])
                    break

            if spice_process is not None:
                # Get the path of Spice64
                spice_path = os.path.dirname(spice_process.exe())

                # Look for ea3-settings.xml and get the model
                xml_path = os.path.join(spice_path, 'prop', 'ea3-config.xml')
                model = get_model_from_xml(xml_path)

                if model:
                    # Prepare the JSON filename
                    json_filename = f'{model}.json'
                    # Load existing JSON data
                    json_data = load_json(json_filename)
                    if 'total-runtime' in json_data:
                        total_runtime = float(json_data['total-runtime'])
                    if 'last-session' in json_data:
                        last_session_runtime = float(json_data['last-session'])

        if spice_process is not None:
            if spice_process.is_running():
                # Calculate the runtime in minutes
                runtime_seconds = spice_process.create_time()
                runtime_minutes = (time.time() - runtime_seconds) / 60
                total_runtime += runtime_minutes
                session_runtime += runtime_minutes
                # Save the data to the JSON file
                if json_filename:
                    data = {
                        "total-runtime": total_runtime,
                        "last-session": session_runtime
                    }
                    with open(json_filename, 'w') as json_file:
                        json.dump(data, json_file, indent=2)
            else:
                # Spice64 process has terminated, stop counting and reset last session
                spice_process = None

        time.sleep(2)

if __name__ == "__main__":
    main()
