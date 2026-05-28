#!/usr/bin/env python3
"""
File Name: ui_mission_components.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_mission_components.py
Created Date: 2026-05-27
Version: 1.0.2
Description: Responsive UI Factory Components Layout Interface for AeroCage-X.
             Enforces pure isolated widget placement and low local variable footprints.
"""

import tkinter as tk
from utils.opwrt_text_registry import MISSION_CONTROL
from utils.opwrt_text_processor import get_processed_rtl_msg


class UiMissionComponents:
    """
    Subsystem Component Interface Factory.
    Builds grid elements, text logs, and radio targets for mission windows.
    """

    def __init__(self, root_window: tk.Tk):
        """تهيئة مصنع المكونات وحقن مرجع النافذة السيادية للجلسة حياً"""
        self.root = root_window

    def draw_storage_profile_frame(self, target_mode_var) -> tk.LabelFrame:
        """بناء وتنسيق إطار الاختيار الحر للتخزين بالمسارات المعكوسة RTL"""
        t_frame = get_processed_rtl_msg("MISSION", "clean_air")
        storage_frame = tk.LabelFrame(
            self.root, text=t_frame, bg="#0B0C10",
            fg="#45A29E", font=("Arial", 10, "bold")
        )
        storage_frame.pack(fill=tk.X, padx=25, pady=5)

        txt_disk = get_processed_rtl_msg("MISSION", "clean_air")
        tk.Radiobutton(
            storage_frame, text=txt_disk, variable=target_mode_var,
            value="DISK", bg="#0B0C10", fg="#C5C6C7",
            selectcolor="#1F2833", font=("Arial", 9, "bold")
        ).pack(anchor=tk.W, padx=20, pady=4)

        txt_ram = get_processed_rtl_msg("MISSION", "warn_active")
        tk.Radiobutton(
            storage_frame, text=txt_ram, variable=target_mode_var,
            value="RAM", bg="#0B0C10", fg="#45A29E",
            selectcolor="#1F2833", font=("Arial", 9, "bold")
        ).pack(anchor=tk.W, padx=20, pady=4)

        return storage_frame

    def draw_terminal_logging_area(self) -> tk.Text:
        """تشييد صندوق الرصد النصي والـ Scrollbar بتلقيم مدمج غير متضخم"""
        scr_frame = tk.Frame(self.root, bg="#0B0C10")
        scr_frame.pack(padx=25, fill=tk.BOTH, expand=True, pady=5)

        text_area = tk.Text(
            scr_frame, bg="#1E1E1E", fg="#00FF00",
            font=("Courier", 10), bd=2, relief=tk.SUNKEN, height=14
        )
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scr = tk.Scrollbar(scr_frame, command=text_area.yview)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scr.set)

        return text_area

 #!/usr/bin/env python3
"""
File Name: mission_controller.py
Path: /home/kali/AeroCage-XV1.0.1/core/mission_controller.py
Created Date: 2026-05-27
Version: 1.0.2
Description: Isolated Operations Controller Subsystem Engine for AeroCage-X.
 Handles asynchronous processing layout tasks without UI blocks.
"""
import tkinter as tk
class MissionController:
 """
 Tactical Backend Controller for Mission Control GUI.
 Orchestrates live telemetry, silent station dumps, and isolated rollbacks.
 """
 def __init__(self, gui_instance, mission_context: dict):
