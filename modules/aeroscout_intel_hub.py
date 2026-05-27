#!/usr/bin/env python3
"""
File Name: aeroscout_intel_hub.py
Path: /home/kali/AeroCage-XV1.0.1/modules/aeroscout_intel_hub.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Tactical Wireless Intel Recon Analytics Dashboard Terminal Node.
             Fully linked with sharded database managers and ubus scouts.
"""

import sys
from pathlib import Path

# ربط محاور مفسر بايثون بجذر المستودع لضمان قراءة التبعيات الفرعية النظيفة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from core.intel_ubus_scout import IntelUbusScout


class AeroScoutIntelHub:
    """
    Main Intelligence Analytics Console Hub.
    Binds textual dashboard controls with live OpenWrt database channels.
    """

    def __init__(self):
        """تهيئة منصة السجلات والتحقق الاستباقي من صلاحيات الـ Root محلياً"""
        SystemGuard.enforce_root_privileges("AeroScout Intel Hub Console")
        self.db_manager = DatabaseManager()
        self.ubus_scout = IntelUbusScout()

    def get_registered_hardware_units(self) -> list:
        """سحب وعزل أجهزة الترسانة والعتاد الملقم حياً من شظايا قاعدة البيانات المحدثة"""
        all_targets = self.db_manager.get_all_active_targets()
        hardware_units = []
        
        for target in all_targets:
            if target.get("status") == "Hardware_AP_Active":
                hardware_units.append(target)
        return hardware_units

    def main_menu(self):
        """حلقة شاشة التحكم التفاعلية الكبرى لسطر الأوامر للـ Intel Hub"""
        while True:
            print("\n" + "=" * 65)
            print(" 📡 [ منصة التحليل الاستخباراتي للتغيرات اللاسلكية: AeroScout ]")
            print("=" * 65)
            print("  [ 1 ] بدء جولة الفحص الحي وقراءة التغييرات والزبائن النشطين")
            print("  [ 0 ] إغلاق نفق المنظومة المنفصلة والخروج")
            print("=" * 65 + "\n")

            try:
                opt = input("🔢 الاختيار: ").strip()
                if opt in ["0", "exit", ""]:
                    print("[*] Terminating Intel Hub console node context cleanly.")
                    break

                if opt == "1":
                    aps = self.get_registered_hardware_units()
                    if not aps:
                        print(" ❌ لا توجد راوترات أو عتاد ملقم في قاعدة البيانات حالياً!")
                        continue

                    print("\n[ اختر اسم الأكسس بوينت الذي سيقوم بالمسح حياً ]:")
                    for idx, ap in enumerate(aps):
                        print(f"   [{idx + 1}] الاسم: {ap.get('essid')} | IP: {ap.get('bssid')}")

                    ap_idx = input("\n🔢 رقم الأكسس: ").strip()
                    if not ap_idx.isdigit() or int(ap_idx) > len(aps):
                        continue
                    
                    selected_ap = aps[int(ap_idx) - 1]
                    target_ip = selected_ap.get("bssid")

                    print(f"\n[*] جاري استجواب حافلة أوامر الراوتر [{target_ip}] عبر UBUS...")
                    # تمرير الواجهة المخصصة للبث وسحب بيانات الزباين حياً وبأمان عبر المحرك الموحد
                    clients = self.ubus_scout.fetch_openwrt_clients_safe("phy1-ap1")
                    
                    print(f"\n[+ SUCCESS] تم جلب وحصاد سجلات الأثير للهدف بنجاح حياً!")
                    print(f"📱 عدد الأجهزة النشطة المرصودة حالياً: {len(clients)}")
                    for c in clients:
                        print(f"   └── 📱 MAC: {c['mac']} | 📶 قوة الإشارة: {c['signal']} dBm")

            except (IOError, OSError, ValueError, KeyboardInterrupt) as e:
                print(f"\n[-] Core Intel Hub Exception pipeline halted: {e}")
                break


if __name__ == "__main__":
    hub = AeroScoutIntelHub()
    hub.main_menu()
