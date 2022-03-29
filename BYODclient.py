# clientsocket.py
import json
import socket
import time
import datetime
import ssl

HOST = "127.0.0.1"
# HOST = "25.35.53.183"  # SERVER: Gabriele - Hamachi IPV4
PORT = 3030  # The port used by the server

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.verify_mode = ssl.CERT_REQUIRED

# Load CA certificate with which the client will validate the server certificate
context.load_verify_locations("./CA.pem")

# Load client certificate
context.load_cert_chain("./certif.crt", "./keys.key")

# Create a client socket
clientSocket = socket.socket()

# Make the client socket suitable for secure communication
secureClientSocket = context.wrap_socket(clientSocket)
secureClientSocket.connect((HOST, PORT))

# Obtain the certificate from the server
server_cert = secureClientSocket.getpeercert()

# Validate whether the Certificate is indeed issued to the server
subject = dict(item[0] for item in server_cert['subject'])
commonName = subject['commonName']

if not server_cert:
    raise Exception("Unable to retrieve server certificate")

if commonName != 'DemoSvr':
    raise Exception("Incorrect common name in server certificate")

notAfterTimestamp = ssl.cert_time_to_seconds(server_cert['notAfter'])
notBeforeTimestamp = ssl.cert_time_to_seconds(server_cert['notBefore'])
currentTimeStamp = time.time()

if currentTimeStamp > notAfterTimestamp:
    raise Exception("Expired server certificate")

if currentTimeStamp < notBeforeTimestamp:
    raise Exception("Server certificate not yet active")

# Safe to proceed with the communication
msgReceived = secureClientSocket.recv(1024)
print("Secure communication received from server:%s" % msgReceived.decode())

# Close the sockets
secureClientSocket.close()
clientSocket.close()