import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

while True:
    # Get the audio device and interface
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # Set the audio level to -38.0 dB (equivalent to 20% volume)
    volume.SetMasterVolumeLevel(-65.0, None)
    print("Set volume to -65 db")
    # Wait for 2 seconds before setting the volume again
    time.sleep(2)
