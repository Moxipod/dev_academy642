# client.py
import pyautogui
import socket
import threading
import time
import keyboard
from pynput.mouse import Controller
from pynput.mouse import Listener, Button
import io
# import zlib  # Removed because it's no longer used

screen_width, screen_height = pyautogui.size()
mouse = Controller()

def create_client(port):
    """
    Create a TCP socket connection to the server on the specified port.

    Args:
        port (int): The port number to connect to.

    Returns:
        socket.socket: The connected socket object.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("149.106.246.173", port))  # Replace with your server IP
    return s

def connect_to_server():
    """
    Try to connect to the control server on port 7766.

    Returns:
        bool: True if connection was successful, False otherwise.
    """
    global client_socket
    try:
        client_socket = create_client(7766)
        print("✅ Connected to server")
        return True
    except Exception as e:
        print(f"❌ No server detected: {e}")
        return False

def handle_mouse(cords_str):
    """
    Move the mouse to the given screen coordinates.

    Args:
        cords_str (str): A string like '(x,y)' representing coordinates.
    """
    try:
        print(f"🖱️ Moving mouse to: {cords_str}")
        cords_tuple = tuple(map(float, cords_str.strip("()").split(",")))
        mouse.position = cords_tuple
    except Exception as e:
        print(f"❌ Error moving mouse: {e}")

def handle_keyboard(key):
    """
    Simulate a key press and release on the local machine.

    Args:
        key (str): The key to press (e.g., 'a', 'ctrl+c').
    """
    try:
        keyboard.press_and_release(key)
        print(f"⌨️ Typed: {key}")
    except Exception as e:
        print(f"❌ Invalid key received: {e}")

def handle_mouse_press(butoon):
    """
    Simulate a mouse click (left or right button).

    Args:
        butoon (str): String representation of button (e.g., 'Button.left').
    """
    button_str = butoon
    print(button_str)
    try:
        if button_str == "Button.left":
            mouse.click(Button.left)
        elif button_str == "Button.right":
            mouse.click(Button.right)
        else:
            print(f"❌ Unknown button: {button_str}")
    except Exception as e:
        print(f"❌ Error pressing mouse button: {e}")

def send_screen_loop(client_socket):
    """
    Continuously capture the screen, compress to JPEG, and send to server.

    Args:
        client_socket (socket.socket): The socket used to send screen frames.
    """
    while True:
        try:
            screenshot = pyautogui.screenshot()
            buffer = io.BytesIO()
            screenshot.save(buffer, format="JPEG", quality=30)
            img_bytes = buffer.getvalue()

            client_socket.sendall(img_bytes)
            client_socket.sendall(b"<<END_OF_FILE126234>>")

            time.sleep(0.033)  # ~30 FPS
        except Exception as e:
            print(f"❌ Error sending screenshot: {e}")
            break

def listener_thread():
    """
    Listen for control commands (keyboard, mouse movement, mouse click) from the server.
    """
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

                if b"<<END_OF_message>>" in buffer:
                    # Handle key press
                    if b"<<key_Pressed>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<key_Pressed>>'):]}")
                        handle_keyboard(full_msg[len('<<key_Pressed>>'):])

                    # Handle mouse movement
                    if b"<<sending_cords>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<sending_cords>>'):]}")
                        handle_mouse(full_msg[len('<<sending_cords>>'):])

                    # Handle mouse press
                    if b"<<mouse_press>>" in buffer:
                        msg = buffer.decode()
                        full_msg, msg = msg.split("<<END_OF_message>>", 1)
                        print(f"📥 Received full message: {full_msg[len('<<mouse_press>>'):]}")
                        handle_mouse_press(full_msg[len('<<mouse_press>>'):])

            except Exception as e:
                print(f"❌ Listener error: {e}")

# --- Main Execution ---

if __name__ == "__main__":
    # Keep trying until server is reachable
    while not connect_to_server():
        time.sleep(3)

    # Send screen resolution info to server
    str1 = f"{screen_width},{screen_height}"
    client_socket.send(str1.encode())

    # Create a second socket for streaming screen frames
    socket2 = create_client(7767)

    # Start screen sending in a separate thread
    threading.Thread(target=send_screen_loop, args=(socket2,), daemon=True).start()

    # Run listener for mouse/keyboard commands (runs forever)
    listener_thread()

    # Keep the program alive
    while True:
        time.sleep(1)
