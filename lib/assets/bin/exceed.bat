@echo off
setlocal enabledelayedexpansion


for %%A in ("%cd%") do set "current_directory=%%~fA"

rem Define the folder path
set "folderPath=E:\KFC-2022122001\contents"

rem Check if the folder exists
if not exist "%folderPath%" (
    echo The folder does not exist: %folderPath%
    exit /b 1
)

rem Change directory to the specified folder

cd "!current_directory!/lib/assets/bin"

rem Start rpc.py in a separate minimized window
start /min "" python rpc.py

rem Start statcounter.py in a separate minimized window
start /min "" python statcounter.py

cd /d "%folderPath%"

rem Start spice64.exe as an administrator in a minimized window
start /min "" "spice64.exe"

endlocal
