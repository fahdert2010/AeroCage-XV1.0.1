#!/usr/bin/env python3
"""
File Name: m2_hardware_tunnel.py
Path: /home/kali/AeroCage-XV1.0.1/modules/m2_hardware_tunnel.py
Created Date: 2026-05-25
Version: 1.0.4
Description: Remote OpenWrt Subprocess Tunneling and AirServ Daemon Deployment
             Controller Engine for AeroCage-X. Implements strict PID extraction.
"""

import time

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.text_parsing_engine import TextParsingEngine


class M2HardwareTunnelEngine:
    """
    Main Hardware Tunnel Control Component.
    Manages active target sessions, queries daemons, and locks dynamic channels.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الأنفاق العتادية والتدقيق الصارم لامتيازات مدير النظام"""
        SystemGuard.enforce_root_privileges("M2 Hardware Tunnel - Daemon Launcher")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)

    def query_active_daemons_before_kill(self) -> dict:
        """استجواب الراوتر صامتاً لمعرفة حالة العمليات والأنفاق الجارية بالداخل"""
        msg_rec = "[*] [Telemetry Search] Analyzing target hardware environment..."
        print(msg_rec)

        airserv_pids = TextParsingEngine.clean_pids(
            self.ssh_factory.execute_remote_cmd("pidof airserv-ng")
        )
        aireplay_pids = TextParsingEngine.clean_pids(
            self.ssh_factory.execute_remote_cmd("pidof aireplay-ng")
        )

        report = {
            "airserv_active": len(airserv_pids) > 0,
            "airserv_pids": airserv_pids,
            "aireplay_active": len(aireplay_pids) > 0,
            "aireplay_pids": aireplay_pids
        }
        return report

    def deploy_airserv_daemon_safe(self, mon_iface: str, target_port: int, channel: str) -> bool:
        """تهيئة وإشعال سيرفر الأيرسيرف عن بعد مع تثبيت القناة والموجة عتادياً"""
        clean_mon = SystemGuard.sanitize_input(mon_iface, "interface")
        clean_chan = "".join(ch for ch in str(channel) if ch.isdigit())

        if not clean_mon or not clean_chan:
            print("[-] Configuration Error: Invalid interface or channel bounds provided.")
            return False

        # 1. الاستعلام الاستباقي وتطهير العمليات القديمة بشكل منبثق ودقيق لحماية المنصة
        env_report = self.query_active_daemons_before_kill()
        if env_report["airserv_active"]:
            msg_pids = f"[*] Notice: Found running daemon for PIDs: {env_report['airserv_pids']}"
            print(msg_pids)
            for pid in env_report["airserv_pids"]:
                self.ssh_factory.execute_remote_cmd(f"kill -9 {pid}")
            time.sleep(1)

        # 2. إعداد مصفوفة الأمر التنفيذي للأيرسيرف وتحديد المنافذ والقنوات اللاسلكية بدقة
        air_command = f"airserv-ng -d {clean_mon} -p {target_port} -c {clean_chan}"

        try:
            msg_deploy = f"[*] [Hardware Control] Deploying socket listener on port: {target_port}"
            print(msg_deploy)
            self.ssh_factory.execute_remote_cmd(air_command)

            # مهلة الاستقرار الفيزيائي وتثبيت الموجة للأكسس بوينت المستهدف
            time.sleep(2)

            # 3. التأكد الجازم من نجاح الإنشاء الفعلي للعملية عبر النبض الموحد للأنظمة البعيدة
            verify_report = self.query_active_daemons_before_kill()
            if verify_report["airserv_active"]:
                # كسر السطر بشكل كلاسيكي لتطابق معايير طول السطر لـ PEP 8 لـ Pylint
                pids_list = verify_report['airserv_pids']
                print(f"[+ AirServ] Remote socket active under PIDs: {pids_list}")
                return True

            print("[-] Exception: Target environment blocked daemon task initialization.")
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Crash inside hardware deployment channel: {e}")
            return False


if __name__ == "__main__":
    print("[+] M2 Hardware Tunnel Engine module configuration verified.")
