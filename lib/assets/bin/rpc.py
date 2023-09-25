import tkinter as tk
import pypresence
import time
import psutil
import threading
import os
import xml.etree.ElementTree as ET

RPC = pypresence.Presence(client_id="1150016230200180746")
RPC.connect()
tempo = int(time.time())

idle_presence_data = {
    "state": "Idle",
    "large_image": "big-loader",
    "large_text": "KNL:I:B:A:2023090300",
    "small_image": "small",
    "small_text": "In Games List",
    "start": tempo,
}

def update_presence(presence_data):
    RPC.update(**presence_data)

def find_spice_exe_path():
    for p in psutil.process_iter(attrs=["name", "exe"]):
        if p.info["name"] == "spice64.exe":
            return p.info["exe"]
    return None

# is this bad? possibly. does it break with shift_jis? also yes. do i give a fuck? no. use utf8 dipshit
# this should work with all games that use ea3-config.xml.(although we officially support onlly sdvx autorpc and IIDX manualRPC)
# just like 99% of shit on kml it's like half untested half thrown together in class or after drinking and it might possibly break like tomorrow 


def extract_info_from_ea3_config(config_path): 
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()

        model = root.find(".//model").text
        dest = root.find(".//dest").text
        spec = root.find(".//spec").text
        rev = root.find(".//rev").text
        ext = root.find(".//ext").text

        return model, dest, spec, rev, ext
        
    except Exception as e:
        print(f"Error parsing ea3-config.xml: {e}")
        return None, None, None, None, None
    
def read_game_log():
    global tempo
    
    log_file_path = os.path.join(os.path.dirname(find_spice_exe_path()), "log.txt")
    try:
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
                presence_data = {
                    "state": state,
                    "large_image": "big",
                    "large_text": f"KFC:A:G:A:2023042500",
                    "small_image": "small",
                    "small_text": "Connected to instance",
                    "start": tempo,
                }
                update_presence(presence_data)
    except FileNotFoundError:
        pass #this shouldn't happen as all loaders make at least one log file.
    except Exception as e:
        print(f"Error reading log file: {e}")



def check_spice_window():
    log_check_interval = 2  
    initial_presence_set = False

    while True:
        print("Checking for 'spice64.exe' window...")
        spice_exe_path = find_spice_exe_path()

        if spice_exe_path:
            print("'spice64.exe' window found.")
            print("Path of 'spice64.exe':", spice_exe_path)

            prop_folder = os.path.join(os.path.dirname(spice_exe_path), "prop")
            ea3_config_path = os.path.join(prop_folder, "ea3-config.xml")

            if os.path.exists(ea3_config_path):
                print("ea3-config.xml found.")
                model, dest, spec, rev, ext = extract_info_from_ea3_config(ea3_config_path)

                print(model, dest, spec, rev, ext)
                if model == "KFC" and not initial_presence_set:
                    presence_data = idle_presence_data
                    update_presence(presence_data)
                    initial_presence_set = True
                elif model == "LDJ":
                    presence_data = {
                        "state": "Premium Free (playing)",
                        "large_image": "big-iidx",
                        "large_text": f"{model}:{dest}:{spec}:{rev}:{ext}",
                        "small_image": "small-iidx",
                        "small_text": "Connected to instance",
                        "start": tempo,
                    }
                    update_presence(presence_data)

            read_game_log()
        else:
            print("'spice64.exe' window not found.")
            initial_presence_set = False 
        time.sleep(log_check_interval)



def button_click(button_text):
    RPC.clear()
    if button_text in ["Attract Mode", "My Room"]:
        presence_data = {
            "state": button_text,
            "large_image": "big",
            "large_text": "KFC:A:G:A:2023042500",
            "small_image": "small",
            "small_text": "Not connected to an instance",
            "start": tempo
        }
    elif button_text == "Starting":
        presence_data = {
            "state": button_text,
            "details": "KonmaiLoader Bootstrap - Information Unavailable",
            "large_image": "big",
            "large_text": "KonmaiLoader Bootstrap - Unable to get version",
            "small_image": "small",
            "small_text": "Not connected to an instance",
            "start": tempo
        }
    else:
        presence_data = {
            "state": button_text,
            "large_image": "big",
            "large_text": "KFC:A:G:A:2023042500",
            "small_image": "small",
            "small_text": "Connected to instance",
            "start": tempo
        }
    update_presence(presence_data)



def on_closing():
    RPC.clear()
    root.destroy()


def create_gui():
    global root
    root = tk.Tk()
    root.title("Discord Rich Presence")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_presence(idle_presence_data)
    button_labels = ["Starting", "Attract Mode", "My Room", "Playing Normal Mode", "With a friend", "Paradise Start", "Premium Time (Playing)", "BLASTER", "Skill Analyzer", "Arena Battle", "Megamix Battle", "Single Battle"]
    buttons = []

    for label in button_labels:
        button = tk.Button(root, text=label, command=lambda l=label: button_click(l))
        button.pack()
        buttons.append(button)

    root.mainloop()

# Create and start the threadshre
spice_thread = threading.Thread(target=check_spice_window)
spice_thread.daemon = True
spice_thread.start()

gui_thread = threading.Thread(target=create_gui)
gui_thread.daemon = True
gui_thread.start()

# Keep the main thread alive
time.sleep(8000)
