import socket, ssl, json
import sqlite3

bindsocket = socket.socket()
bindsocket.bind(('25.35.53.183', 10035))
currentDb ="database.db"
connection =""
user_search = """SELECT username,password FROM User WHERE username=? AND password=?"""
bindsocket.listen(5)
connection = sqlite3.connect(currentDb, check_same_thread=False)


print(" [SERVER] - Server started. Listening for clients...")
while True:
    curs = connection.cursor()
    newsocket, fromaddr = bindsocket.accept()
    connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile="server.crt",
                                 keyfile="server.key",
                                 ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-SHA256:HIGH:")
    print(" [SERVER] - Estabilished secure connection with trusted client. Awaiting authetication.")
    connstream.sendall(b">[SERVER] Your certificate has been validated. Pending client authentication.")
    data = connstream.recv(1024)
    print(" [SERVER] - Received authetincation credentials... Verifying database")
    message = json.loads(data)
    tupla_name = (message['username'], message['password'])
    curs.execute(user_search, tupla_name)
    rows = curs.fetchall()
    if not bool(rows):
        connstream.sendall(b"[SERVER] Failed user authentication. Aborting connection now.")
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
        break
    connstream.sendall(b"[SERVER] User logged in successfully. Welcome!")
    data = connstream.recv(1024)
    data = data.decode("utf-8")
    if data:
        print("pieno")
    else:
        print("vuoto")


