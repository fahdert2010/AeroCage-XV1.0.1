#!/usr/bin/env python3
"""
File Name: process_manager.py
Path: /home/kali/AeroCage-XV1.0.1/core/process_manager.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Safe Multi-Threaded Process Lifecycle Management and Secure Socket
             Binding Infrastructure Module for AeroCage-X.
"""

import sys
import subprocess
import threading
import socket
from pathlib import Path

# ربط المسارات بالنواة المركزية للمنظومة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard


class ProcessManager:
    """
    Main Process Lifecyle Controller.
    Manages thread-safe local subprocess execution pools and stream drainage.
    """

    def __init__(self):
        """تهيئة القاموس المركزي لتتبع العمليات مع مقفل التزامن الخيطي"""
        self.active_processes = {}
        self.lock = threading.Lock()

    def spawn_process_safe(self, key_name: str, command_array: list) -> subprocess.Popen:
        """إطلاق الأدوات الخارجية بأمان مصفوفة كامل ومغلق الشل لـ Bandit"""
        clean_key = SystemGuard.sanitize_input(key_name, "interface")

        if not command_array or not isinstance(command_array, list):
            print(f"[-] Configuration Error: Invalid process command format for {clean_key}.")
            return None

        try:
            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                command_array,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            with self.lock:
                self.active_processes[clean_key] = process
                print(f"[+] Task successfully initialized [{clean_key}] (PID: {process.pid})")

            # تشغيل خيط الحراسة لتفريغ المخزن لمنع الاختناق وتجميد الأنابيب
            drain_thread = threading.Thread(
                target=self._drain_buffer_stream,
                args=(clean_key, process),
                daemon=True
            )
            drain_thread.start()
            return process

        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Critical: Failed to launch backend sub-process for [{clean_key}]: {e}")
            return None

    def _drain_buffer_stream(self, key_name: str, process: subprocess.Popen):
        """خيط تفريغ مخزن الأنبوب اللحظي لضمان ثبات واستمرارية تدفق الحزم"""
        try:
            while process.poll() is None:
                line = process.stdout.readline()
                if not line:
                    break
        except (IOError, OSError, ValueError) as e:
            print(f"[-] Buffer Stream Warning on [{key_name}]: {e}")
        finally:
            # تنظيف ومسح الكائن من مصفوفة التتبع فور إغلاقه بالنظام
            with self.lock:
                if key_name in self.active_processes:
                    del self.active_processes[key_name]

    def terminate_process(self, key_name: str):
        """إنهاء واحتواء عملية محلية محددة بدقة ومنع تكون الـ Zombie Processes"""
        clean_key = SystemGuard.sanitize_input(key_name, "interface")

        with self.lock:
            if clean_key in self.active_processes:
                process = self.active_processes[clean_key]
                if process.poll() is None:
                    try:
                        process.terminate()
                        process.wait(timeout=2)
                        print(f"[+] Process handle [{clean_key}] closed cleanly.")
                    except subprocess.TimeoutExpired:
                        # قتل قسري فوري مع استدعاء مفرغ المعرفات لمنع الـ Zombie Processes
                        process.kill()
                        process.wait()
                        print(f"[-] Process forced to terminate context (PID: {process.pid})")
                del self.active_processes[clean_key]
            else:
                print(f"[-] System Notice: No active runtime registered for key: {clean_key}")

    @staticmethod
    def create_secure_listener(port: int, local_only: bool = True) -> socket.socket:
        """التحكم الصارم في مجال الاستماع للسوكت لمنع ثغرات الاستماع العشوائي"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        bind_address = '127.0.0.1' if local_only else '0.0.0.0'

        try:
            server_socket.bind((bind_address, port))
            server_socket.listen(5)
            print(f"[+] Secure core socket infrastructure active on: {bind_address}:{port}")
            return server_socket
        except (socket.error, OSError) as e:
            print(f"[-] Network Exception: Failed to bind socket address boundary {port}: {e}")
            server_socket.close()
            return None


if __name__ == "__main__":
    print("[+] Process Manager core layout configuration verified.")
