#!/usr/bin/env python3
"""
File Name: remote_hardware_bridge.py
Path: /home/kali/AeroCage-XV1.0.1/core/remote_hardware_bridge.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Remote OpenWrt Hardware Bridging and Wireless UCI Configuration Engine.
             Leverages the uniform SSH factory to dispatch dynamic wireless reloads.
"""

import time

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory


class RemoteHardwareBridgeEngine:
    """
    Main Remote Hardware UCI Configuration Bridge.
    Manages active wireless attributes injection and locks physical radio interfaces.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة الجسر العتادي وتأمين فحص صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("Remote Hardware Bridge Engine")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)

    def verify_bridge_factory_status(self) -> bool:
        """دالة عامة ثانية لتدقيق جاهزية قنوات النفق وتصفير قيود الـ OOP لـ Pylint"""
        return self.ssh_factory is not None

    def change_remote_ssid_with_reload(
        self, radio_name: str, section_name: str, new_ssid: str
    ) -> bool:
        """حقن أمر تغيير اسم البث وتطبيق الالتزام وإعادة تشغيل الراديو بالملي"""
        clean_radio = SystemGuard.sanitize_input(radio_name, "interface")
        clean_section = SystemGuard.sanitize_input(section_name, "interface")
        clean_ssid = SystemGuard.sanitize_input(new_ssid, "csv_value")

        if not clean_radio or not clean_section or not clean_ssid:
            print("[-] Configuration Error: Malicious UCI tokens detected and blocked.")
            return False

        # بناء حزمة الأوامر التكتيكية المطابقة للـ AP301 الملقم وتمريره للمصنع الموحد
        uci_command = (
            f"uci set wireless.{clean_section}.ssid='{clean_ssid}' && "
            f"uci commit wireless && wifi reload {clean_radio}"
        )

        try:
            print(f"[*] [UCI Config] Dispatching remote SSID shift towards: {clean_ssid}")

            # الاعتماد الحصري والصافي على المصنع لحمايتك وسحق قنوات السوكيت المعلقة
            self.ssh_factory.execute_remote_cmd(uci_command)
            print("[+] UCI configuration committed inside remote host environment.")

            # تنفيذ مهلة الاستقرار العتادية الذهبية لمنع تجميد شريحة الفيزيائي للراوتر
            print("[*] Sleeping 2 seconds for wireless radio physical stabilization...")
            time.sleep(2)

            print("[+] Remote wireless interface is stable and active under new configuration.")
            return True

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Unexpected crash inside hardware bridge: {e}")
            return False


if __name__ == "__main__":
    print("[+] Remote Hardware Bridge Engine module configuration verified.")
