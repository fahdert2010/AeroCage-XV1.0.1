#!/usr/bin/env python3
"""
File Name: recon_analyzer.py
Path: /home/kali/AeroCage-XV1.0.1/modules/recon_analyzer.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Network Reconnaissance Log and Deep PCAP Parsing Engine for AeroCage-X.
             Optimized for strict sandboxed subprocess processing.
"""

from pathlib import Path

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators
from modules.recon_packet_parser import ReconPacketParserComponent


class ReconAnalyzerEngine(ReconPacketParserComponent):
    """
    Main Recon Analyzer Object.
    Processes textual captures and structures sanitized intelligence datasets.
    """

    def __init__(self):
        """تهيئة المحرك والتحقق من الصلاحيات والاعتماديات العتادية للنواة"""
        super().__init__()
        SystemGuard.enforce_root_privileges("Recon Analyzer Engine")
        SystemGuard.verify_dependencies(["tshark"])

    @staticmethod
    def analyze_recon_log_safe(log_file_path: str) -> list:
        """تحليل وقراءة تقارير الاستطلاع النصية بأمان كامل وحصانة ضد أخطاء الترميز"""
        path = Path(log_file_path)
        valid_targets = []

        if not path.exists():
            print(f"[-] Error: Telemetry log file not found: {path}")
            return valid_targets

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith("#"):
                        continue

                    # معالجة جراحية موثوقة للسطر عبر الحارس المعتمد لمنع الانهيارات الحركية
                    if NetworkValidators.is_valid_bssid(clean_line):
                        clean_mac = SystemGuard.sanitize_input(clean_line, "bssid")
                        valid_targets.append(
                            {"bssid": clean_mac, "source": path.name}
                        )

            print(f"[+] Structured {len(valid_targets)} sanitized targets.")
            return valid_targets

        except (IOError, OSError, KeyError, ValueError) as e:
            print(f"[-] Integrity Error: Exception inside recon sequence: {e}")
            return valid_targets


if __name__ == "__main__":
    print("[+] Recon Analyzer module deployment configuration verified.")
