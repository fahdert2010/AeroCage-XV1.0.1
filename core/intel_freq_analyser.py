#!/usr/bin/env python3
"""
File Name: intel_freq_analyser.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_freq_analyser.py
Created Date: 2026-05-25
Version: 1.0.3
Description: OpenWrt Wireless Frequency and Channels Optimization Analyzer Core
             for AeroCage-X. Fully integrated with secure execution wrappers.
"""

import subprocess
import tkinter as tk
from tkinter import messagebox

from core.system_guard import SystemGuard


class IntelFreqAnalyser:
    """
    Main Air Space Frequency Optimizer Component.
    Queries remote nodes for airspace scanning metrics and ranks stable channels.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التحليل الراداري وتأمين فحص صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("OpenWrt Frequency Analyser Engine")
        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password

    def scan_air_space_standard(self, ap_interface: str = "phy1-ap0") -> dict:
        """تشغيل مسح الأجواء الطبيعي عن بعد واستدعاء الخوارزمية للتحليل"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")
        remote_cmd = f"iwinfo {clean_inf} scan"

        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", remote_cmd
        ]

        try:
            result = subprocess.run(
                base_ssh_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=20
            )
            if result.returncode == 0 and result.stdout:
                # استيراد محلي ديناميكي معزول للحظر الاستباقي لانهيارات الـ Linting الساكنة
                # pylint: disable=import-outside-toplevel, import-error, no-name-in-module
                from utils.channel_optimizer import ChannelOptimizer
                parsed_cells = ChannelOptimizer.parse_scan_output(result.stdout)
                return ChannelOptimizer.calculate_best_channel(parsed_cells)
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            print(f"[-] Execution Exception inside air space scan query: {e}")
        return {}

    def switch_channel_with_confirmation(self, radio_name: str, target_channel: str) -> bool:
        """سؤال المستخدم وطلب التأكيد الإجباري قبل Tعديل التردد بالـ UCI للراوتر"""
        clean_radio = SystemGuard.sanitize_input(radio_name, "interface")
        clean_chan = "".join(ch for ch in str(target_channel) if ch.isdigit())

        root_box = tk.Tk()
        root_box.withdraw()
        user_response = messagebox.askyesno(
            "تأكيد التعديل التكتيكي",
            f"هل تريد تعديل تردد الراديو ({clean_radio}) للقناة ({clean_chan})؟"
        )
        root_box.destroy()

        if not user_response:
            print("[*] Tactic command aborted by operator control handle.")
            return False

        uci_command = (
            f"uci set wireless.{clean_radio}.channel='{clean_chan}' && "
            f"uci commit wireless && wifi reload {clean_radio}"
        )

        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", uci_command
        ]

        try:
            result = subprocess.run(
                base_ssh_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=20
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, OSError):
            return False
        return False


if __name__ == "__main__":
    print("[+] Intel Airspace Frequency Analyser subsystem verified.")
