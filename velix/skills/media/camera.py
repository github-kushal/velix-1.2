import os 
import pyautogui
import time

def open_camera():
    os.system("start microsoft.windows.camera:")

def take_ss():
    try:
        pyautogui.hotkey('win','shift', 's')
    except Exception as e:
        raise e
    

# open_camera()