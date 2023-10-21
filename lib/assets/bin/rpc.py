import pypresence
import time
import psutil
import os
import xml.etree.ElementTree as ET
import asyncio
import websockets
import re

RPC_SDVX = pypresence.Presence(client_id="1150016230200180746")
RPC_IIDX = pypresence.Presence(client_id="1162075373853483049")

tempo = int(time.time())
state = None
large_image = None
# Default presence data for both KFC and LDJ
default_presence_data = {
    "state": "Idle",
    "large_image": "big-loader",
    "large_text": "KNL:I:B:A:2023090300",
    "small_image": "small",
    "small_text": "In Games List",
    "start": tempo,
}

ldj_presence = {
    "state": state,
    "large_image": large_image,
    "large_text": f"LDJ:J:A:A:2023090500",
    "small_image": "small-iidx",
    "small_text": "Connected to instance",
    "start": tempo,
}

KFC_presence_data = {
    "state": state,
    "large_image": "big",
    "large_text": f"KFC:A:G:A:2023042500",
    "small_image": "small",
    "small_text": "Connected to instance",
    "start": tempo,
}

# WebSocket configuration
websocket_address = "localhost"  # Change this address to your WebSocket server's address (TICKERHOOK IS *MANDATORY* FOR IIDX WEBSOCKET CONFIG)
websocket_port = 10573

# Function to update presence data based on KFC logs
def update_presence_from_kfc_log(log_file_path):
    try:
        if os.path.exists(log_file_path):  # Check if the log file exists
            with open(log_file_path, "r", encoding="utf-8", errors="ignore") as log_file:
                state = None
                for line in log_file:
                    if "I:Attach: in APPMAINFLOW" in line:
                        state = "Starting"
                    elif "I:Attach: out NETWORK_CONFIRM" in line or "I:Attach: out ONLINEUPDATE" in line:
                        state = "Connecting to servers"
                    elif "I:Attach: out TITLE_SCENE" in line:
                        state = "In Attract Mode"
                    elif "I:Attach: out CARD_ENTRY_SCENE" in line:
                        state = "Logging in"
                    elif "I:Attach: out CARD_OUT_SCENE" in line:
                        state = "Logging out - Saving Play Data"
                    elif "I:Attach: out CARD_ENTRY_MODE_SELECT_SCENE" in line:
                        state = "Mode Select"
                    elif "I:Attach: out MYROOM_SCENE" in line:
                        state = "My Room"
                    elif "I:Attach: out MUSICSELECT" in line:
                        state = "Chart Select"
                    elif "I:Attach: out ALTERNATIVE_GAME_SCENE" in line:
                        state = "In chart - Playing"
                    elif "I:Attach: out RESULT_SCENE" in line:
                        state = "In Result Screen"
                    elif "I:Attach: out T_RESULT_SCENE" in line:
                        state = "Final Results - Leaving Game"
                    elif "I:Attach: out SKILL LEVEL SELECT" in line:
                        state = "Skill Analyzer - Select Level"
                    elif "I:Attach: out ARENA_MATCHMAKE_SCENE" in line:
                        state = "Arena Mode - Matchmaking"
                    elif "tempo:" in line:
                        try:
                            tempo = int(line.split(":")[1].strip())
                        except ValueError:
                            tempo = int(time.time())

                if state:
                    presence_data = KFC_presence_data.copy()
                    presence_data["state"] = state
                    RPC_SDVX.update(**presence_data)
                    print(f"KFC Presence Data: {presence_data}")
    except Exception as e:
        print(f"Error reading or processing log file: {e}")

# Function to find the path to spice64.exe and read ea3-config.xml
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

                    model = root.find(".//model").text
                    dest = root.find(".//dest").text
                    spec = root.find(".//spec").text
                    rev = root.find(".//rev").text
                    ext = root.find(".//ext").text

                    if model in ("LDJ", "TDJ"):
                        if spec == "B" and ext == "2022082400":
                            RPC_IIDX.connect()
                            presence_data = ldj_presence.copy()
                            presence_data["large_text"] = f"{model}:{dest}:{spec}:{rev}:{ext}"
                            presence_data["large_image"] = "big-iidx-ch"
                            RPC_IIDX.update(**presence_data)
                            print(f"LDJ CH Presence Data: {presence_data}")
                        elif ext == "2023101800":
                            RPC_IIDX.connect()
                            presence_data = ldj_presence.copy()
                            presence_data["large_image"] = "big-iidx-epo"
                            RPC_IIDX.update(**presence_data)
                        else:
                            RPC_IIDX.connect()
                            presence_data = ldj_presence.copy()
                            presence_data["large_text"] = f"{model}:{dest}:{spec}:{rev}:{ext}"
                            presence_data["large_image"] = "big-iidx"
                            RPC_IIDX.update(**presence_data)
                            print(f"LDJ Presence Data: {presence_data}")
                    elif model == "KFC":
                        RPC_SDVX.connect()
                        presence_data = KFC_presence_data.copy()
                        presence_data["large_text"] = f"{model}:{dest}:{spec}:{rev}:{ext}"
                        RPC_SDVX.update(**presence_data)
                        print(f"KFC Presence Data: {presence_data}")
                    log_file_path = os.path.join(os.path.dirname(spice_exe_path), "log.txt")
                    return model, spice_exe_path, log_file_path  # Return model, spice path, and log file path
                except Exception as e:
                    print(f"Error parsing ea3-config.xml: {e}")

    return None, None, None

