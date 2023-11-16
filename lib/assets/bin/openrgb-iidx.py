import os
import psutil
import xml.etree.ElementTree as ET
import websockets
import re
import asyncio
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType

client = OpenRGBClient()
client.clear()
keyboard = client.get_devices_by_type(DeviceType.KEYBOARD)[0]


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

websocket_address = "localhost"  # must be executed locally.
websocket_port = 10573


async def connect_websocket():
    client = OpenRGBClient()
    client.clear()
    keyboard = client.get_devices_by_type(DeviceType.KEYBOARD)[0]
    keyboard.set_color(RGBColor(250, 231, 21))
    print(keyboard)
    uri = f"ws://{websocket_address}:{websocket_port}"
    reconnecting = False  # Initialize the reconnecting flag
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                try:
                    message = await websocket.recv()
                    message = message.strip().upper()
                    print(message)
                    if "CONNECTED!" in message:
                        keyboard.set_color(RGBColor(0, 255, 0))
                    elif "WELCOME" in message:
                        match = re.search(r'WELCOME TO BEATMANIA IIDX(.+)', message)
                        welcome_text = ""
                        if match:
                            welcome_text = match.group(1)
                            print(welcome_text)
                        if welcome_text == "31 EPOLIS":
                            keyboard.set_color(RGBColor(250, 231, 21))
                            keyboard.set_mode("breathing")
                        elif welcome_text == "30 RESIDENT":
                            keyboard.set_color(RGBColor(21, 250, 263))
                            keyboard.set_mode("breathing")
                        elif welcome_text == "29 CASTHOUR":
                            keyboard.set_color(RGBColor(255, 65, 0))
                            keyboard.set_mode("breathing")
                        elif welcome_text == "28 BISTROVER":
                            keyboard.set_color(RGBColor(2, 129, 230))
                            keyboard.set_mode("breathing")
                        elif welcome_text == "27 HEROIC VERSE":
                            keyboard.set_color(RGBColor(143, 111, 186))
                            keyboard.set_mode("breathing")
                        elif welcome_text == "26 ROOTAGE":
                            keyboard.set_color(RGBColor(214, 53, 6))
                            keyboard.set_mode("breathing")
                    elif "SELECT FROM ORIGIN" in message:
                        origin_category = re.search(r'SELECT FROM ORIGIN (.+?) CATEGORY', message)
                        if origin_category == "epolis":
                            keyboard.set_color(RGBColor(250, 231, 21))
                            keyboard.set_mode("static")
                        elif origin_category == "resident":
                            keyboard.set_color(RGBColor(21, 250, 263))
                            keyboard.set_mode("static")
                        elif origin_category == "casthour":
                            keyboard.set_color(RGBColor(255, 65, 0))
                            keyboard.set_mode("static")
                        elif origin_category == "bistrover":
                            keyboard.set_color(RGBColor(2, 129, 230))
                            keyboard.set_mode("static")
                        elif origin_category == "heroic verse":
                            keyboard.set_color(RGBColor(143, 111, 186))
                            keyboard.set_mode("static")
                        elif origin_category == "rootage":
                            keyboard.set_color(RGBColor(214, 53, 6))
                            keyboard.set_mode("static")
                    elif "CLEAR!" in message:
                        keyboard.set_color(RGBColor(21, 250, 263))
                        keyboard.set_mode("breathing")
                    elif "FAILED.." in message:
                        print("skrill issue")
                        keyboard.set_color(RGBColor(251, 0, 0))
                        keyboard.set_mode("breathing")
                    reconnecting = False  # Reset the reconnecting flag when a message is received
                except websockets.exceptions.ConnectionClosed:
                    if not reconnecting:
                        print("Connection closed. Reconnecting...")
                        reconnecting = True  # Set the reconnecting flag when connection is closed
                        timeout_task = asyncio.create_task(asyncio.sleep(10))  # Start a 10-second timer
                    try:
                        await asyncio.wait_for(timeout_task, 10)  # Wait for up to 10 seconds
                    except asyncio.TimeoutError:
                        print("Timeout: No message received for 10 seconds. Disconnecting the API and quitting tickerhookWS")
                        print("sl2dx disconnected. Goodbye :D")
                        raise SystemExit
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

