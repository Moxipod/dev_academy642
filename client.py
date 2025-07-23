import socket
import threading
from tkinter import *
from tkinter import filedialog
import os
import time

file_path = ""
client_socket = None  # Global socket
downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
fille_to_download =""
# --- UI Setup ---
window = Tk()
window.geometry("2000x1200")
window.title("Guy's File Sender")
window.config(bg="#2c3e50")

headline_label = Label(
    text="Guy's File Sender",
    font=("Arial", 24, "bold"),
    bg="#2c3e50", fg="white"
)
headline_label.place(relx=0.5, rely=0.1, anchor="center")

separator = Frame(window, bg="white", height=2, width=400)
separator.place(relx=0.5, rely=0.17, anchor="center")

server_listbox = Listbox(window, width=50, height=10, font=("Arial", 12))
server_listbox.place(relx=0.5, rely=0.85, anchor="center")

# Listbox click event
def on_listbox_select(event):
    """
    When a file is selected from the listbox, update the label and store the selected filename.
    """
    global fille_to_download
    selection = server_listbox.curselection()
    if selection:
        selected_file = server_listbox.get(selection[0])
        fille_to_download = selected_file
        result_label.config(text=f" Selected: {selected_file}")

def get_file():
    """
    Open file dialog to choose a file to upload. Updates global `file_path`.
    """
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        result_label.config(text=f"Selected: {file_path}")
    else:
        result_label.config(text="No file selected.")

def request_file_list():
    """
    Send request to server for available file list and update the Listbox.
    """
    global server_listbox
    if client_socket is None:
        result_label.config(text="❌ Connect to server first!")
        return

    try:
        client_socket.send(b"<<GET_FILE_LIST>>")
        raw_len = client_socket.recv(4)
        list_len = int.from_bytes(raw_len, 'big')

        data = b""
        while len(data) < list_len:
            packet = client_socket.recv(1024)
            data += packet

        files_str = data.decode()
        file_list = files_str.split("::") if files_str else []

        server_listbox.delete(0, END)
        for file in file_list:
            server_listbox.insert(END, file)

        result_label.config(text="📁 File list received from server.")
    except Exception as e:
        result_label.config(text=f"❌ Failed to get file list: {e}")

def threaded_request_file_list():
    """
    Create a thread to request file list from the server without freezing the UI.
    """
    global client_socket
    if client_socket is None:
        result_label.config(text="❌ Connect to server first!")
        return
    threading.Thread(target=request_file_list).start()

def threaded_send_file():
    """
    Create a thread to send selected file to the server.
    """
    global client_socket, file_path
    if client_socket is None:
        result_label.config(text="❌ Connect to server first!")
        return
    if not file_path:
        result_label.config(text="❌ Select a file first!")
        return
    threading.Thread(target=upload_file, args=(client_socket, file_path)).start()

def create_client():
    """
    Create a TCP client socket and connect to the server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("149.106.246.173", 8080))
    return s

def upload_file(client_socket, file_path):
    """
    Send a file to the server over the provided socket.
    """
    filename = os.path.basename(file_path)
    filename_bytes = filename.encode()
    filename_len = len(filename_bytes)
    client_socket.send(filename_len.to_bytes(4, 'big'))
    client_socket.send(filename_bytes)

    with open(file_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                print("finish sending file")
                break
            print("sending 1024 bytes...")
            client_socket.send(data)
        client_socket.send(b"<<END_OF_FILE126234>>")

def connect_to_server():
    """
    Connect the client to the server and update UI accordingly.
    """
    global client_socket
    try:
        client_socket = create_client()
        result_label.config(text="✅ Connected to server")
        button_connect.config(state=DISABLED)
    except Exception as e:
        result_label.config(text=f"❌ Connection failed: {e}")

def download_file():
    """
    Request a specific file from the server and save it to the Downloads folder.
    """
    global server_listbox
    if client_socket is None:
        result_label.config(text="❌ Connect to server first!")
        return
   
    try: 
        new_path = os.path.join(downloads_path, fille_to_download)
        client_socket.send(b"<<Download file>>")
        time.sleep(0.5)
        filename_bytes = fille_to_download.encode()
        client_socket.send(len(filename_bytes).to_bytes(4, 'big'))
        client_socket.send(filename_bytes)
        buffer = client_socket.recv(1024)
        with open(new_path, "wb") as file:
            while True:
                if b"<<END_OF_FILE126234>>" in buffer:
                    content, _ = buffer.split(b"<<END_OF_FILE126234>>", 1)
                    file.write(content)
                    result_label.config(text="✅ File received and saved.")
                    break
                else:
                    file.write(buffer)
                    buffer = client_socket.recv(1024)
    except Exception as e:
        result_label.config(text=f"❌ Failed to download file from server: {e}")

def threaded_download_file():
    """
    Create a thread to download the selected file from the server.
    """
    global client_socket
    if client_socket is None:
        result_label.config(text="❌ Connect to server first!")
        return
    threading.Thread(target=download_file).start()



button_bg = "#3498db"
button_fg = "white"

button_connect = Button(
    text="Connect to Server", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg="#e74c3c", fg="white",
    relief="flat",
    activebackground="#a50e0e", activeforeground="white",
    command=connect_to_server
)

button_select = Button(
    text="Select file to upload", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg=button_bg, fg=button_fg, relief="flat",
    activebackground="#2980b9", activeforeground="white",
    command=get_file
)

button_download_select = Button(
    text="Select flie to download", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg=button_bg, fg=button_fg, relief="flat",
    activebackground="#2980b9", activeforeground="white",
    command=threaded_download_file
)

button_send = Button(
    text="Send File to Server", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg="#27ae60", fg="white", relief="flat",
    activebackground="#1e8449", activeforeground="white",
    command=threaded_send_file
)

button_get_file_list = Button(
    text="Get File List", width=20, height=2,
    font=("Arial", 16, "bold"),
    bg="#27ae60", fg="white", relief="flat",
    activebackground="#1e8449", activeforeground="white",
    command=threaded_request_file_list
)

result_label = Label(
    text="", font=("Arial", 14),
    bg="#2c3e50", fg="white", wraplength=700, justify="center"
)

# Layout all buttons
button_connect.place(relx=0.5, rely=0.25, anchor='center')
button_select.place(relx=0.5, rely=0.35, anchor='center')
button_send.place(relx=0.5, rely=0.45, anchor='center')
button_get_file_list.place(relx=0.5, rely=0.55, anchor='center')
button_download_select.place(relx=0.5, rely=0.65, anchor='center')
result_label.place(relx=0.5, rely=0.72, anchor='center')

if __name__ == "__main__":
    window.mainloop()
   # server_listbox.bind("<<ListboxSelect>>", on_listbox_select)

