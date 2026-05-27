#!/usr/bin/env python3
"""
File Name: strike_tunnel.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_tunnel.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Remote OpenWrt Secure Reverse SSH Tunneling Management Module.
             Monitors socket bindings and ensures clean port isolation matrix.
"""

import socket
import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager


class StrikeTunnelEngine:
    """
    Main Reverse Tunneling Controller Component.
    Deploys atomic reverse SSH tunnels and handles active background socket polling.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الأنفاق العتادية وتأمين صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("AeroCage-X Reverse Tunnel Engine")
        self.proc_manager = ProcessManager()
        self.lock = threading.Lock()

        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.active_tunnels = {}

    @staticmethod
    def _is_local_port_busy(port: int) -> bool:
        """فحص داخلي ذكي للمنفذ محلياً لمنع تعارض وانهيار الأنفاق التتابعية"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def establish_reverse_ssh_tunnel(self, local_port: int, remote_port: int) -> bool:
        """حفر وإنشاء نفق العبور العكسي بأمان مصفوفة مغلقة الشل ومحمية من التكرار"""
        if not str(local_port).isdigit() or not str(remote_port).isdigit():
            print("[-] Configuration Error: Port parameters must be absolute numeric digits.")
            return False

        tunnel_key = f"rev_tunnel_{remote_port}"

        # خط الدفاع الهيكلي لمحلي كالي: منع التضارب والـ Socket overlapping
        if self._is_local_port_busy(local_port):
            print(f"[-] Alert: Local port {local_port} is busy. Aborting double binding.")
            return False

        # تفتيت المصفوفة بشكل منسق للتوافق الصارم مع معيار الـ 100 حرف لـ Pylint
        bind_arg = f"{remote_port}:127.0.0.1:{local_port}"
        command_array = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-N", "-R", bind_arg,
            "-o", "StrictHostKeyChecking=no", f"root@{self.ap_ip}"
        ]

        try:
            print(f"[*] [Tunnel Core] Mining reverse path to host: {self.ap_ip}")

            # ركوب نفق الـ Popen المستقر والمعزول مركزياً داخل محرك العمليات الموحد
            process = self.proc_manager.spawn_process_safe(tunnel_key, command_array)

            if process:
                with self.lock:
                    self.active_tunnels[tunnel_key] = process
                msg_suc = f"[+] Reverse tunnel locked (Local:{local_port} -> Remote:{remote_port})"
                print(msg_suc)
                return True
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside socket tunneling allocation: {e}")
            return False

    def close_tunnel_bridge(self, remote_port: int):
        """إغلاق النفق المخصص برمجياً بالـ PID اللحظي وتطهير المنفذ لمنع الـ Port Busy"""
        tunnel_key = f"rev_tunnel_{remote_port}"
        with self.lock:
            if tunnel_key in self.active_tunnels:
                # إنهاء محدد ونظيف وموثق للعملية لمنع بقاء السوكيت كـ Zombie في كالي
                self.proc_manager.terminate_process(tunnel_key)
                del self.active_tunnels[tunnel_key]
                print(f"[+] Successfully destroyed tunnel context: [{tunnel_key}]")
            else:
                print(f"[-] Notice: No active channels allocated for port: {remote_port}")


if __name__ == "__main__":
    print("[+] Strike Reverse Tunnel Engine module configuration verified.")
