import os
import psutil
import xml.etree.ElementTree as ET
import websockets
import re
import asyncio
import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
import requests
import random
import json



def main():
    while True:
        result = find_spice_exe_path_and_read_ea3_config()
        
        if result is not None:
            model, spice_exe_path = result
            if spice_exe_path:
                print(f"spice64.exe found at: {spice_exe_path}")

            if model and model in ("LDJ", "TDJ"):
                asyncio.run(connect_websocket())

def find_spice_exe_path_and_read_ea3_config():
    for p in psutil.process_iter(attrs=["name", "exe"]):
        if p.info["name"] == "spice64.exe":
            spice_exe_path = p.info["exe"]
            prop_folder = os.path.join(os.path.dirname(spice_exe_path), "prop")
            ea3_config_path = os.path.join(prop_folder, "ea3-config.xml")

            if os.path.exists(ea3_config_path):
                try:
                    tree = ET.parse(ea3_config_path)
                    root = tree.getroot()

                    model = root.find(".//model")

                    if all(element is not None for element in [model]):
                        model = model.text
                        return model, spice_exe_path
                    else:
                        print("One or more elements not found in ea3-config.xml")
                except Exception as e:
                    print(f"An error occurred while parsing ea3-config.xml: {e}")

    # If no matching process or config file was found, return None
    return None

websocket_address = "localhost"  # Change this address to your WebSocket server's address if you're running rpc on a separate machine(REMEMBER THAT TICKERHOOK IS *MANDATORY* FOR IIDX WEBSOCKET CONFIG)
websocket_port = 10573

async def connect_websocket():
    uri = f"ws://{websocket_address}:{websocket_port}"
    reconnecting = False  # Initialize the reconnecting flag
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    message = message.strip().upper()
                    print(message)
                    if "CLEAR!" in message:
                        cleared_shock()
                    if "FAILED.." in message:
                        shock_function()
                    reconnecting = False  # Reset the reconnecting flag when a message is received
                except websockets.exceptions.ConnectionClosed:
                    if not reconnecting:
                        print("Connection closed. Reconnecting...")
                        reconnecting = True  # Set the reconnecting flag when connection is closed
                        timeout_task = asyncio.create_task(asyncio.sleep(10))  # Start a 10-second timer
                    try:
                        await asyncio.wait_for(timeout_task, 10)  # Wait for up to 10 seconds
                    except asyncio.TimeoutError:
                        print("Timeout: No message received for 10 seconds. Leaving RPC and quitting loop...")
                        print("IIDX Rpc disconnected. Goodbye :D")
                        raise SystemExit
    except Exception as e:
        print(f"An error occurred: {e}")

def shock_function():
    min_shock = 1
    max_shock = 100 
    min_time = 1
    max_time = 10
    shocker_id = ""
    target_url = "https://api.shocklink.net/1/shockers/control" 
    api_key = "" #generate an api key from the shocklink dashboard
    rand_shock = random.uniform(min_shock, max_shock)
    rand_time = random.uniform(min_time, max_time)
    rand_time_millis = int(rand_time * 1000)

    request_data = [
        {
            "id": shocker_id,
            "type": 0,
            "intensity": rand_shock,
            "duration": rand_time_millis
        }
    ]

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        "OpenShockToken": api_key
    }

    try:
        response = requests.post(target_url, data=json.dumps(request_data), headers=headers)
        if response.status_code == 200:
            print("Shock request sent successfully.")
        else:
            print(f"Failed to send shock request. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while sending the shock request: {e}")


def cleared_shock():
    score_threshold = 250
    window_title_regex = r"Beatmania IIDX \w+ main"
    screenshot_filename = "screenshot.png"

    pyautogui.screenshot(screenshot_filename)
    windows = pyautogui.getWindows()
    target_window = None
    for window in windows:
        if re.match(window_title_regex, window.title):
            target_window = window
            break

    if target_window:
        left = target_window.left + 404
        top = target_window.top + 550
        right = target_window.left + 494
        bottom = target_window.top + 572

        screenshot = cv2.imread(screenshot_filename)
        cropped = screenshot[top:bottom, left:right]

        cv2.imwrite("cropped_screenshot.png", cropped)

        extracted_text = pytesseract.image_to_string(Image.fromarray(cropped))
        numbers = re.findall(r'\d+', extracted_text)

        if numbers:
            for number in numbers:
                number = int(number)
                print(f"Extracted Number: {number}")

                if number <= score_threshold:
                    shock_function()
    else:
        print("Window not found")

if __name__ == "__main__":
    main()

