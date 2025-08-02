import pyautogui
import socket
import time
import io
import zlib

def create_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("149.106.246.173", 7767))  # Replace with your server IP
    return s

def send_screen_loop(sock):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            buffer = io.BytesIO()
            screenshot.save(buffer, format="JPEG", quality=30)  # More efficient
            img_bytes = buffer.getvalue()

            compressed = zlib.compress(img_bytes)
            client_socket.sendall(compressed)
            client_socket.sendall(b"<<END_OF_FILE126234>>")

            time.sleep(0.033)  # ~60 FPS
        except Exception as e:
            print(f"❌ Error sending screenshot: {e}")
            break

        

if __name__ == "__main__":
    client_socket = None
    while client_socket is None:
        try:
            client_socket = create_client()
            print("✅ Connected to server")
        except:
            print("Retrying...")
            time.sleep(2)

    send_screen_loop(client_socket)
