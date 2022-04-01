import socket, ssl, json

bindsocket = socket.socket()
bindsocket.bind(('25.35.53.183', 10035))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")
    data = connstream.recv(1024)
    message = json.loads(data)
    print("Recibido del cliente: ", message)
    connstream.sendall(b"Ricevuto!")
connstream.shutdown(socket.SHUT_RDWR)
connstream.close()
