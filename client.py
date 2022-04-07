import socket
import ssl
import json
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# HOST = "127.0.0.1"
HOST = "25.35.53.183"  # SERVER: Gabriele - Hamachi IPV4
PORT = 10035  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED,
                           ciphers="ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-256:HIGH:")

print("[CLIENT] Trying to connect to Server: ", HOST, " via SSL...")
try:
    ssl_sock.connect((HOST, PORT))
    data = ssl_sock.recv(1024)
    data = data.decode("utf-8")
    print(data)
except Exception as error:
    print(str(error))
    print("Can't create secure connection via SSL. The program will be terminated.")
    sys.exit(0)

username = input("Insert username:")  # str type
password = input("Insert password:")  # str type

data = {
        "username": username,
        "password": password}

serialized = json.dumps(data)

ssl_sock.write((bytes(serialized, "utf-8")))
authresponse = ssl_sock.recv(1024)
authresponse = authresponse.decode("utf-8")
print(authresponse)

while True:
    message = input("Insert message: ")
    message = message.encode("utf-8")
    ssl_sock.write(message)
    response = ssl_sock.recv(1024)
    response = response.decode("utf-8")
    print(response)

ssl_sock.close()

