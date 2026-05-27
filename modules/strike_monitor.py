#!/usr/bin/env python3
"""
File Name: strike_monitor.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_monitor.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Remote OpenWrt Dual Monitor Channels Management and Traffic Quality 
             Assurance Watchdog Engine for AeroCage-X. Fully integrated with toolkits.
"""

import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.shared_utils_1 import SharedSecurityToolkit


class StrikeMonitorEngine:
    """
    Main Remote Monitor Interface Controller.
    Manages active wireless tracking cells and captures quality control telemetries.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الرقابة العكسية وتأمين صلاحيات مدير النظام محلياً عبر النواة"""
        SystemGuard.enforce_root_privileges("Strike Monitor Remote OpenWrt Engine")

        self.proc_manager = ProcessManager()
        self.lock = threading.Lock()

        self.ap_ip = SharedSecurityToolkit.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.ssh_factory = OpWrtSSHFactory(ip=self.ap_ip, password=self.ap_password)

        # تخزن أسماء القنوات المزدوجة المنشأة داخل الراوتر
        self.remote_monitor_interfaces = []

    def setup_remote_dual_monitor_channels(self, ap_iface1: str, ap_iface2: str) -> bool:
        """إنشاء واجهتي مراقبة والتحقق الجراحي من نجاح العملية عتادياً بالراوتر"""
        clean_if1 = SharedSecurityToolkit.sanitize_input(ap_iface1, "interface")
        clean_if2 = SharedSecurityToolkit.sanitize_input(ap_iface2, "interface")

        if not clean_if1 or not clean_if2 or clean_if1 == clean_if2:
            print("[-] Configuration Error: Invalid or redundant interfaces provided.")
            return False

        print(f"[*] Provisioning dual monitoring channels inside target host: {self.ap_ip}")

        # تفتيت كتل نصوص الـ uci والـ iw وتوزيعها على أسطر قصيرة متوافقة 100% مع معايير PEP 8
        cmd_1 = (
            f"iw dev {clean_if1} interface add {clean_if1}mon type monitor && "
            f"ifconfig {clean_if1}mon up"
        )
        cmd_2 = (
            f"iw dev {clean_if2} interface add {clean_if2}mon type monitor && "
            f"ifconfig {clean_if2}mon up"
        )
        verify_cmd = f"iw dev {clean_if1}mon info && iw dev {clean_if2}mon info"

        try:
            self.ssh_factory.execute_remote_cmd(cmd_1)
            self.ssh_factory.execute_remote_cmd(cmd_2)

            check_stdout = self.ssh_factory.execute_remote_cmd(verify_cmd)

            if check_stdout and "type monitor" in check_stdout.lower():
                with self.lock:
                    self.remote_monitor_interfaces = [f"{clean_if1}mon", f"{clean_if2}mon"]
                msg_suc = f"[+] Remote validation success! Active: {self.remote_monitor_interfaces}"
                print(msg_suc)
                return True

            print("[-] Hardware Exception: OpenWrt host environment rejected monitor creation.")
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside remote environment provision: {e}")
            return False

    def start_remote_strike_monitoring_async(self, target_mac: str) -> bool:
        """إطلق مراقبة جودة الضربات حياً من داخل الراوتر دون حظر نظام كالي"""
        with self.lock:
            if len(self.remote_monitor_interfaces) < 2:
                print("[-] Error: Dual monitoring infrastructure has not been deployed yet.")
                return False
            # قنص العنصر النصي الأول حركياً لمنع تمرير كائن الـ List لـ tcpdump
            intel_iface = self.remote_monitor_interfaces[0]

        clean_target = SharedSecurityToolkit.sanitize_input(target_mac, "bssid")
        session_key = f"remote_mon_{clean_target}"

        remote_mon_cmd = f"tcpdump -i {intel_iface} -n 'wlan == 0xc0 and wlan addr1 {clean_target}'"

        full_command_array = self.ssh_factory.base_args + [remote_mon_cmd]

        try:
            print(f"[📡 Remote Monitor] Streaming runtime frame metrics for node: {clean_target}")
            self.proc_manager.spawn_process_safe(session_key, full_command_array)
            return True
        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Stalled socket listener within channel context: {e}")
            return False

    def stop_remote_monitoring(self, target_mac: str):
        """قطع جلسة المراقبة البعيدة وتطهير الذاكرة لمنع العمليات المعلقة Zombie Processes"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_mac, "bssid")
        session_key = f"remote_mon_{clean_mac}"

        self.ssh_factory.execute_remote_cmd("killall tcpdump")

        self.proc_manager.terminate_process(session_key)
        print(f"[+] Successfully unmapped and flushed monitoring pipelines for: [{clean_mac}]")


if __name__ == "__main__":
    print("[+] Strike Watchdog Monitor Engine module configuration verified.")
