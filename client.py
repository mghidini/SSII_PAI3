import socket,ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ssl_sock = ssl.wrap_socket(s,	
			   ca_certs = "server.crt",
			   cert_reqs = ssl.CERT_REQUIRED,
			   ciphers = "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:AES128-GCM-SHA256:AES128-256:HIGH:")
ssl_socket.connect(('localhost', 10035))

while True:
	mensaje = raw_input("Mensaje a enviar:")
	ssl_sock.write(mensaje)
	ssl_sock.close()
