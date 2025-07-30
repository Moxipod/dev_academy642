# client.py
import pyautogui
import socket
import threading
import time
import keyboard
from pynput.mouse import Controller
from pynput.mouse import Listener, Button

screen_width, screen_height = pyautogui.size()

mouse = Controller()

def create_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # s.settimeout(3)
    s.connect(("149.106.246.173", 7766))  # Replace with your server IP
    return s

def connect_to_server():
    global client_socket
    try:
        client_socket = create_client()
        print("✅ Connected to server")
        return True
    except Exception as e:
        print(f"❌ No server detected: {e}")
        return False

def handle_mouse(cords_str):
    try:
       # cords_str = cords_data.decode().strip()
        print(f"🖱️ Moving mouse to: {cords_str}")

        # Remove parentheses and split by comma
        cords_tuple = tuple(map(float, cords_str.strip("()").split(",")))

        # Move the mouse
        mouse.position = cords_tuple

    except Exception as e:
        print(f"❌ Error moving mouse: {e}")

def handle_keyboard(key):
    try:
        #key = key_data.decode()
        keyboard.press_and_release(key)
        print(f"⌨️ Typed: {key}")
    except Exception as e:
        print(f"❌ Invalid key received: {e}")

def handle_mouse_press(butoon):
    button_str = "Bu"+butoon
    print(button_str)
    try:
        if button_str == "Button.left":
            mouse.press(Button.left)
        elif button_str == "Button.right":
            mouse.press(Button.right)
        else:
            print(f"❌ Unknown button: {button_str}")
    except Exception as e:
        print(f"❌ Error pressing mouse button: {e}")



def listener_thread():
    buffer = b""
    global client_socket
    while True:
        buffer = b""
        while b"<<END_OF_message>>" not in buffer:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("❌ Disconnected from server.")
                    break

                buffer += data

                # Process all complete messages
                if b"<<END_OF_message>>" in buffer :
                    if b"<<key_Pressed>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1) 
                        #full_msg, buffer = buffer.split(b"<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<key_Pressed>>'):]}")
                        handle_keyboard(full_msg[len('<<key_Pressed>>'):])

                    if b"<<sending_cords>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1) 
                        #full_msg, buffer = buffer.split(b"<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<sending_cords>>'):]}")
                        handle_mouse(full_msg[len('<<sending_cords>>'):])

                    if b"<<mouse_press>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1) 
                        #full_msg, buffer = buffer.split(b"<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<sending_cords>>'):]}")
                        handle_mouse_press(full_msg[len('<<sending_cords>>'):])
                    
            except Exception as e:
                print(f"❌ Listener error: {e}")
                #break


if __name__ == "__main__":
    while not connect_to_server():
        time.sleep(3)

    str1 = f"{screen_width},{screen_height}"
    client_socket.send(str1.encode())


    listener_thread()

   # threading.Thread(target=listener_thread, daemon=True).start()
   

    while True:
        time.sleep(1)
