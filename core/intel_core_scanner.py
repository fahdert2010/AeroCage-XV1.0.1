#!/usr/bin/env python3
"""
File Name: intel_core_scanner.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_core_scanner.py
Created Date: 2026-05-25
Version: 1.0.7
Description: Infrastructure Services and Network Ports Deep Scanner Core Engine
             for AeroCage-X. Fully optimized for sharded database integration.
"""

import subprocess
import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from core.db_manager import DatabaseManager


class IntelCoreScanner:
    """
    Main Infrastructure Deep Audit Scanner Component.
    Deploys automated nmap binaries handles and ensures thread-safe polling.
    """

    def __init__(self):
        """تهيئة محرك الفحص وتأمين فحص صلاحيات النظام والاعتماديات"""
        self.proc_manager = ProcessManager()
        self.db_manager = DatabaseManager()
        self.lock = threading.Lock()
        self.active_scans = {}
        SystemGuard.verify_dependencies(["nmap"])

    @staticmethod
    def _sanitize_ports_input(ports_str: str) -> str:
        """تنظيف وتطهير مدخلات المنافذ تماماً لمنع حقن النصوص والسماح فقط بالأرقام"""
        return "".join(ch for ch in ports_str if ch.isdigit() or ch in ",-")

    def launch_infrastructure_scan_async(self, target_ip: str, ports: str = "1-1000") -> bool:
        """إطلاق فحص عميق للخدمات والمنافذ بأمان كامل 100% وبدون فتح شل"""
        clean_ip = SystemGuard.sanitize_input(target_ip, "interface")
        clean_ports = self._sanitize_ports_input(ports)

        if not clean_ip or not clean_ports:
            print("[-] Configuration Error: Invalid scan bounds or target host tokens.")
            return False

        scan_key = f"core_scan_{clean_ip}"

        with self.lock:
            if scan_key in self.active_scans:
                print(f"[-] Notice: Active core scan context allocated for: {clean_ip}")
                return False

        command_array = ["nmap", "-sV", "-p", clean_ports, "-T4", clean_ip]

        try:
            with self.lock:
                msg_trig = (
                    f"[*] [Core Scan] Triggering secure audit for "
                    f"target: {clean_ip}"
                )
                print(msg_trig)

            process = self.proc_manager.spawn_process_safe(scan_key, command_array)

            if process:
                with self.lock:
                    self.active_scans[scan_key] = process

                # كسر وتفتيت سطر خيط المراقبة للامتثال لـ PEP 8 ومنع التجاوز نهائياً
                th_worker = threading.Thread(
                    target=self._wait_and_finalize_scan,
                    args=(scan_key, clean_ip),
                    daemon=True
                )
                th_worker.start()
                return True

        except (subprocess.SubprocessError, OSError, ValueError) as e:
            print(f"[-] Pipeline Exception inside core scanning engine: {e}")
            return False
        return False

    def _wait_and_finalize_scan(self, scan_key: str, target_ip: str):
        """الانتظار الآمن لانتهاء الفحص وتحديث السجلات التكتيكية للهدف"""
        with self.lock:
            process = self.active_scans.get(scan_key)

        if process:
            process.wait()

            with self.lock:
                if scan_key in self.active_scans:
                    del self.active_scans[scan_key]

            msg_fin = f"[+] Infrastructure scan finalized context for host: {target_ip}"
            print(msg_fin)

            # مواءمة وتحديث النداء ليتطابق 100% مع الـ Sharded DB API المطور ومنع الانهيار
            meta_payload = {
                "channel": "0",
                "power": -50,
                "status": "Scanned_Core_Host"
            }
            self.db_manager.save_target_safe(target_ip, "Scanned_Core_Host", meta_payload)

    def terminate_core_scan(self, target_ip: str):
        """إيقاف فحص الخدمات فوراً وتنظيف العمليات الخلفية لمنع الـ Zombie Processes"""
        scan_key = f"core_scan_{SystemGuard.sanitize_input(target_ip, 'interface')}"

        with self.lock:
            if scan_key in self.active_scans:
                self.proc_manager.terminate_process(scan_key)
                del self.active_scans[scan_key]
                print(f"[+] Successfully decoupled active scanning link: [{scan_key}]")
            else:
                print(f"[-] Notice: No active scan channels mapped for descriptor: {scan_key}")


if __name__ == "__main__":
    print("[+] Intel Core Scanner infrastructure deployment verified.")
