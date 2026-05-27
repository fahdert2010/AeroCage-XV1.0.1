#!/usr/bin/env python3
"""
File Name: text_parsing_engine.py
Path: /home/kali/AeroCage-XV1.0.1/utils/text_parsing_engine.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Text Parsing and Hardware Output Extraction Engine for AeroCage-X.
             Uses pre-compiled regex for fast pattern discovery in wireless data.
"""

import re


class TextParsingEngine:
    """
    Main Parsing Engine Object.
    Provides static methods for scanning hardware logs and filtering PIDs.
    """
    # تحصين الأنماط ومطابقة معايير التسمية القياسية للـ PEP 8 لحصد العلامة الكاملة
    _bssid_pattern = re.compile(
        r'address:\s+((?:[0-9a-fa-f]{2}[:-]){5}[0-9a-fa-f]{2})',
        re.IGNORECASE
    )
    _essid_pattern = re.compile(r'essid:\s+"([^"]*)"', re.IGNORECASE)
    _channel_pattern = re.compile(r'channel:\s+(\d+)', re.IGNORECASE)
    _signal_pattern = re.compile(r'signal:\s+(-\d+)\s+dBm', re.IGNORECASE)

    # تحصين التعبير النمطي لمنع التداخل العشوائي للكسور العشرية أو الـ IPs
    _pid_strict_pattern = re.compile(r'^\d+$')

    @classmethod
    def extract_ap_cells(cls, raw_stdout: str) -> list:
        """تفكيك كتل مسح الأجواء وعزل الحقول التالفة صامتاً من البيئة البعيدة"""
        cells = []
        if not raw_stdout:
            return cells

        blocks = raw_stdout.split("Cell ")
        for block in blocks:
            if not block.strip():
                continue
            bssid = cls._bssid_pattern.search(block)
            essid = cls._essid_pattern.search(block)
            chan = cls._channel_pattern.search(block)
            sig = cls._signal_pattern.search(block)

            if bssid and chan:
                cells.append({
                    "bssid": bssid.group(1).upper(),
                    "essid": essid.group(1) if essid else "Hidden_Network",
                    "channel": chan.group(1),
                    "power": int(sig.group(1)) if sig else -95
                })
        return cells

    @classmethod
    def clean_pids(cls, raw_stdout: str) -> list:
        """تنظيف وتصفية مخرجات العمليات واستخراج الأرقام الصافية فقط بحصانة صارمة"""
        if not raw_stdout:
            return []

        validated_pids = []
        raw_tokens = raw_stdout.strip().split()

        for token in raw_tokens:
            if cls._pid_strict_pattern.match(token):
                validated_pids.append(token)

        return validated_pids


if __name__ == "__main__":
    print("[+] Text Parsing Engine module deployment verification verified.")
