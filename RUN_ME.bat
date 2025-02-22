@echo off
REM Hide the window
if not "%1"=="hidden" (
    start /b /min cmd /c "%~f0" hidden
    exit /b
)

REM Get the parent folder of this script
set "parent_folder=%~dp0"

REM Remove trailing backslash
set "parent_folder=%parent_folder:~0,-1%"

REM Get the folder name
for %%A in ("%parent_folder%") do set "folder_name=%%~nxA"

REM Define the destination path (Documents folder)
set "destination=%USERPROFILE%\Documents\%folder_name%"

REM Copy the parent folder to the Documents folder
xcopy "%parent_folder%" "%destination%" /E /H /C /I /Y

REM Check if Install.bat exists in the copied folder
if exist "%destination%\Install.bat" (
    cd /d "%destination%"
    call Install.bat
)