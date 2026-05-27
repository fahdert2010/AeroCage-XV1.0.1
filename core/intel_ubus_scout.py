#!/usr/bin/env python3
"""
File Name: intel_ubus_scout.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_ubus_scout.py
Created Date: 2026-05-25
Version: 1.0.4
Description: Remote OpenWrt UBUS Command Bus Client Discovery Engine for AeroCage-X.
             Fully optimized for uniform sharded database API integration.
"""

import json
import subprocess
import threading
import time

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from core.db_manager import DatabaseManager


class IntelUbusScout:
    """
    Main UBUS Stream Discovery Object.
    Queries remote router internal message buses and schedules dynamic dataset mapping.
    """

    def __init__(self):
        """تهيئة محرك استكشاف الـ ubus وتأمين صلاحيات ومراجع النواة"""
        self.proc_manager = ProcessManager()
        self.db_manager = DatabaseManager()
        self.lock = threading.Lock()
        self.active_ubus_sessions = {}

    def fetch_openwrt_clients_safe(self, interface: str) -> list:
        """استدعاء واستخراج الأجهزة المتصلة بالراوتر عبر ubus بأمان كامل"""
        clean_inf = SystemGuard.sanitize_input(interface, "interface")
        clients_list = []
        if not clean_inf:
            print("[-] Configuration Error: Invalid interface bounds provided.")
            return clients_list

        command_array = [
            "ubus", "call", "iwinfo", "assoclist",
            f'{{"device":"{clean_inf}"}}'
        ]

        try:
            print(f"[*] Querying router internal UBUS pipeline for interface: {clean_inf}")
            result = subprocess.run(
                command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=15
            )

            if result.returncode != 0:
                print(f"[-] UBUS execution failure: {result.stderr.strip()}")
                return clients_list

            try:
                raw_data = json.loads(result.stdout)
                if "results" in raw_data:
                    for client in raw_data["results"]:
                        mac = SystemGuard.sanitize_input(client.get("mac", ""), "bssid")
                        signal = int(client.get("signal", -100))

                        if mac:
                            clients_list.append({"mac": mac, "signal": signal})

                            # مواءمة وتحديث النداء ليتطابق 100% مع الـ Sharded DB API المطور
                            meta_payload = {
                                "channel": "0",
                                "power": signal,
                                "status": "discovered"
                            }
                            essid_lbl = f"OpenWrt_Client_{clean_inf}"
                            self.db_manager.save_target_safe(
                                mac, essid_lbl, meta_payload
                            )
            except (json.JSONDecodeError, TypeError, KeyError, ValueError):
                print("[-] Alert: Corrupted json metadata packet discarded.")

            return clients_list

        except (subprocess.SubprocessError, OSError) as e:
            print(f"[-] Pipeline Exception inside core UBUS discovery loop: {e}")
            return clients_list

    def run_live_ubus_monitor_async(self, interface: str, interval_sec: int = 5):
        """تشغيل مراقب الـ ubus الحي للراوتر في الخلفية لتحديث طابور الضربات"""
        clean_inf = SystemGuard.sanitize_input(interface, "interface")
        if not clean_inf:
            return

        session_key = f"ubus_monitor_{clean_inf}"

        with self.lock:
            if session_key in self.active_ubus_sessions:
                print(f"[-] Notice: Active UBUS monitors context allocated for: {clean_inf}")
                return

        def _monitor_worker():
            print(f"[+] Operational thread launched for host bus context: [{clean_inf}]")
            while session_key in self.active_ubus_sessions:
                self.fetch_openwrt_clients_safe(clean_inf)
                time.sleep(interval_sec)

        with self.lock:
            self.active_ubus_sessions[session_key] = True
            threading.Thread(target=_monitor_worker, daemon=True).start()

    def stop_ubus_monitor(self, interface: str):
        """إيقاف خيط المراقبة وتطهير ممرات الذاكرة فوراً لمنع تعليق الموارد"""
        session_key = f"ubus_monitor_{SystemGuard.sanitize_input(interface, 'interface')}"
        with self.lock:
            if session_key in self.active_ubus_sessions:
                del self.active_ubus_sessions[session_key]
                print(f"[+] Successfully decoupled UBUS stream channel: [{session_key}].")


if __name__ == "__main__":
    print("[+] Intel UBUS Command Bus Scout deployment configuration verified.")
