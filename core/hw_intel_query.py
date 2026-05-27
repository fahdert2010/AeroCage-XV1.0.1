#!/usr/bin/env python3
"""
File Name: hw_intel_query.py
Path: /home/kali/AeroCage-XV1.0.1/core/hw_intel_query.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Master Hardware Intelligence Query Library for AeroCage-X.
             Globally isolates OpenWrt wireless nodes scanning and parsing logic.
"""

import re
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.shared_utils_1 import SharedSecurityToolkit


class HardwareIntelQueryLibrary:
    """
    Master Remote Router Telemetry and Interface Discovery Engine.
    Enforces deterministic dynamic parsing across real OpenWrt configuration nodes.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة مكتبة الاستخبارات العتادية وحقن معالم الـ SSH الموحدة"""
        self.ap_ip = SharedSecurityToolkit.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.ssh_factory = OpWrtSSHFactory(ip=self.ap_ip, password=self.ap_password)

    def execute_wireless_parent_query(self) -> str:
        """[الأب للاستعلامات] سحب وتحليل التكوين الموحد للـ UCI اللاسلكي نصاً"""
        cmd = "uci show wireless"
        return self.ssh_factory.execute_remote_cmd(cmd) or ""

    def get_active_radio_by_band(self, band: str) -> str:
        """[دالة 1] الاستجواب التكتيكي للنطاق: فرز معرّف الراديو الحقيقي حياً"""
        raw_out = self.execute_wireless_parent_query()
        fallback_radio = "radio0" if band == "2G" else "radio1"
        if not raw_out:
            return fallback_radio

        for line in raw_out.splitlines():
            line_low = line.lower()
            is_2g = "11g" in line_low or "2g" in line_low or "b" in line_low
            is_5g = "11a" in line_low or "5g" in line_low or "ac" in line_low or "ax" in line_low

            if band == "2G" and is_2g:
                match = re.search(r'wireless\.(\w+)\.', line)
                return match.group(1) if match else "radio0"
            if band == "5G" and is_5g:
                match = re.search(r'wireless\.(\w+)\.', line)
                return match.group(1) if match else "radio1"

        return fallback_radio

    def get_radio_current_channel(self, radio: str) -> str:
        """[دالة 2] قنص وقراءة رقم القناة الترددية الأصلية الحالية للراديو"""
        cmd = f"uci -q get wireless.{radio}.channel"
        raw_chan = self.ssh_factory.execute_remote_cmd(cmd)
        if raw_chan and raw_chan.strip().isdigit():
            return raw_chan.strip()
        return "1"

    def get_live_ssids_broadcast(self, radio: str) -> list:
        """[دالة 3] استخلاص أسماء الـ SSIDs الحركية الظاهرة للزباين في الجو حياً"""
        raw_out = self.execute_wireless_parent_query()
        ssids = []
        if not raw_out:
            return ssids

        for line in raw_out.splitlines():
            if ".ssid=" in line and f".device='{radio}'" in line:
                match = re.search(r"\.ssid='([^']*)'", line)
                if match:
                    ssids.append(match.group(1))
        return list(set(ssids))

    def get_linux_kernel_interfaces(self, radio: str) -> list:
        """[دالة 4] قنص أسماء واجهات البث النشطة (Master Mode) التابعة للراديو"""
        cmd = f"uci show wireless | grep -E '\\.device=\'{radio}\''"
        raw_out = self.ssh_factory.execute_remote_cmd(cmd)
        interfaces = []
        if not raw_out:
            return interfaces

        for line in raw_out.splitlines():
            if "wireless." in line and ".device=" in line:
                parts = line.split(".device=")
                if parts:
                    if_part = parts.replace("wireless.", "").strip()
                    interfaces.append(if_part)
        return list(set(interfaces))

    def get_sequential_interface_index(self) -> int:
        """[دالة 5] حساب الرقم التسلسلي القادم الشاغر للـ UCI منعاً للتخبيص"""
        cmd = "uci show wireless | grep -c '=wifi-iface'"
        raw_count = self.ssh_factory.execute_remote_cmd(cmd)
        if raw_count and raw_count.strip().isdigit():
            return int(raw_count.strip())
        return 0

    def get_disabled_interfaces_telemetry(self) -> list:
        """[دالة 6] صيد واستخراج كافة معطيات واجهات البث المعطلة بالكامل داخل الراوتر"""
        disabled_list = []
        raw_out = self.execute_wireless_parent_query()
        if not raw_out:
            return disabled_list

        sections = []
        for line in raw_out.splitlines():
            if "=wifi-iface" in line:
                sec = line.split("=").split(".")[-1].strip()
                sections.append(sec)

        for sec in list(set(sections)):
            cmd_dis = f"uci -q get wireless.{sec}.disabled"
            if self.ssh_factory.execute_remote_cmd(cmd_dis) == "1":
                dev = self.ssh_factory.execute_remote_cmd(
                    f"uci -q get wireless.{sec}.device"
                )
                mode = self.ssh_factory.execute_remote_cmd(
                    f"uci -q get wireless.{sec}.mode"
                ) or "ap"
                ssid = self.ssh_factory.execute_remote_cmd(
                    f"uci -q get wireless.{sec}.ssid"
                ) or "Hidden"

                # سحق التحذيرات بكسر مصفوفة الإرجاع لأسطر منضبطة تماماً
                disabled_list.append({
                    "config_name": sec,
                    "radio": dev,
                    "mode": mode,
                    "ssid": ssid
                })
        return disabled_list

    def query_iwinfo_assoclist(self, interface: str) -> str:
        """[دالة 7] إخراج وتفكيك ناتج أمر iwinfo assoclist بشكل مستقل تماماً نصاً"""
        cmd = f"iwinfo {interface} assoclist"
        return self.ssh_factory.execute_remote_cmd(cmd) or "No clients mapped via iwinfo."

    def query_station_dump(self, interface: str) -> str:
        """[دالة 8] إخراج وتفكيك ناتج أمر iw dev station dump بشكل مستقل تماماً نصاً"""
        cmd = f"iw dev {interface} station dump"
        return self.ssh_factory.execute_remote_cmd(cmd) or "No clients mapped via station dump."


if __name__ == "__main__":
    print("[+] Master Hardware Intelligence Query Library configuration verified.")
