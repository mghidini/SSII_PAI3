import socket
import ssl
import json
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# HOST = "127.0.0.1"
HOST = "25.35.53.183"  # SERVER: Gabriele - Hamachi IPV4
PORT = 10035  # The port used by the server

username = input("Insert username:")  # str type
password = input("Insert password:")  # str type

data = {
    "username": username,
    "password": password}

serialized = json.dumps(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED,
                           ciphers="ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-256:HIGH:")
ssl_sock.connect((HOST, PORT))


ssl_sock.write((bytes(serialized, "utf-8")))
data = ssl_sock.recv(1024)
print(str(data))
#while True:
ssl_sock.close()
