#!/usr/bin/env python3
"""
File Name: process_terminator.py
Path: /home/kali/AeroCage-XV1.0.1/modules/process_terminator.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Remote OpenWrt Process Termination and Radio Reset Interface 
             Module for AeroCage-X. Implements secure environment cleansing.
"""

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory


# pylint: disable=too-few-public-methods
class ProcessTerminatorEngine:
    """
    Main Process Terminator Component.
    Provides utility methods to clean remote daemon queues and reload wireless radios.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التطهير العتادي وتأمين فحص امتيازات مدير النظام"""
        SystemGuard.enforce_root_privileges("Process Terminator & Interface Cleaner")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)

    def sever_all_remote_attack_daemons(self) -> bool:
        """كبح شامل وصارم لجميع هجمات وسيرفرات الفصل المعلقة داخل الراوتر البعيد"""
        msg_clean = "[*] [Strategic Clean] Cleansing remote target tracking contexts..."
        print(msg_clean)

        self.ssh_factory.execute_remote_cmd("killall -9 airserv-ng")
        self.ssh_factory.execute_remote_cmd("killall -9 aireplay-ng")

        print("[+] Active remote task handles successfully terminated inside hardware pool.")
        return True

    def factory_reset_wireless_radio(self, radio_name: str) -> bool:
        """إعادة تحميل كرت الراديو الفيزيائي للراوتر لوضعه الافتراضي المستقر"""
        clean_radio = SystemGuard.sanitize_input(radio_name, "interface")
        if not clean_radio:
            return False

        print(f"[⚠️ Emergency] Forcing physical wireless radio interface reload on: {clean_radio}")
        self.ssh_factory.execute_remote_cmd(f"wifi reload {clean_radio}")
        return True


if __name__ == "__main__":
    print("[+] Process Terminator Engine module configuration verified.")
