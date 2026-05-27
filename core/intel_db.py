#!/usr/bin/env python3
"""
File Name: intel_db.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_db.py
Created Date: 2026-05-25
Version: 1.0.4
Description: Advanced Targets Encryption Metrics Intelligence Facade Interface 
             for AeroCage-X. Inherits cleanly structuralized database components.
"""

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager


class IntelDatabase(DatabaseManager):
    """
    Main Intelligence Storage Facade.
    Provides decoupled secure interfaces to archive discovered deep networks metrics.
    """

    def update_intel_recon_safe(self, bssid: str, essid: str, intel_data: dict) -> bool:
        """تحديث مستودع الاستخبارات اللاسلكية ببيانات الأهداف بسلامة سيبرانية"""
        clean_bssid = SystemGuard.sanitize_input(bssid, "bssid").upper()
        clean_essid = SystemGuard.sanitize_input(essid, "csv_value")

        # تفتيت كتل القاموس الصارم لتتطابق 100% مع حدود الـ 100 حرف لـ PEP 8
        sanitized_data = {
            "encryption_type": SystemGuard.sanitize_input(
                intel_data.get("encryption_type", "OPEN"), "interface"
            ),
            "cipher": SystemGuard.sanitize_input(
                intel_data.get("cipher", "NONE"), "interface"
            ),
            "auth_type": SystemGuard.sanitize_input(
                intel_data.get("auth_type", "NONE"), "interface"
            ),
            "recon_notes": SystemGuard.sanitize_input(
                intel_data.get("recon_notes", ""), "csv_value"
            )
        }

        return super().update_intel_recon_safe(
            clean_bssid, clean_essid, sanitized_data
        )

    def query_target_recon_data(self, bssid: str) -> dict:
        """استدعاء السجل الاستخباراتي الكامل لهدف معين بأمان وحصانة"""
        clean_mac = SystemGuard.sanitize_input(bssid, "bssid").upper()
        return super().query_target_recon_data(clean_mac)


if __name__ == "__main__":
    print("[+] Wireless Targets Intel Database Engine facade verified.")