""" ةيحلاةهجالارفبوقيسلاةلسبطب
وكرحملاةئيهت """
 self.gui = gui_instance
 self.ctx = mission_context
 self.factory = self.gui.factory
 def check_active_remote_processes(self):
]""" سّ % &انلا (ي'مع'ل ة*لعلا [ يرريسلاةار ً ثدحتو رـلا ةنآ """
 telemetry = self.ctx]"mon_engine"[.discover_active_hacks_telemetry()
 if telemetry]"active"[:
 self.gui.is_attack_active = True
 self.gui.root.after(0, lambda: self.gui.btn_fire.config(state=tk.DISABLED))
"]{]'type]'telemetry ]{سّ % &انلا : دص
 ,-. 1ش/ "f = 1p_m
 m_w = f"{m_p1} | PID: {telemetry]'pid'[} | Port: {telemetry]'port'[}"
 self.gui.root.after(0, lambda: self.gui.status_lbl.config(
 text=self.gui.process_mixed_text_safely(m_w), fg="#FF00FF"
 ))
 self.gui.root.after(0, lambda: self.gui.text_area.insert(
 tk.END, "\n] [ Core Alert: Active remote operation detected.\n"
 ))
 def run_async_scan_worker(self):
""" 2علا 4ف'خلا (ملا ء8د67لا ـلا dump station ـلاو assoclist ي ً """
 radio = self.ctx.get("radio")
 ifaces = self.ctx]"mon_engine"[.extract_live_kernel_monitors(radio)
 ssid_lbl = self.ctx]"ap_engine"[.get_live_ssid_name(radio)
 if not ssid_lbl:
 ssid_lbl = self.ctx.get("ap_name")
 if not ifaces:
 self.ctx]"mon_engine"[.execute_hardware_decision_tree(radio)
 ifaces = self.ctx]"mon_engine"[.extract_live_kernel_monitors(radio)
 for iface in ifaces:
 res_dump = self.factory.query_station_dump(iface)
 res_info = self.factory.query_iwinfo_assoclist(iface)
 h_dump = f"\n] dump: {ssid_lbl} | {iface} [\n"
 h_info = f"\n] info: {ssid_lbl} | {iface} [\n"
 self.gui.root.after(0, lambda h=h_dump, r=res_dump:
self.gui.append_text_safely(h + r))
 self.gui.root.after(0, lambda h=h_info, r=res_info:
self.gui.append_text_safely(h + r))
if __name__ == "__main__":
 print("]+[ Core Operations Controller Framework initialized safely.")

#!/usr/bin/env python3
"""
File Name: tunnel_watchdog.py
Path: /home/kali/AeroCage-XV1.0.1/utils/tunnel_watchdog.py
Created Date: 2026-05-26
Version: 1.2.2
Description: Ultimate Reverse SSH Tunnel Watchdog Subsystem for AeroCage-X.
             Enforces thread-safe locked hot reconnections and telemetry cache.
"""

import subprocess
import threading
import time


class TunnelWatchdog:
    """
    Decoupled Subsystem Watchdog Engine.
    Monitors live heartbeat sockets and processes background hot reconnections.
    """

    def __init__(self, mission_context: dict, ssh_factory_instance):
        """تهيئة الحارس وحقن كبسولة السياق التكتيكي والاقتران بمصنع الـ SSH"""
        self.ctx = mission_context
        self.factory = ssh_factory_instance
        self.is_monitoring = False
        self.on_timeout_callback = None

        # [مجمع النبض الموحد المعزول]: كاش محلي صامت لحماية معالج الراوتر البعيد
        self.last_known_alive = True

        # [صمام الخيط الأحادي التمكين]: قفل حركي لمنع انفجار الـ Threads بالخلفية
        self.is_reconnecting = False

    def start_tunnel_monitoring_loop(self, timeout_callback_func):
        """إطلاق خيط الحراسة الخلفي الصامت وتثبيت دالة الإلغاء الطارئة للواجهة"""
        self.on_timeout_callback = timeout_callback_func
        self.is_monitoring = True

        threading.Thread(
            target=self._async_watchdog_worker_loop,
            daemon=True
        ).start()

    def stop_tunnel_monitoring_loop(self):
        """كبح محرك الحراسة وتصفير المؤشرات لتطهير بافر الذاكرة العشوائية"""
        self.is_monitoring = False

    def _execute_background_reconnection(self):
        """[محرك الإنعاش الخارق المعزول]: حفر نفق الـ SSH صامتاً بدون تكرار"""
        # التصفير الكلي للثوابت: القراءة الحية للبورتات المتسلسلة الديناميكية للمهمة
        r_port = int(self.ctx["remote_port"])
        l_port = int(self.ctx["local_port"])

        cmd_tunnel = [
            "sshpass", "-p", "root", "ssh", "-N", "-R",
            f"{r_port}:localhost:{l_port}", f"root@{self.factory.ip}",
            "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/shm/null"
        ]
        try:
            with subprocess.Popen(
                cmd_tunnel, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            ) as proc:
                proc.wait(timeout=1.0)
        except (OSError, ValueError, subprocess.TimeoutExpired):
            pass
        finally:
            # تحرير القفل فور انتهاء المحاولة بسلام للسماح بالدورة التالية عند الحاجة
            self.is_reconnecting = False

    def _async_watchdog_worker_loop(self):
        """المحرك الخلفي الموقوت بالـ 60 ثانية صرامة لمنع اللانهائية وحماية كالي"""
        start_drop_time = None
        print("[🪐 Watchdog] Background heartbeat listener established safely.")

        while self.is_monitoring:
            time.sleep(2)

            is_alive = self.factory.verify_ssh_heartbeat()
            self.last_known_alive = is_alive

            if not is_alive:
                if start_drop_time is None:
                    start_drop_time = time.time()
                    print("[⚠️] Watchdog Sensor: Tunnel drop registered live!")

                elapsed_time = time.time() - start_drop_time

                if not self.is_reconnecting:
                    self.is_reconnecting = True
                    threading.Thread(
                        target=self._execute_background_reconnection,
                        daemon=True
                    ).start()

                if elapsed_time >= 60.0:
                    # اختصار وسحق النص والـ print الصريح نهائياً لمنع الـ line too long
                    print("[🚨 Watchdog] Critical Timeout.")
                    self.is_monitoring = False
                    if self.on_timeout_callback:
                        self.on_timeout_callback()
                    break
            else:
                if start_drop_time is not None:
                    start_drop_time = None
                    print("[🟢 Watchdog] Heartbeat recovered. System stabilized.")


if __name__ == "__main__":
    print("[+] Ultimate Tunnel Watchdog Engine Upgraded 1000%.")
    

#!/usr/bin/env python3
"""
File Name: system_guard.py
Path: /home/kali/AeroCage-XV1.0.1/core/system_guard.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Cyber Security Guard Module for AeroCage-X. Handles privileges,
             input sanitization, and cryptographically secure token generation.
"""

import os
import sys
import shutil
import secrets
import tkinter as tk
from tkinter import messagebox


class SystemGuard:
    """
    Main Security Guard Object.
    Provides static protection mechanisms and system validation pipelines.
    """

    @staticmethod
    def enforce_root_privileges(module_name: str, graphical: bool = False):
        """حارس صلاحيات الـ Root القياسي - يمنع العمليات العمياء ويغلق السكربت فوراً"""
        if os.geteuid() != 0:
            msg = f"[-] خطأ أمني فادح: [{module_name}] يتطلب صلاحيات مدير النظام (sudo)."
            if graphical:
                try:
                    root_err = tk.Tk()
                    root_err.withdraw()
                    err_title = "AeroCage-X | خطأ صلاحيات تكتيكي"
                    err_msg = f"{msg}\n\nيرجى إعادة تشغيل الأداة باستخدام أمر: sudo"
                    messagebox.showerror(err_title, err_msg)
                    root_err.destroy()
                except tk.TclError:
                    # معالجة فشل تشغيل الواجهة الرسومية في بيئات الطرفية الصافية أو SSH
                    print("[-] Graphical environment not available for root warning dialog.")

            print(msg)
            sys.exit(1)

    @staticmethod
    def verify_dependencies(tools: list) -> bool:
        """التحقق العتادي الصارم من توفر أدوات كالي الخارجية قبل إطلاق العمليات"""
        for tool in tools:
            if shutil.which(tool) is None:
                print(f"[-] خطأ نظامي حرج: الأداة '{tool}' مفقودة في بيئة كالي.")
                return False
        return True

    @staticmethod
    def sanitize_input(user_input: str, input_type: str = "alphanumeric") -> str:
        """مطهر المدخلات التكتيكي العتادي - القضاء التام على ثغرات الـ Injection"""
        if not user_input:
            return ""
        user_input = user_input.strip()

        if input_type == "interface":
            # السماح فقط بالأحرف والأرقام ورموز الواجهات القياسية
            return "".join(ch for ch in user_input if ch.isalnum() or ch in "._-")

        if input_type == "bssid":
            # تطهير الماك أدرس تماماً والسماح فقط بصيغ الـ Hex والفواصل
            return "".join(ch for ch in user_input if ch.isalnum() or ch in ":-")

        if input_type == "csv_value":
            # حماية ملفات الـ CSV من التلاعب البرمجي والرموز التنفيذية الخبيثة
            if user_input.startswith(('=', '+', '-', '@')):
                user_input = "'" + user_input
            return "".join(ch for ch in user_input if ch.isalnum() or ch in " ._-@:")

        # الافتراضي: تصفية النصوص العادية لمنع الرموز الغريبة
        return "".join(ch for ch in user_input if ch.isalnum() or ch in " ._-")

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """توليد مفاتيح وتوكنات تشفير عشوائية حصينة سيبرانياً تضمن دقة الأطوال الفردية"""
        # حساب دقيق لعدد البايتات المطلوبة لإنتاج السلسلة النصية بدون نقص منطقي
        num_bytes = (length + 1) // 2
        token = secrets.token_hex(num_bytes)
        return token[:length]


if __name__ == "__main__":
    print("[+] حارس النظام المركزي وخط الدفاع الأول (System Guard) نشط.")
    # اختبار تشغيلي صامت للتحقق من كفاءة فلاتر التطهير والحماية
    assert SystemGuard.sanitize_input("wlan0; rm -rf /", "interface") == "wlan0"
    assert SystemGuard.sanitize_input("=cmd|' /C calc'!A1", "csv_value") == "'cmd /C calc!A1"
    assert len(SystemGuard.generate_secure_token(7)) == 7
    print("[+] نجحت كافة الفحوصات الذاتية التكتيكية للحارس المركزي.")

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
    
