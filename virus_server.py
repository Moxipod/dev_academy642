import pyautogui
import socket
import threading
import time
import keyboard
from pynput.mouse import Controller
from pynput.mouse import Listener, Button
from tkinter import *
from PIL import Image, ImageTk
import io
import zlib

# --- UI Setup ---
window = Tk()
window.attributes('-fullscreen', True)
window.overrideredirect(True)  # Removes title bar and borders
window.config(bg="black")

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()


def exit_fullscreen(event=None):
    """
    Exit full screen and show window borders when Escape is pressed.
    """
    window.overrideredirect(False)
    window.attributes('-fullscreen', False)


window.bind("<Escape>", exit_fullscreen)

mouse = Controller()

# Label for background image
bg_label = Label(window)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


def create_server(port):
    """
    Create and bind a TCP server socket to listen for a connection.
    :param port: The port to bind the server on.
    :return: The server socket.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(1)
    print("📡 Listening for new connections...")
    return server_socket


def accept_client(server_socket):
    """
    Accepts an incoming client connection.
    :param server_socket: The server socket accepting connections.
    :return: The client socket.
    """
    client_socket, client_address = server_socket.accept()
    print(f"🔌 Connected to {client_address}")
    return client_socket


def check_for_keypress():
    """
    Listens for a key press event.
    :return: The name of the key pressed or "exit" if Esc was pressed.
    """
    if keyboard.is_pressed('esc'):
        print("Exiting key check.")
        return "exit"

    event = keyboard.read_event()
    if event.event_type == "down":
        print(f"⌨️ Key pressed: {event.name}")
        return event.name
    return None


def send_keyboard_input(client_sock):
    """
    Sends a keypress to the client over the socket.
    :param client_sock: The client socket.
    """
    key = check_for_keypress()
    if key and key != "exit":
        try:
            full = b"<<key_Pressed>>" + key.encode() + b"<<END_OF_message>>"
            client_sock.sendall(full)
            print(f"✅ Sent key: {key}")
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Failed to send key: {e}")


def receive_picture(client_sock):
    """
    Receives image frames from the client and displays them in the GUI.
    :param client_sock: The client socket sending image data.
    """
    global bg_label
    buffer = b""

    while True:
        try:
            data = client_sock.recv(4096)
            if not data:
                break

            buffer += data

            while b"<<END_OF_FILE126234>>" in buffer:
                frame_data, buffer = buffer.split(b"<<END_OF_FILE126234>>", 1)

                try:
                    image_stream = io.BytesIO(frame_data)
                    img = Image.open(image_stream)
                    img = img.resize((screen_width, screen_height), Image.ANTIALIAS)

                    photo = ImageTk.PhotoImage(img)
                    bg_label.config(image=photo)
                    bg_label.image = photo

                except Exception as e:
                    print(f"❌ Failed to process one image: {e}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
            break


def send_mouse_position(client_sock, tx, ty):
    """
    Sends the current mouse position to the client, scaled to target resolution.
    :param client_sock: The client socket.
    :param tx: Target screen width (remote).
    :param ty: Target screen height (remote).
    """
    myx, myy = pyautogui.size()
    scale_x = tx / myx
    scale_y = ty / myy
    mouse_x, mouse_y = mouse.position
    cords = str((mouse_x * scale_x, mouse_y * scale_y))
    try:
        full = b"<<sending_cords>>" + cords.encode() + b"<<END_OF_message>>"
        client_sock.sendall(full)
        print(f"🖱️ Sent mouse: {cords}")
    except Exception as e:
        print(f"❌ Failed to send mouse coords: {e}")


def is_socket_connected(sock):
    """
    Check if the socket is still connected.
    :param sock: The socket object.
    :return: True if connection is alive, False otherwise.
    """
    try:
        sock.send(b"ping")
        return True
    except:
        return False


def create_on_click_handler(client_sock):
    """
    Creates a click event handler to send mouse button presses.
    :param client_sock: The client socket.
    :return: A function to handle mouse click events.
    """
    def on_click(x, y, button, pressed):
        if pressed:
            print(f"🖱️ {button} pressed at ({x}, {y})")
            try:
                full = b"<<mouse_press>>" + str(button).encode() + b"<<END_OF_message>>"
                client_sock.sendall(full)
                print(f"🖱️ Sent mouse_button_pressed: {button}")
            except Exception as e:
                print(f"❌ Failed to send mouse button: {e}")
        else:
            print(f"🖱️ {button} released at ({x}, {y})")
    return on_click


def mouse_press_threaded_func(client):
    """
    Runs mouse press listener in a separate thread.
    :param client: The client socket.
    """
    click_handler = create_on_click_handler(client)
    listener = Listener(on_click=click_handler)
    listener.start()


def keyboard_thread_func(sock):
    """
    Continuously sends keyboard input to the client in a thread.
    :param sock: The client socket.
    """
    while True:
        send_keyboard_input(sock)


def mouse_thread_func(sock, tx, ty):
    """
    Continuously sends mouse position to the client in a thread.
    :param sock: The client socket.
    :param tx: Target screen width.
    :param ty: Target screen height.
    """
    last_position = None
    last_sent_time = 0
    while True:
        current_position = mouse.position
        now = time.time()

        if current_position != last_position and now - last_sent_time > 0.1:
            send_mouse_position(sock, tx, ty)
            last_position = current_position
            last_sent_time = now

        time.sleep(0.01)


# --- Main Program ---
if __name__ == "__main__":
    server = create_server(7766)
    client = accept_client(server)
    
    target_size = client.recv(2000)
    tup = tuple(map(float, target_size.decode().split(",")))
    targetx, targety = tup[0], tup[1]
    print(tup)

    server2 = create_server(7767)
    client2 = accept_client(server2)

    threading.Thread(target=keyboard_thread_func, args=(client,), daemon=True).start()
    threading.Thread(target=mouse_thread_func, args=(client, targetx, targety), daemon=True).start()
    threading.Thread(target=mouse_press_threaded_func, args=(client,), daemon=True).start()
    threading.Thread(target=receive_picture, args=(client2,), daemon=True).start()

    window.mainloop()