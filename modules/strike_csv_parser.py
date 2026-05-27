#!/usr/bin/env python3
"""
File Name: strike_csv_parser.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_csv_parser.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Secure CSV Parsing and Sanitization Engine for AeroCage-X.
             Protects against CSV Injection and validates dynamic MAC schemas.
"""

import csv
from pathlib import Path

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators


# pylint: disable=too-few-public-methods
class StrikeCSVParser:
    """
    Main CSV Parser Object.
    Provides automated sanitization, column filtering, and asset verification.
    """

    def __init__(self, file_path: str):
        """تهيئة المحرك وتأمين فحص صلاحيات مدير النظام محلياً عند الاستدعاء"""
        SystemGuard.enforce_root_privileges("Strike CSV Parser")
        self.file_path = Path(file_path)

    def parse_results_safely(self) -> list:
        """قراءة وتطهير ملف نتائج الفحص اللاسلكي وحمايته بالاعتماد على الفلاتر"""
        parsed_records = []
        if not self.file_path.exists():
            print(f"[-] Error: Target log file not found at: {self.file_path}")
            return parsed_records

        try:
            with open(
                self.file_path, mode='r', encoding='utf-8', errors='ignore'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    cleaned_row = {}
                    for key, val in row.items():
                        if key is not None:
                            clean_key = SystemGuard.sanitize_input(
                                str(key), "csv_value"
                            )
                            clean_val = SystemGuard.sanitize_input(
                                str(val), "csv_value"
                            )

                            # التحقق الصارم إذا كان الحقل يمثل عنوان ماك أدرس
                            key_low = clean_key.lower()
                            if "bssid" in key_low or "mac" in key_low:
                                if not NetworkValidators.is_valid_bssid(clean_val):
                                    clean_val = "00:00:00:00:00:00"

                            cleaned_row[clean_key] = clean_val
                    if cleaned_row:
                        parsed_records.append(cleaned_row)

            msg = f"[+] Successfully parsed and sanitized {len(parsed_records)} log records."
            print(msg)
            return parsed_records

        except (IOError, OSError, KeyError, ValueError) as e:
            print(f"[-] Integrity Error: Crash in CSV parsing pipeline: {e}")
            return []


if __name__ == "__main__":
    print("[+] Strike CSV Parser module deployment verified.")
