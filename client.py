import socket

s = socket.socket()

port = 50001

s.connect(("192.168.2.6", port))

print (s.recv(1024).decode())

s.close()