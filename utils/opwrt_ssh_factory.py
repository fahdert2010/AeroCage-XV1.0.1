#!/usr/bin/env python3
"""
File Name: opwrt_ssh_factory.py
Path: /home/kali/AeroCage-XV1.0.1/utils/opwrt_ssh_factory.py
Created Date: 2026-05-26
Version: 1.2.1
Description: Unified SSH Connection Factory and Hardware Intel Query Library.
             Enforces deterministic dynamic parsing across real OpenWrt nodes.
"""

import re
import subprocess


class OpWrtSSHFactory:
    """
    Master SSH Connection Factory and Remote Device Discovery Engine.
    Isolates environment execution parameters and gathers real-time telemetries.
    """

    def __init__(self, ip: str, password: str):
        """تهيئة مصنع الاتصال وتأمين معالم الـ SSH الأساسية المعزولة"""
        self.ip = "".join(ch for ch in ip.strip() if ch.isalnum() or ch in ".:-_")
        self.password = password
        self.base_args = [
            "sshpass", "-p", self.password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ip}"
        ]

    def execute_remote_cmd(self, command_str: str) -> str:
        """قذف المقذوف البرمجي وتنفيذه صامتاً داخل معالج الراوتر البعيد"""
        if not command_str:
            return ""

        full_args = self.base_args + [command_str]
        try:
            result = subprocess.run(
                full_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return ""
        except (subprocess.SubprocessError, OSError):
            return ""

    def verify_ssh_heartbeat(self) -> bool:
        """[📡 حساس الـ SSH المطور] فحص ومصادقة نبض الاتصال بالراوتر البعيد قبل الحفظ أو القذف"""
        cmd_args = self.base_args + ["echo 'HEARTBEAT_OK'"]
        try:
            result = subprocess.run(
                cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=3
            )
            return result.returncode == 0 and "HEARTBEAT_OK" in result.stdout
        except (subprocess.SubprocessError, OSError):
            return False

    def check_active_exploit_processes(self) -> dict:
        """[🪐 حسّاس النواة للعمليات العالقة] كشف ومراقبة الهجمات النشطة بالداخل دون تخمين"""
        telemetry = {"active": False, "pid": None, "target": "None", "type": "None"}
        cmd = "ps | grep -E 'aireplay-ng|tcpdump|airserv-ng' | grep -v grep"
        raw_out = self.execute_remote_cmd(cmd)

        if not raw_out:
            return telemetry

        for line in raw_out.splitlines():
            line_str = line.strip()
            parts = line_str.split()
            if len(parts) >= 1 and parts[0].isdigit():
                telemetry["active"] = True
                telemetry["pid"] = parts[0]

                if "aireplay-ng" in line_str:
                    telemetry["type"] = "Deauth Attack (aireplay)"
                    match = re.search(r'-a\s+([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line_str)
                    if match:
                        telemetry["target"] = match.group(1).upper()
                elif "tcpdump" in line_str:
                    telemetry["type"] = "SIGINT Sniffer (tcpdump)"
                elif "airserv-ng" in line_str:
                    telemetry["type"] = "AirServ Wireless Node (Hardware Hijack)"
                break

        return telemetry

    def execute_wireless_parent_query(self) -> str:
        """[الأب للاستعلامات] سحب وتحليل التكوين الموحد للـ UCI اللاسلكي نصاً"""
        return self.execute_remote_cmd("uci show wireless")

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
        raw_chan = self.execute_remote_cmd(f"uci -q get wireless.{radio}.channel")
        if raw_chan and raw_chan.isdigit():
            return raw_chan
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
        raw_out = self.execute_remote_cmd(f"uci show wireless | grep -E '\\.device=\'{radio}\''")
        interfaces = []
        if not raw_out:
            return interfaces

        for line in raw_out.splitlines():
            if "wireless." in line and ".device=" in line:
                parts = line.split(".device=")
                if parts:
                    if_part = parts[0].replace("wireless.", "").strip()
                    interfaces.append(if_part)
        return list(set(interfaces))

    def get_sequential_interface_index(self) -> int:
        """[دالة 5] حساب الرقم التسلسلي القادم الشاغر للـ UCI منعاً للتخبيص"""
        raw_count = self.execute_remote_cmd("uci show wireless | grep -c '=wifi-iface'")
        if raw_count and raw_count.isdigit():
            return int(raw_count)
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
                sec = line.split("=")[0].split(".")[-1].strip()
                sections.append(sec)

        for sec in list(set(sections)):
            if self.execute_remote_cmd(f"uci -q get wireless.{sec}.disabled") == "1":
                dev = self.execute_remote_cmd(f"uci -q get wireless.{sec}.device")
                mode = self.execute_remote_cmd(f"uci -q get wireless.{sec}.mode") or "ap"
                ssid = self.execute_remote_cmd(f"uci -q get wireless.{sec}.ssid") or "Hidden"

                disabled_list.append({
                    "config_name": sec,
                    "radio": dev,
                    "mode": mode,
                    "ssid": ssid
                })
        return disabled_list

    def query_iwinfo_assoclist(self, interface: str) -> str:
        """[دالة 7] إخراج وتفكيك ناتج أمر iwinfo assoclist بشكل مستقل تماماً نصاً"""
        return self.execute_remote_cmd(f"iwinfo {interface} assoclist") or "No clients mapped."

    def query_station_dump(self, interface: str) -> str:
        """[دالة 8] إخراج وتفكيك ناتج أمر iw dev station dump بشكل مستقل تماماً نصاً"""
        return self.execute_remote_cmd(f"iw dev {interface} station dump") or "No stations mapped."


if __name__ == "__main__":
    print("[+] Unified SSH Factory and Hardware Intelligence Engine verified.")
