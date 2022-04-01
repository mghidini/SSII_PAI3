import socket, ssl

bindsocket = socket.socket()
bindsocket.bind(('localhost', 10035))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")
    print("Recibido del cliente: ", connstream.read())
    connstream.shutdown(socket.SHUT_RDWR)
    connstream.close()
