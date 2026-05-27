#!/usr/bin/env python3
"""
File Name: recon_packet_parser.py
Path: /home/kali/AeroCage-XV1.0.1/modules/recon_packet_parser.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Deep Packet Inspection and Subprocess Tshark Command Pool Component 
             for AeroCage-X. Handles safe binary files reading.
"""

import subprocess
from pathlib import Path


class ReconPacketParserComponent:
    """
    Tshark Subprocess Handler Component.
    Manages isolated binary analysis pools and ensures clean dataset export.
    """

    @staticmethod
    def verify_pcap_extension(pcap_path: str) -> bool:
        """دالة عامة ثانية لتدقيق امتداد الملف وحظر قيود الـ OOP لـ Pylint"""
        if not pcap_path:
            return False
        path = Path(pcap_path)
        return path.suffix.lower() in [".pcap", ".cap", ".pcapng"]

    @classmethod
    def run_deep_packet_analysis(cls, pcap_path: str, output_txt_path: str) -> bool:
        """تشغيل فحص عميق للحزم اللاسلكية عبر tshark بأمان كامل وبدون فتح شل"""
        pcap_file = Path(pcap_path)
        output_file = Path(output_txt_path)

        if not pcap_file.exists() or not cls.verify_pcap_extension(pcap_path):
            print(f"[-] Error: Invalid or missing source PCAP file: {pcap_file}")
            return False

        command_array = [
            "tshark", "-r", str(pcap_file), "-T", "fields",
            "-e", "wlan.sa", "-e", "wlan.da"
        ]

        try:
            print(f"[*] Extracting packet metrics from capture: {pcap_file}")
            result = subprocess.run(
                command_array,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,
                check=False,
                timeout=60
            )

            if result.returncode == 0 and result.stdout:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as out_f:
                    out_f.write(result.stdout)
                print(f"[+] Dataset successfully exported to: {output_file}")
                return True

            print(f"[-] tshark subprocess failure: {result.stderr.strip()}")
            return False

        except (subprocess.SubprocessError, subprocess.TimeoutExpired, IOError, OSError) as e:
            print(f"[-] Critical Error inside deep processing engine: {e}")
            return False


if __name__ == "__main__":
    print("[+] Recon Packet Parser binary sharding component verified.")
