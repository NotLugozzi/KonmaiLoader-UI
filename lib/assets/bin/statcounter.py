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
    game_data = {}  # Dictionary to store game data for different models

    while True:
        # Check if Spice64 is running
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name'] == 'spice64.exe':
                spice_process = psutil.Process(proc.info['pid'])
                break
        else:
            spice_process = None

        if spice_process is not None:
            # Get the path of Spice64
            spice_path = os.path.dirname(spice_process.exe())

            # Look for ea3-settings.xml and get the model
            xml_path = os.path.join(spice_path, 'prop', 'ea3-config.xml')
            model = get_model_from_xml(xml_path)

            if model:
                # Prepare the JSON filename
                json_filename = f'{model}.json'
                if json_filename not in game_data:
                    # Load existing JSON data if it's not already loaded
                    game_data[json_filename] = load_json(json_filename)
                    if 'total-runtime' not in game_data[json_filename]:
                        game_data[json_filename]['total-runtime'] = 0.0
                    if 'last-session' not in game_data[json_filename]:
                        game_data[json_filename]['last-session'] = 0.0

            if spice_process.is_running():
                # Calculate the runtime in seconds
                runtime_seconds = spice_process.create_time()
                runtime_hours, remainder_seconds = divmod(time.time() - runtime_seconds, 3600)
                runtime_minutes, runtime_seconds = divmod(remainder_seconds, 60)
                
                # Update the total runtime and last session in hours:minutes:seconds format
                total_runtime_hms = f"{int(runtime_hours):02d}:{int(runtime_minutes):02d}:{int(runtime_seconds):02d}"
                game_data[json_filename]['total-runtime'] = total_runtime_hms
                game_data[json_filename]['last-session'] = total_runtime_hms
                
                # Save the data to the JSON file
                with open(json_filename, 'w') as json_file:
                    json.dump(game_data[json_filename], json_file, indent=2)
            else:
                # Spice64 process has terminated, stop counting and reset last session
                game_data[json_filename]['last-session'] = "00:00:00"

            time.sleep(2)

if __name__ == "__main__":
    main()
