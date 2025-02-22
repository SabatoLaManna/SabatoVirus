@echo off
echo Stopping all Python scripts...

REM Terminate python.exe
taskkill /f /im python.exe >nul 2>&1
if %errorlevel%==0 (
    echo Stopped python.exe processes.
) else (
    echo No python.exe processes found.
)

REM Terminate pythonw.exe
taskkill /f /im pythonw.exe >nul 2>&1
if %errorlevel%==0 (
    echo Stopped pythonw.exe processes.
) else (
    echo No pythonw.exe processes found.
)

REM Final check
tasklist /fi "imagename eq python.exe" /fi "imagename eq pythonw.exe" | find /i "python" >nul
if %errorlevel%==0 (
    echo Some Python processes are still running. Try running as Administrator.
) else (
    echo All Python scripts have been stopped.
)

pause