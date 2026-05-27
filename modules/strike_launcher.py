#!/usr/bin/env python3
"""
File Name: strike_launcher.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_launcher.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Task Execution Launcher Wrapper Module for AeroCage-X.
             Coordinates dynamic wireless sessions via strict OOP bindings.
"""

import sys
from pathlib import Path

# ربط المسارات بالنواة المركزية والمساعدات الفنية لمنظومة AeroCage-X
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position, no-name-in-module
from core.system_guard import SystemGuard
from modules.strike_manager import StrikeManagerEngine


class StrikeLauncher:
    """
    Main Strike Launcher Wrapper Object.
    Acts as an intermediary layer between UI triggers and back-end stream tasks.
    """

    def __init__(self):
        """تهيئة كائن الإطلاق والتحقق من الصلاحيات والاعتماديات الحتمية للنظام"""
        # تفعيل حارس صلاحيات الـ Root الفوري محلياً لحماية السكربت عند التهيئة الكائنية
        SystemGuard.enforce_root_privileges("Strike Launcher Mod")
        SystemGuard.verify_dependencies(["aireplay-ng"])
        self.manager = StrikeManagerEngine()

    def launch_strike_session(self, interface: str, target_bssid: str) -> bool:
        """تلقيم وإطلاق جلسة الفحص والمراقبة الآمنة عبر المدير المركزي المطور"""
        clean_inf = SystemGuard.sanitize_input(interface, "interface")
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()

        if not clean_inf or not clean_mac:
            print("[-] Error: Refused to initialize execution parameters due to invalid inputs.")
            return False

        try:
            print("[*] Forwarding sanitized environment variables to core management engine...")
            success = self.manager.queue_and_launch_strike_safe(clean_inf, clean_mac)
            return success
        except (RuntimeError, AttributeError, OSError) as e:
            print(f"[-] Integrity Error: Sudden crash inside launcher wrapper thread: {e}")
            return False

    def stop_strike_session(self, target_bssid: str):
        """إيقاف الجلسة المحددة بالماك أدرس برمجياً وتطهير مسارات الذاكرة العشوائية"""
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()
        if clean_mac:
            self.manager.abort_target_strike(clean_mac)


if __name__ == "__main__":
    launcher_instance = StrikeLauncher()

    # دعم التشغيل المباشر من سطر الأوامر بمدخلات مصفاة وآمنة تماماً
    if len(sys.argv) == 3:
        raw_inf = sys.argv[1]
        raw_mac = sys.argv[2]
        print("[+] Received local CLI argument parameters initialization vector.")
        launcher_instance.launch_strike_session(raw_inf, raw_mac)
    else:
        print("[*] Strike Launcher session utility module verified.")
        print("[*] Direct CLI Usage: python3 strike_launcher.py <interface> <bssid>")
