#!/usr/bin/env python3
"""
File Name: strike_watchdog.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_watchdog.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Fault Recovery and Daemon Health Watchdog Pool Engine for AeroCage-X.
             Optimized via centralized shared utility toolkits wrappers.
"""

import time
import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from utils.shared_utils_1 import SharedSecurityToolkit


class StrikeWatchdogEngine:
    """
    Main Task Watchdog Controller.
    Monitors process liveness and dynamically redeploys stalled tracking streams.
    """

    def __init__(self):
        """تهيئة محرك الحراسة وتأمين صلاحيات النظام محلياً ومنع الـ Dead-locks"""
        SystemGuard.enforce_root_privileges("Strike Watchdog Engine")

        self.proc_manager = ProcessManager()
        self.watchdog_active = False
        self.monitored_targets = {}
        self.lock = threading.Lock()

    def register_target_for_monitoring(
        self, interface: str, target_bssid: str, command_array: list
    ):
        """تسجيل وتلقيم هدف جديد في طابور الحراسة والمراقبة المستمرة"""
        clean_inf = SharedSecurityToolkit.sanitize_input(interface, "interface")
        clean_mac = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid")

        if not clean_inf or not clean_mac or not command_array:
            return

        with self.lock:
            target_key = f"{clean_inf}_{clean_mac}"
            self.monitored_targets[target_key] = {
                "interface": clean_inf,
                "bssid": clean_mac,
                "command": command_array
            }
            msg_reg = f"[+] Successfully registered target node [{clean_mac}]"
            print(f"{msg_reg} inside watchdog queue.")

    def start_watchdog_loop_async(self, check_interval_sec: int = 5):
        """إطلاق محرك الحراسة والرقابة في الخلفية بأمان عالي ودون حظر المنظومة"""
        if self.watchdog_active:
            return

        self.watchdog_active = True
        worker_thread = threading.Thread(
            target=self._watchdog_core_worker,
            args=(check_interval_sec,),
            daemon=True
        )
        worker_thread.start()
        print("[*] Strike Watchdog supervisor loop successfully activated.")

    def _watchdog_core_worker(self, interval: int):
        """العامل الخلفي المعزول لفحص حالة المكونات وإعادة إنعاشها برمجياً بأمان"""
        while self.watchdog_active:
            try:
                with self.lock:
                    current_queue = list(self.monitored_targets.values())

                for info in current_queue:
                    mac = info["bssid"]
                    cmd_array = info["command"]

                    process = self.proc_manager.active_processes.get(mac)

                    if process is None or process.poll() is not None:
                        print(f"[⚠️] Watchdog Alert: Broken daemon handle for [{mac}].")
                        print("[*] Initiating automated hot-recovery deployment...")

                        self.proc_manager.terminate_process(mac)
                        self.proc_manager.spawn_process_safe(mac, cmd_array)

                time.sleep(interval)

            except (RuntimeError, ValueError, AttributeError, SystemError) as e:
                print(f"[-] Integrity Error inside core watchdog loop: {e}")
                time.sleep(interval)

    def unregister_and_stop_target(self, target_bssid: str):
        """حذف الهدف من طابور الحراسة وإخماد عمليته نهائياً وتصفير ممراته"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid")

        with self.lock:
            keys_to_remove = [
                k for k, v in self.monitored_targets.items() if v["bssid"] == clean_mac
            ]
            for k in keys_to_remove:
                del self.monitored_targets[k]

        self.proc_manager.terminate_process(clean_mac)
        msg_out = f"[+] Successfully unallocated tracking registers for: [{clean_mac}]"
        print(msg_out)

    def stop_watchdog_completely(self):
        """إيقاف محرك الكلب الحارس بالكامل وتطهير الذاكرة"""
        self.watchdog_active = False
        with self.lock:
            self.monitored_targets.clear()
        print("[+] Core Watchdog deallocated. Monitoring queues flushed cleanly.")


if __name__ == "__main__":
    print("[+] Strike Watchdog Engine module deployment configuration verified.")
