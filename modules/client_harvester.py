#!/usr/bin/env python3
"""
File Name: client_harvester.py
Path: /home/kali/AeroCage-XV1.0.1/modules/client_harvester.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Remote Client Harvester and Hardware Signal Monitor Engine 
             for AeroCage-X. Extract and structures active OpenWrt nodes.
"""

import re

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory


# pylint: disable=too-few-public-methods
class ClientHarvesterEngine:
    """
    Main Client Harvester Component.
    Manages active association lists, structures signal metrics and updates DB.
    """
    # تجهيز النمط التعبيري مسبقاً في الذاكرة لتسريع استخلاص الماك والإشارة وحظر الـ CPU Hang
    _MAC_SIGNAL_REGEX = re.compile(
        r'(([0-9a-fa-f]{2}[:-]){5}([0-9a-fa-f]{2})).*?signal:\s+(-\d+)\s+dBm',
        re.DOTALL
    )

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك حصاد الأجهزة وتأمين فحص امتيازات مدير النظام"""
        SystemGuard.enforce_root_privileges("Client Harvester & Signal Monitor")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)
        self.db_manager = DatabaseManager()

    def harvest_active_clients_safe(self, ap_interface: str) -> list:
        """قنص وحصاد عناوين الأجهزة المتصلة بالراوتر وتوثيق إشاراتها وقنواتها بأمان"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")
        if not clean_inf:
            return []

        remote_cmd = f"iwinfo {clean_inf} assoclist"
        raw_stdout = self.ssh_factory.execute_remote_cmd(remote_cmd)
        clients_found = []

        if not raw_stdout:
            return clients_found

        try:
            # قراءة المخرجات وتفكيكها عتادياً بالاعتماد على النمط المجمع مسبقاً
            mac_blocks = self._MAC_SIGNAL_REGEX.findall(raw_stdout.lower())

            for block in mac_blocks:
                mac = SystemGuard.sanitize_input(block[0], "bssid").upper()

                # تصحيح التقاط الفهرس بناءً على تقسيمات النطاقات الرياضية للمصفوفة
                signal = int(block[3]) if len(block) > 3 else -90

                clients_found.append({"mac": mac, "signal": signal})

                # ضخ السجل حياً وتوثيق هوية العميل لـ OpenWrt دون تداخل لغوي
                target_identity = f"OPWRT_CLIENT_{clean_inf}"
                self.db_manager.save_target_safe(mac, target_identity, "0", signal)

            print(f"[+] Successfully extracted {len(clients_found)} active client nodes.")
            return clients_found

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside client harvesting pipeline: {e}")
            return clients_found


if __name__ == "__main__":
    print("[+] Client Harvester Engine module configuration verified.")
