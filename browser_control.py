import sys
from pathlib import Path

# Add the parent directory to sys.path so velix can be imported
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

#  open_browser()
#  close_browser()
#  restart_browser()
#  focus_browser()
#  is_browser_running()
#  open_url()
#  new_tab()
#  close_tab()
#  refresh()
#  back()
#  forward()
#  get_current_url()
#  get_page_title()
from velix.skills.browser.web_search import WebSearch as wb
from voice.listener import Listener
from voice.speaker import speak
import pyautogui 


def open_browser():
    wb.open_browser()

def close(browser="msedge"):
    import os
    os.system(f"taskkill /im {browser}.exe /f")

def search(query):
    speak("Please tell what do you want to search.")
    query = Listener.listen()
    wb.web_search(query=query)

def activate_window(browser="edge"):
    import pygetwindow as gw
    import time
    try:
        windows = gw.getWindowsWithTitle(browser)
        if not windows:
            speak("Sorry i could not find the window")
            return False
        
        win = windows[0]

        if win.isMinimized:
            win.restore()

        win.activate()
        time.sleep(0.5)
        return True
        
    except Exception as e:
        print(f"Error : {e}")
        return False
    
def new_tab():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+t')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def close_tab():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+w')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def next_tab():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+tab')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def pre_tab():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+shift+tab')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def new_win():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+n')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def incog():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+shift+n')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def refresh():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+shift+r')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def downloads():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+j')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def history():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+h')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

def bookmarks():
    activate_window()
    import keyboard
    try:
        keyboard.press_and_release('ctrl+d')  # Correct shortcut for new tab
    except Exception as e:
        print(f"Error opening new tab: {e}")

