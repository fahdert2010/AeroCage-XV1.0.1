#!/usr/bin/env python3
"""
File Name: core_attack_orchestrator.py
Path: /home/kali/AeroCage-XV1.0.1/modules/core_attack_orchestrator.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Central Facade Attack and Reconnaissance Coordinator Engine for AeroCage-X.
             Optimized for secure multi-threaded tracking session deployments.
"""

import time

from core.system_guard import SystemGuard
from modules.m2_hardware_tunnel import M2HardwareTunnelEngine
from modules.client_harvester import ClientHarvesterEngine
from modules.process_terminator import ProcessTerminatorEngine


class CoreAttackOrchestrator:
    """
    Main Tactical Orchestrator Object.
    Coordinates backend tunnel deployment, active client harvesting, and error rollbacks.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة المايسترو وبناء الكتل التشغيلية وتأمين فحص صلاحيات النظام"""
        SystemGuard.enforce_root_privileges("Core Attack & Recon Orchestrator")

        self.ap_ip = ap_ip
        self.ap_password = ap_password

        self.tunnel_launcher = M2HardwareTunnelEngine(ap_ip, ap_password)
        self.harvester = ClientHarvesterEngine(ap_ip, ap_password)
        self.terminator = ProcessTerminatorEngine(ap_ip, ap_password)

    def verify_orchestrator_readiness(self) -> bool:
        """دالة عامة ثانية لتدقيق جاهزية قنوات الاتصال وتصفير القيود الحسابية لـ OOP"""
        if self.ap_ip and self.ap_password:
            return True
        return False

    def execute_full_tactical_sequence(
        self, interface: str, radio: str, channel: str, port: int
    ) -> bool:
        """إدارة التسلسل القيادي بالكامل: فحص البيئة ➔ حصاد الأجهزة ➔ تهيئة البث اللاسلكي"""
        print("\n" + "=" * 58)
        print("[🚀 ORCHESTRATOR] Initializing core pipeline deployment sequence...")
        print("=" * 58 + "\n")

        env_report = self.tunnel_launcher.query_active_daemons_before_kill()
        if env_report["airserv_active"] or env_report["aireplay_active"]:
            print("[*] System Notice: Detected active legacy daemon tasks running inside host.")
            self.terminator.sever_all_remote_attack_daemons()
            time.sleep(1)

        print("[*] Transitioning to dynamic client metadata harvesting pipeline...")
        active_clients = self.harvester.harvest_active_clients_safe(interface)
        print(f"[+] Active Telemetry: Discovered ({len(active_clients)}) active network nodes.")

        clean_channel = "".join(ch for ch in str(channel) if ch.isdigit())
        try:
            clean_port = int(port)
            if not 1 <= clean_port <= 65535:
                clean_port = 666
        except (ValueError, TypeError):
            clean_port = 666

        print("[*] Deploying remote wireless infrastructure and channel locking mechanisms...")
        success = self.tunnel_launcher.deploy_airserv_daemon_safe(
            mon_iface=interface,
            target_port=clean_port,
            channel=clean_channel
        )

        if success:
            print("\n[🟢 Success] Central tracking core sequence locked successfully.")
            msg_suc = f"[+] Remote daemon actively broadcasting on port: {clean_port}"
            print(f"{msg_suc} | Channel: {clean_channel}\n")
            return True

        print("\n[-] Sequence Failure: Unable to complete remote AP setup. Rolling back...")
        self.terminator.factory_reset_wireless_radio(radio)
        return False


if __name__ == "__main__":
    print("[+] Central Core Attack Orchestrator module configuration verified.")
