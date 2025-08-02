import socket
import os

def create_server():
    """
    Create a TCP server socket that listens on all interfaces (0.0.0.0) and port 8080.
    Returns the server socket object.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8080))
    server_socket.listen(5)
    print("📡 Listening for new connections...")
    return server_socket

def accept_client(server_socket):
    """
    Accept a new client connection on the server socket.
    Returns the client socket object.
    """
    client_socket, client_address = server_socket.accept()
    print(f"🔌 Connection established with {client_address}")
    return client_socket

def upload_file_list(client_socket):
    """
    Send a list of files available in the server folder to the client.
    The list is sent as a UTF-8 encoded string with '::' separating filenames.
    """
    folder_path = r"C:\Users\User\Desktop\pythonProj\dev_academy642\server_folder"
    os.makedirs(folder_path, exist_ok=True)2
    files = os.listdir(folder_path)
    file_list_str = "::".join(files)
    encoded = file_list_str.encode()

    try:
        client_socket.send(len(encoded).to_bytes(4, 'big'))  # Send length
        client_socket.sendall(encoded)  # Then send data
        print("✅ Sent file list to client.")
    except Exception as e:
        print("❌ Error sending file list:", e)

def receive_file(client_socket, first_chunk):
    """
    Receive a file sent by the client.
    The file starts with a 4-byte length for the filename, then the filename, then the file content.
    Ends when the <<END_OF_FILE126234>> marker is received.
    """
    folder_path = r"C:\Users\User\Desktop\pythonProj\dev_academy642\server_folder"
    os.makedirs(folder_path, exist_ok=True)

    buffer = first_chunk

    if len(buffer) < 4:
        print("❌ Invalid header.")
        return

    filename_len = int.from_bytes(buffer[:4], 'big')

    while len(buffer) < 4 + filename_len:
        buffer += client_socket.recv(1024)

    filename = buffer[4:4 + filename_len].decode()
    file_path = os.path.join(folder_path, filename)
    print(f"📥 Writing to: {file_path}")

    buffer = buffer[4 + filename_len:]

    try:
        with open(file_path, "wb") as file:
            while True:
                if b"<<END_OF_FILE126234>>" in buffer:
                    content, _ = buffer.split(b"<<END_OF_FILE126234>>", 1)
                    file.write(content)
                    print("✅ File received and saved.")
                    break
                else:
                    file.write(buffer)
                    buffer = client_socket.recv(1024)
    except Exception as e:
        print("❌ Error writing file:", e)

def upload_file_to_client(client_socket, filename):
    """
    Send a file from the server folder to the client.
    The file is sent in chunks of 1024 bytes, ending with the marker <<END_OF_FILE126234>>.
    """
    folder_path = os.path.join(r"C:\Users\User\Desktop\pythonProj\dev_academy642\server_folder", filename)

    with open(folder_path, "rb") as file:
        while True:
            data = file.read(1024)
            if not data:
                print("finish sending file")
                break
            print("sending 1024 bytes...")
            client_socket.send(data)
        client_socket.send(b"<<END_OF_FILE126234>>")

def handle_client(client_socket):
    """
    Handle communication with a connected client.
    Supports file list request, file upload, and file download.
    """
    print("🧵 Started thread for new client.")
    while True:
        try:
            buffer = client_socket.recv(1024)
            if not buffer:
                print("❌ Client disconnected.")
                break

            if buffer.startswith(b"<<GET_FILE_LIST>>"):
                upload_file_list(client_socket)

            elif buffer.startswith(b"<<Download file>>"):
                filename_len_bytes = client_socket.recv(4)
                filename_len = int.from_bytes(filename_len_bytes, 'big')
                filename_bytes = client_socket.recv(filename_len)
                filename = filename_bytes.decode()
                upload_file_to_client(client_socket, filename)
            
            else:
                receive_file(client_socket, buffer)

        except Exception as e:
            print(f"❌ Error handling client: {e}")
            break

if __name__ == "__main__":
    """
    Main server loop: starts the server and continuously accepts and handles clients.
    """
    server_sock = create_server()
    while True:
        client_sock = accept_client(server_sock)
        handle_client(client_sock)
