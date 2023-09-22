@echo off
setlocal enabledelayedexpansion


for %%A in ("%cd%") do set "current_directory=%%~fA"

rem Define the folder path
set "folderPath=D:\ArcadeData\LDJ-003-2022103100\contents"

rem Check if the folder exists
if not exist "%folderPath%" (
    echo The folder does not exist: %folderPath%
    exit /b 1
)

rem Change directory to the specified folder

cd "!current_directory!/lib/assets/bin"
dir
start "" python bm2dxaudio.py
echo "started 2dx audio patch"
start "" python rpc.py
echo "started discord rpc event"
start "" python statcounter.py
echo "started statcount event"

cd /d "%folderPath%"

rem Start spice64.exe as an administrator in a minimized window
start /min "" "spice64.exe"

endlocal


pause