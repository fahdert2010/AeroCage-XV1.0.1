#!/usr/bin/env python3
"""
File Name: radar_historian.py
Path: /home/kali/AeroCage-XV1.0.1/modules/radar_historian.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Tactical Airspace Radar Historian Tracking Engine for AeroCage-X.
             Manages real-time safe dynamic target telemetry logging buffers.
"""

import threading

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.network_validators import NetworkValidators


class RadarHistorianEngine:
    """
    Main Space Radar Auditor Component.
    Examines runtime client association movements and updates persistent vaults.
    """

    def __init__(self):
        """تهيئة محرك مؤرخ الرادار وتأمين فحص صلاحيات النظام عن بعد"""
        SystemGuard.enforce_root_privileges("Radar Historian Engine")
        self.db_manager = DatabaseManager()
        self.lock = threading.Lock()
        self.historical_movements = {}

    def log_target_movement_safe(
        self, client_mac: str, associated_bssid: str, essid_name: str
    ) -> bool:
        """توثيق وأرشفة حركة وتنقل الأهداف بين الشبكات في الذاكرة والكاش والـ DB"""
        clean_client = SystemGuard.sanitize_input(client_mac, "bssid").upper()
        clean_ap = SystemGuard.sanitize_input(associated_bssid, "bssid").upper()
        clean_essid = SystemGuard.sanitize_input(essid_name, "csv_value")

        is_client_valid = NetworkValidators.is_valid_bssid(clean_client)
        is_ap_valid = NetworkValidators.is_valid_bssid(clean_ap)

        if not is_client_valid or not is_ap_valid:
            return False

        # البحث السريع O(1) في الكاش المحلي لحظر الفتح التكراري
        target_key = f"{clean_client}_current"
        with self.lock:
            if self.historical_movements.get(target_key) == clean_ap:
                return True
            self.historical_movements[target_key] = clean_ap

        # تمرير السجلات المصفاة عتادياً ومباشرة للـ Public API السيادي للنواة
        success = self.db_manager.save_radar_movement_safe(
            clean_client, clean_ap, clean_essid
        )
        if success:
            print(f"[📡 RADAR] Logged shift vector for [{clean_client}] towards AP: {clean_essid}")
            return True
        return False

    def track_client_historical_path(self, client_mac: str) -> list:
        """استدعاء خريطة السير التاريخية وجدول القفزات لهدف هارب بأمان كامل"""
        clean_client = SystemGuard.sanitize_input(client_mac, "bssid").upper()
        return self.db_manager.fetch_client_radar_path(clean_client)


if __name__ == "__main__":
    print("[+] Radar Historian Engine module configuration verified.")