# WebSocket parsing and updating presence for LDJ
async def connect_websocket():
    uri = f"ws://{websocket_address}:{websocket_port}"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                message = message.strip().upper()
                print(message)
                update_presence_from_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed. Reconnecting...")
                await asyncio.sleep(1)
                continue
            except Exception as e:
                print(f"An error occurred: {e}")

def update_presence_from_message(message):
    presence_data = ldj_presence.copy()
    isCH = "0"
    isEpo = "0"
    if "SELECT FROM ORIGIN" in message:
        origin_category = re.search(r'SELECT FROM ORIGIN (.+?) CATEGORY', message)
        if origin_category:
            origin_category = origin_category.group(1)
            presence_data["state"] = f"In Style List ({origin_category})"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "FAILED.." in message:
        chart_name = re.search(r'(.+?) FAILED', message)
        if chart_name:
            chart_name = chart_name.group(1)
            presence_data["state"] = f"Result Screen - Failed ({chart_name})"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "CLEAR!" in message:
        chart_name = re.search(r'(.+?) CLEAR!', message)
        if chart_name:
            chart_name = chart_name.group(1)
            presence_data["state"] = f"Result Screen - Chart cleared ({chart_name})"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "WELCOME" in message:
        match = re.search(r'WELCOME TO BEATMANIA IIDX(.+)', message)
        welcome_text = ""
        if match:
            welcome_text = match.group(1)
            presence_data["state"] = f"Starting Beatmania IIDX {welcome_text}"
            if "29" in welcome_text:
                presence_data["large_image"] = "big-iidx-ch"
                isCH = "1"
            if "31" in welcome_text:
                presence_data["large_image"] = "big-iidx-epo"
                isEpo = "1"
        else:
            presence_data["state"] = "Starting Beatmania IIDX"
    elif "ENTRY" in message:
        presence_data["state"] = f"Logging In"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "MODE?" in message:
        presence_data["state"] = f"Mode Select"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "STAY COOL" in message:
        presence_data["state"] = f"Premium Start Selected"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "MUSIC SELECT!!" in message:
        presence_data["state"] = f"In Songlist"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "THANK YOU FOR PLAYING!!" in message:
        presence_data["state"] = f"Quitting and Saving Data"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    elif "CONNECTED!" in message:
        presence_data["state"] = f"Booting Game"
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    else:
        presence_data["state"] = message
        if isCH == "1":
            presence_data["large_image"] = "big-iidx-ch"
    
    RPC_IIDX.update(**presence_data)
    print(f"LDJ Presence Data: {presence_data}")

if __name__ == "__main__":
    while True:
        # Find spice64.exe path and read ea3-config.xml
        result = find_spice_exe_path_and_read_ea3_config()
        
        if result is not None:
            model, spice_exe_path, log_file_path = result  # Unpack the result
            # Print the path to spice64.exe as soon as it's found
            if spice_exe_path:
                print(f"spice64.exe found at: {spice_exe_path}")

            # Start the WebSocket connection for LDJ if model is LDJ or TDJ
            if model and model in ("LDJ", "TDJ"):  
                print("BM2DX detected - Starting websocket listener for RPC")
                asyncio.get_event_loop().run_until_complete(connect_websocket())

            # Monitor KFC log and update presence if model is KFC
            if model == "KFC":
                print("SDVX detected - Starting Logreader for RPC")
                while True:
                    if spice_exe_path:
                        update_presence_from_kfc_log(log_file_path)
                    print(log_file_path)
                    print(spice_exe_path)
                    time.sleep(2)  # Adjust the interval as needed
        else:
            print("spice64.exe not found. Waiting...")
            time.sleep(5)