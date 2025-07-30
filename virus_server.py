# server.py
import pyautogui
import socket
import threading
import time
import keyboard
from pynput.mouse import Controller
from pynput.mouse import Listener,Button

mouse = Controller()

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 7766))
    server_socket.listen(1)
    print("📡 Listening for new connections...")
    return server_socket

def accept_client(server_socket):
    client_socket, client_address = server_socket.accept()
    print(f"🔌 Connected to {client_address}")
    return client_socket

def check_for_keypress():
    if keyboard.is_pressed('esc'):
        print("Exiting key check.")
        return "exit"

    event = keyboard.read_event()
    if event.event_type == "down":
        print(f"⌨️ Key pressed: {event.name}")
        return event.name
    return None

def send_keyboard_input(client_sock):
    key = check_for_keypress()
    if key and key != "exit":
        try:
            full = b"<<key_Pressed>>" + key.encode() + b"<<END_OF_message>>"
            #client_sock.send(b"<<key_Pressed>>")
            #client_sock.send(key.encode())
            #client_sock.send(b"<<END_OF_key>>")
            client_sock.sendall(full)
            print(f"✅ Sent key: {key}")
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Failed to send key: {e}")

def send_mouse_position(client_sock,tx,ty):
    myx,myy = pyautogui.size()
    scale_x =tx/myx
    scale_y =ty/myy
    mouse_x,mouse_y = (mouse.position)
    cords =str((mouse_x*scale_x,mouse_y*scale_y))
    try:
        full = b"<<sending_cords>>" + cords.encode() + b"<<END_OF_message>>"
       # client_sock.send(b"<<sending_cords>>")
        #client_sock.send(cords.encode())
        #client_sock.send(b"<<finish_cords>>")
        client_sock.sendall(full)
        print(f"🖱️ Sent mouse: {cords}")
    except Exception as e:
        print(f"❌ Failed to send mouse coords: {e}")

def is_socket_connected(sock):
    try:
        sock.send(b"ping")
        return True
    except:
        return False


def create_on_click_handler(client_sock):
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
    click_handler = create_on_click_handler(client)
    listener = Listener(on_click=click_handler)
    listener.start()


def keyboard_thread_func(sock):
    while True:
        send_keyboard_input(sock)



def mouse_thread_func(sock,tx,ty):
    last_position = None
    last_sent_time = 0
    while True:
        current_position = mouse.position
        now = time.time()

        if current_position != last_position and now - last_sent_time > 0.1:
            send_mouse_position(sock,tx,ty)
            last_position = current_position
            last_sent_time = now

        time.sleep(0.01)




if __name__ == "__main__":
    server = create_server()
    while True:
        client = accept_client(server)
        target_size=client.recv(2000)
        tup = tuple(map(float,target_size.decode().split(",")))
        targetx,targety=tup[0],tup[1]
        print(tup)


        threading.Thread(target=keyboard_thread_func, args=(client,), daemon=True).start()
        threading.Thread(target=mouse_thread_func, args=(client,targetx,targety), daemon=True).start()
        threading.Thread(target=mouse_press_threaded_func, args=(client,), daemon=True).start()

