@echo off
setlocal enabledelayedexpansion

for %%A in ("%cd%") do set "current_directory=%%~fA"

cd "!current_directory!"

start %~dp0resi.bat