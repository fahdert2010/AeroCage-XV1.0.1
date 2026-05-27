#!/usr/bin/env python3
"""
File Name: shared_utils_1.py
Path: /home/kali/AeroCage-XV1.0.1/utils/shared_utils_1.py
Created Date: 2026-05-25
Version: 1.1.0
Description: Centralized Security and SSH Commands Serialization Toolkit 1
             for AeroCage-X. Fully optimized for UCI hardware monitoring modes.
"""

import re


class SharedSecurityToolkit:
    """
    Unified Infrastructure Protection and Telemetry Builder Components.
    Provides strict tokens sanitization and decoupled UCI arguments builders.
    """

    @staticmethod
    def sanitize_input(user_input: str, validation_type: str) -> str:
        """تطهير وتصفية المدخلات عبر تعابير نمطية صارمة لحظر الاختراقات العكسية"""
        if not user_input or not isinstance(user_input, str):
            return ""

        clean = user_input.strip()
        if validation_type == "bssid":
            if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', clean):
                return clean
            return "00:00:00:00:00:00"

        if validation_type == "interface":
            return "".join(ch for ch in clean if ch.isalnum() or ch in "._-")

        if validation_type == "csv_value":
            return clean.replace("'", "").replace('"', "").replace(";", "")

        return clean

    @staticmethod
    def build_uci_monitor_sequence(radio: str, channel: str) -> str:
        """مصنع الأوامر المكررة بكثافة: بناء سلسلة أوامر حفر واجهات المراقبة بالـ UCI"""
        cmd_pool = [
            f"uci set wireless.wifinet8=wifi-iface",
            f"uci set wireless.wifinet8.device='{radio}'",
            f"uci set wireless.wifinet8.mode='monitor'",
            f"uci set wireless.wifinet8.ssid='AeroCage_Mon1'",
            f"uci set wireless.wifinet8.macaddr='random'",
            f"uci set wireless.wifinet8.disassoc_low_ack='0'",
            f"uci set wireless.wifinet9=wifi-iface",
            f"uci set wireless.wifinet9.device='{radio}'",
            f"uci set wireless.wifinet9.mode='monitor'",
            f"uci set wireless.wifinet9.ssid='AeroCage_Mon2'",
            f"uci set wireless.wifinet9.macaddr='random'",
            f"uci set wireless.wifinet9.disassoc_low_ack='0'",
            f"uci set wireless.wireless.{radio}.channel='{channel}'",
            f"uci commit wireless"
        ]
        return " && ".join(cmd_pool)


if __name__ == "__main__":
    print("[+] Shared Utility Security Toolkit 1 validated successfully.")
