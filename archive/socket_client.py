import socket


TCP_IP = 'rs485tester'
TCP_PORT = 56789
BUFFER_SIZE = 1024
MESSAGE = b'Hello World'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print("received data: {}", data)
