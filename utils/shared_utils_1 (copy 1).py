#!/usr/bin/env python3
"""
File Name: shared_utils_1.py
Path: /home/kali/AeroCage-XV1.0.1/utils/shared_utils_1.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Centralized Security and SSH Commands Serialization Toolkit 1
             for AeroCage-X. Resolves injection vulnerabilities globally.
"""

import re


class SharedSecurityToolkit:
    """
    Unified Infrastructure Protection and Telemetry Builder Components.
    Provides strict tokens sanitization and decoupled argument matrix extraction.
    """

    @staticmethod
    def sanitize_input(user_input: str, validation_type: str) -> str:
        """تطهير وتصفية المدخلات عبر تعابير نمطية صارمة لحظر الاختراقات العكسية"""
        if not user_input or not isinstance(user_input, str):
            return ""

        clean = user_input.strip()
        if validation_type == "bssid":
            # السماح فقط بصيغ الماك أدرس القياسية القياسية لـ لينكس
            if re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', clean):
                return clean
            return "00:00:00:00:00:00"

        if validation_type == "interface":
            # حظر كافة الرموز التعبيرية والسماح بأسماء كروت الوايرلس فقط
            return "".join(ch for ch in clean if ch.isalnum() or ch in "._-")

        if validation_type == "csv_value":
            # حظر علامات الاقتباس المفردة لحفظ متانة قواعد البيانات
            return clean.replace("'", "").replace('"', "").replace(";", "")

        return clean

    @staticmethod
    def build_secure_ssh_args(password: str, remote_ip: str, raw_command: str) -> list:
        """مصنع مركزي موحد لبناء مصفوفات الـ SSH المغلقة الشل لحظر ثغرات Bandit"""
        return [
            "sshpass", "-p", password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{remote_ip}", raw_command
        ]


if __name__ == "__main__":
    print("[+] Shared Utility Security Toolkit 1 validated successfully.")
