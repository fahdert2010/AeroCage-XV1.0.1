#!/usr/bin/env python3
"""
File Name: strike_whitelist.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_whitelist.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Safe Whitelist Engine and Client Hardware Node Protector for AeroCage-X.
             Optimized via centralized shared utility toolkits wrappers.
"""

from pathlib import Path

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.network_validators import NetworkValidators
from utils.shared_utils_1 import SharedSecurityToolkit


class StrikeWhitelistEngine:
    """
    Main Whitelist Validation Engine.
    Handles persistent white-list configurations and automated client node exemption.
    """

    def __init__(self, whitelist_file: str = "whitelist.txt"):
        """💡 تهيئة محرك القائمة البيضاء الكائني وتأمين فحص صلاحيات النظام"""
        SystemGuard.enforce_root_privileges("Strike Whitelist Engine")

        self.db_manager = DatabaseManager()
        self.whitelist_path = Path(__file__).resolve().parent.parent / "data" / whitelist_file

        # حفظ كاش القائمة في الذاكرة الموحدة لمنع اختناق القراءة والكتابة للقرص
        self._cached_whitelist = set()

        self._ensure_whitelist_file_exists()
        self.load_clean_whitelist()

    def _ensure_whitelist_file_exists(self):
        """إنشاء ملف الاستثناءات تلقائياً إذا لم يكن موجوداً لمنع الانهيارات"""
        try:
            self.whitelist_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.whitelist_path.exists():
                with open(self.whitelist_path, "w", encoding="utf-8") as f:
                    f.write("# AeroCage-X | Whitelisted Assets Configuration File\n")
                    # كسر السطور الطويلة للامتثال لـ PEP 8 لـ Pylint
                    msg_txt = "# Write MAC Addresses line by line (Example: AA:BB:CC:DD:EE:FF)\n"
                    f.write(msg_txt)
                print(f"[+] Default whitelist initialized at: {self.whitelist_path}")
        except (IOError, OSError) as e:
            print(f"[-] System Exception initializing default configurations: {e}")

    def load_clean_whitelist(self) -> set:
        """قراءة وتطهير عناوين القائمة البيضاء وتخزينها بكفاءة في الذاكرة العشوائية"""
        whitelist_set = set()
        if not self.whitelist_path.exists():
            self._cached_whitelist = whitelist_set
            return whitelist_set

        try:
            with open(self.whitelist_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith("#"):
                        continue

                    if NetworkValidators.is_valid_bssid(clean_line):
                        # الاعتماد الحصري والصافي على ممر حقيبة الخدمات المشتركة 1 لاختزال التضخم
                        clean_mac = SharedSecurityToolkit.sanitize_input(clean_line, "bssid")
                        whitelist_set.add(clean_mac.upper())

            self._cached_whitelist = whitelist_set
            msg = f"[+] Loaded {len(self._cached_whitelist)} whitelisted nodes in RAM buffer."
            print(msg)
            return self._cached_whitelist
        except (IOError, OSError, ValueError) as e:
            print(f"[-] Integrity Exception during configuration processing: {e}")
            self._cached_whitelist = whitelist_set
            return whitelist_set

    def is_target_whitelisted(self, target_bssid: str) -> bool:
        """فحص فوري سريع ومعزول القراءة للتحقق من سلامة البصمة الفيزيائية للهدف"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid").upper()
        if not NetworkValidators.is_valid_bssid(clean_mac):
            return False

        return clean_mac in self._cached_whitelist

    def enforce_whitelist_on_targets(self, raw_targets_list: list) -> list:
        """غربلة الأهداف المستخلصة وحظر تمرير الأصول المحمية في طابور العمليات"""
        sanitized_targets = []
        purged_count = 0

        for target in raw_targets_list:
            bssid = SharedSecurityToolkit.sanitize_input(target.get("bssid", ""), "bssid").upper()

            if bssid in self._cached_whitelist:
                purged_count += 1
                continue

            sanitized_targets.append(target)

        if purged_count > 0:
            print(f"[🛡️] System Guard Alert: Intercepted and protected {purged_count} assets.")
        return sanitized_targets


if __name__ == "__main__":
    print("[+] Strike Whitelist Engine module deployment configuration verified.")
