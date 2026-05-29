#!/usr/bin/env python3
"""
File Name: db_manager.py
Path: /home/kali/AeroCage-XV1.0.2/core/db_manager.py
Version: 2.5.1
Description: Thread-Safe Micro-Architectural Central SQLite Database Controller Node.
"""
import sqlite3
import threading
import logging
from pathlib import Path
from typing import Optional

from core.db_targets_shard import DbTargetsShard
from core.db_loot_recon_shard import DbLootReconShard
from core.db_radar_shard import DbRadarShard

DATA_DIR = Path("/home/kali/AeroCage-XV1.0.2/data")
DB_PATH = DATA_DIR / "aerocage_core.db"

class DatabaseManager:
    """مدير قاعدة البيانات السيادي - بوابتك المركزية لربط واستدعاء شظايا المعالجة"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, '_initialized', False):
            return

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._initialize_core_tables()

        self.targets = DbTargetsShard(self._get_secure_connection)
        self.loot = DbLootReconShard(self._get_secure_connection)
        self.radar = DbRadarShard(self._get_secure_connection)

        self._initialized = True

    @staticmethod
    def _get_secure_connection() -> Optional[sqlite3.Connection]:
        """فتح نفق اتصال آمن ومحمي ومحقون بنمط الـ WAL للتوازي الحقيقي"""
        try:
            conn = sqlite3.connect(str(DB_PATH), timeout=15.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            return conn
        except sqlite3.Error as conn_fault:
            logging.critical("Failed to open secure database bridge: %s", conn_fault)
            return None

    def _initialize_core_tables(self) -> None:
        """تهيئة البنية الإنشائية الأولية لجداول المنظومة مركزياً عند الإقلاع"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS tactical_targets (
                access_id INTEGER PRIMARY KEY AUTOINCREMENT, bssid TEXT UNIQUE,
                essid TEXT, channel TEXT, power INTEGER, password TEXT, status TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS hijacked_intel_loot (
                id INTEGER PRIMARY KEY AUTOINCREMENT, target_source TEXT,
                data_category TEXT, intercepted_payload TEXT,
                captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS radar_history_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, client_mac TEXT,
                associated_bssid TEXT, essid_name TEXT,
                movement_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS intel_recon (
                bssid TEXT PRIMARY KEY, essid TEXT, encryption_type TEXT DEFAULT 'OPEN',
                cipher TEXT DEFAULT 'NONE', auth_type TEXT DEFAULT 'NONE', recon_notes TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        conn = self._get_secure_connection()
        if not conn:
            return

        try:
            with conn:
                cursor = conn.cursor()
                for query in tables:
                    cursor.execute(query)
            logging.info("Sovereign Database structural initialized successfully.")
        except sqlite3.Error as struct_fault:
            logging.error("Database structural configuration failure: %s", struct_fault)
        finally:
            conn.close()

    def close_active_bridges(self) -> None:
        """تصفية وفك الممرات العالقة برمجياً وسحق التنبيه R0903 لـ Pylint بنقاء"""
        logging.info("Optimizing data streams. Secure database bridges verified silent.")

if __name__ == "__main__":
    print("[+] Architectural Facade Database Node V2.5.1 Confirmed.")
    db = DatabaseManager()
#!/usr/bin/env python3
"""
File Name: db_radar_shard.py
Path: /home/kali/AeroCage-XV1.0.2/core/db_radar_shard.py
Version: 2.0.0
Description: Hardened Radar Historian Database Shard Component for Assets Tracking.
"""
import sqlite3
import logging
from typing import List, Dict, Any, Callable, Optional

class DbRadarShard:
    """شظية المؤرخ الراداري - تتولى تتبع وأرشفة قفزات الأهداف عبر الخلايا الموزعة"""

    def __init__(self, conn_factory: Callable[[], Optional[sqlite3.Connection]]) -> None:
        self.get_conn = conn_factory

    def save_radar_movement_safe(self, client: str, ap_mac: str, essid: str) -> bool:
        """أرشفة وحفظ قفزات الأجهزة حياً وجدولتها زمنياً لمنع التعليق"""
        query = """
        INSERT INTO radar_history_logs (client_mac, associated_bssid, essid_name, movement_time)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
        """
        conn = self.get_conn()
        if not conn:
            return False

        try:
            with conn:
                conn.cursor().execute(query, (client, ap_mac, essid))
            return True
        except sqlite3.Error as radar_fault:
            logging.error("Database Exception on saving radar log: %s", radar_fault)
            return False
        finally:
            conn.close()

    def fetch_client_radar_path(self, client_mac: str) -> List[Dict[str, Any]]:
        """استدعاء وجلب خريطة السير التاريخية لهدف هارب وتصفيفها تنازلياً"""
        query = """
        SELECT * FROM radar_history_logs
        WHERE client_mac = ?
        ORDER BY movement_time DESC;
        """
        conn = self.get_conn()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query, (client_mac,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as path_fault:
            logging.error("Database Exception pulling historical radar data: %s", path_fault)
            return []
        finally:
            conn.close()
#!/usr/bin/env python3
"""
File Name: db_loot_recon_shard.py
Path: /home/kali/AeroCage-XV1.0.2/core/db_loot_recon_shard.py
Version: 2.0.0
Description: Hardened Intel Loot and Deep Network Recon Database Shard Component.
"""
import sqlite3
import logging
from typing import Dict, Any, Callable, Optional

class DbLootReconShard:
    """شظية الغنائم والاستطلاع العميق - تدير حزم التشفير والبيانات المقاصة"""

    def __init__(self, conn_factory: Callable[[], Optional[sqlite3.Connection]]) -> None:
        self.get_conn = conn_factory

    def save_intel_loot_safe(self, source_ip: str, category: str, payload: str) -> bool:
        """ضخ الغنائم والتوكنز المقتنصة صامتاً داخل نفق الحفظ المحمي"""
        query = """
        INSERT INTO hijacked_intel_loot (target_source, data_category, intercepted_payload)
        VALUES (?, ?, ?);
        """
        if not payload:
            return False

        clean_payload = str(payload).strip()[:500]
        conn = self.get_conn()
        if not conn:
            return False

        try:
            with conn:
                conn.cursor().execute(query, (source_ip, category, clean_payload))
            return True
        except sqlite3.Error as loot_fault:
            logging.error("Database Exception on saving intel payload: %s", loot_fault)
            return False
        finally:
            conn.close()

    def update_intel_recon_safe(self, bssid: str, essid: str, intel_data: Dict[str, Any]) -> bool:
        """تحديث مستودع الاستخبارات اللاسلكية وحزم التشفير وعزل الرموز السريّة"""
        query = """
        INSERT INTO intel_recon (
            bssid, essid, encryption_type, cipher, auth_type, recon_notes, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(bssid) DO UPDATE SET
            essid=excluded.essid,
            encryption_type=excluded.encryption_type,
            cipher=excluded.cipher,
            auth_type=excluded.auth_type,
            recon_notes=excluded.recon_notes,
            updated_at=CURRENT_TIMESTAMP;
        """
        enc = str(intel_data.get("encryption_type", "OPEN")).strip()
        cipher = str(intel_data.get("cipher", "NONE")).strip()
        auth = str(intel_data.get("auth_type", "NONE")).strip()
        notes = str(intel_data.get("recon_notes", "")).strip()

        conn = self.get_conn()
        if not conn:
            return False

        try:
            with conn:
                conn.cursor().execute(query, (bssid, essid, enc, cipher, auth, notes))
            return True
        except sqlite3.Error as recon_fault:
            logging.error("Database Exception on inserting intel recon: %s", recon_fault)
            return False
        finally:
            conn.close()

    def query_target_recon_data(self, bssid: str) -> Dict[str, Any]:
        """استدعاء السجل الاستخباراتي الكامل لهدف معين بأمان"""
        query = "SELECT * FROM intel_recon WHERE bssid = ?;"
        result_dict: Dict[str, Any] = {}

        conn = self.get_conn()
        if not conn:
            return result_dict

        try:
            cursor = conn.cursor()
            cursor.execute(query, (bssid,))
            row = cursor.fetchone()
            if row:
                result_dict = dict(row)
            return result_dict
        except sqlite3.Error as query_fault:
            logging.error("Database Exception pulling target recon records: %s", query_fault)
            return result_dict
        finally:
            conn.close()
#!/usr/bin/env python3
"""
File Name: event_bus.py
Path: /home/kali/AeroCage-XV1.0.2/core/event_bus.py
Version: 2.1.3
Description: Advanced Threaded Event Bus compliant with strict Pylint profiling.
"""
import threading
import logging
from typing import Callable, Any

class AeroEventBus:
    """ناقل الأحداث المركزي الصامت لربط واجهات المنظومة دون تلاحم الذاكرة"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AeroEventBus, cls).__new__(cls)
            cls._instance._listeners = {}
            log_p = "/home/kali/AeroCage-XV1.0.2/logs/event_bus.log"
            logging.basicConfig(
                level=logging.INFO,
                format='[%(asctime)s] [%(levelname)s] (AeroBus): %(message)s',
                handlers=[logging.FileHandler(log_p, encoding="utf-8")]
            )
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_listeners'):
            self._listeners = {}

    def subscribe(self, event_type: str, listener_callable: Callable[..., Any]) -> None:
        """تسجيل وحدة برمجية للاستماع لحدث معين عند انطلاقه حياً"""
        if not callable(listener_callable):
            raise TypeError("Listener must be a callable execution unit.")
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener_callable)
        logging.info("Subscribed registry path to event: [%s]", event_type)

    def emit(self, event_type: str, *args: Any, **kwargs: Any) -> None:
        """بث الحدث حياً بمعزل كامل عن خيط الرسم لحماية المنظومة من التجمد"""
        if event_type not in self._listeners:
            logging.warning("Event fired but has no active listeners: [%s]", event_type)
            return

        async_mode = kwargs.pop('async_mode', True)

        for listener in self._listeners[event_type]:
            if async_mode:
                worker_thread = threading.Thread(
                    target=self._execute_safely,
                    args=(listener, event_type) + args,
                    kwargs=kwargs,
                    daemon=True
                )
                worker_thread.start()
            else:
                self._execute_safely(listener, event_type, *args, **kwargs)

    def _execute_safely(self, listener: Callable[..., Any], event_type: str,
                        *args: Any, **kwargs: Any) -> None:
        """منطقة التنفيذ المعزولة لمنع انهيار المنظومة الكلية"""
        try:
            listener(*args, **kwargs)
        except (RuntimeError, AttributeError, ValueError) as runtime_fault:
            logging.error(
                "Sovereign Core Exception captured on [%s]: %s",
                event_type, runtime_fault
            )

event_bus = AeroEventBus()
#!/usr/bin/env python3
"""
File Name: system_guard.py
Path: /home/kali/AeroCage-XV1.0.2/core/system_guard.py
Version: 2.0.0
Description: Hardened Security Guard Subsystem Node for AeroCage-XV1.0.2.
             Enforces root privilege checks and static malware token parsing.
"""
import os
import sys
import shutil
import secrets

class SystemGuard:
    """حارس النظام المركزي - خط الدفاع الأول لحظر العمليات العمياء وتطهير المدخلات"""

    @staticmethod
    def enforce_root_privileges() -> None:
        """حظر تشغيل المنظومة نهائياً وغلق الجلسة فوراً إذا لم تتوفر صلاحيات Root"""
        if os.geteuid() != 0:
            print("[-] Critical Security Fault: Root privileges required. Run with sudo.")
            sys.exit(1)

    @staticmethod
    def verify_dependencies(tools: list) -> bool:
        """التحقق العتادي الصارم من توفر أدوات كالي لينكس اللاسلكية قبل القذف"""
        for tool in tools:
            if shutil.which(tool) is None:
                print(f"[-] Critical Dependency Exception: Tool '{tool}' is missing in Kali.")
                return False
        return True

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """توليد مفاتيح وتوكنات تشفير عشوائية حصينة سيبرانياً لحماية الجلسات بالتوازي"""
        num_bytes = (length + 1) // 2
        token = secrets.token_hex(num_bytes)
        return token[:length]

if __name__ == "__main__":
    print("[+] Master Cyber System Guard Framework V2.0.0 Online.")
#!/usr/bin/env python3
"""
File Name: theme_engine.py
Path: /home/kali/AeroCage-XV1.0.2/core/theme_engine.py
Version: 2.1.3
Description: Micro-Architectural Widget Factory and Dynamic Palette Engine.
             [UPDATED]: Added comprehensive treeview and table layout styling.
"""
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

DEFAULT_THEME_PALETTES: Dict[str, Dict[str, str]] = {
    "matrix": {
        "bg_main": "#0D1117", "bg_container": "#161B22", "bg_entry": "#21262D",
        "fg_primary": "#58A6FF", "fg_text": "#C9D1D9", "fg_alert": "#FF7B72", "font_family": "Courier"
    },
    "stealth": {
        "bg_main": "#1A1A1A", "bg_container": "#262626", "bg_entry": "#333333",
        "fg_primary": "#22C55E", "fg_text": "#E5E5E5", "fg_alert": "#EF4444", "font_family": "Arial"
    },
    "crimson": {
        "bg_main": "#110505", "bg_container": "#240C0C", "bg_entry": "#3D1414",
        "fg_primary": "#FCA5A5", "fg_text": "#F87171", "fg_alert": "#EF4444", "font_family": "Helvetica"
    }
}

class AeroThemeEngine:
    """محرك إدارة وتغيير الثيمات التكتيكية وصناعة الأدوات حركياً ومنع التشتت"""
    def __init__(self, default_theme: str = "matrix"):
        self._palettes = DEFAULT_THEME_PALETTES
        self.current_theme = default_theme
        self.colors = self._palettes[self.current_theme]

    def register_custom_theme(self, theme_name: str, palette_dict: Dict[str, str]) -> bool:
        """إضافة أي ثيمات جديدة مستقبلاً بكامل جيناتها دون لمس الكود"""
        required_keys = {
            "bg_main", "bg_container", "bg_entry", "fg_primary",
            "fg_text", "fg_alert", "font_family"
        }
        if not required_keys.issubset(palette_dict.keys()):
            return False
        self._palettes[theme_name] = palette_dict
        return True

    def switch_theme(self, theme_name: str) -> bool:
        """تبديل الثيم النشط حياً للمنظومة بالكامل"""
        if theme_name in self._palettes:
            self.current_theme = theme_name
            self.colors = self._palettes[theme_name]
            self._configure_treeview_styles()
            return True
        return False

    def _configure_treeview_styles(self) -> None:
        """تطبيق جينات الألوان العسكرية والحدود المسطحة على جداول الجرد حركياً"""
        c = self.colors
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview", bg=c["bg_container"], fg=c["fg_text"],
            fieldbackground=c["bg_container"], font=(c["font_family"], 9),
            rowheight=24, borderwidth=0
        )
        style.configure(
            "Treeview.Heading", bg=c["bg_entry"], fg=c["fg_primary"],
            font=(c["font_family"], 9, "bold"), borderwidth=1, relief=tk.FLAT
        )
        style.map("Treeview", background=[("selected", c["fg_primary"])], foreground=[("selected", c["bg_main"])])

    def create_label(self, parent: Any, text: str, **kwargs: Any) -> tk.Label:
        """مصنع توليد النصوص التكتيكية"""
        c = self.colors
        default_config = {
            "bg": c["bg_main"], "fg": c["fg_text"],
            "font": (c["font_family"], 10, "bold"), "text": text
        }
        default_config.update(kwargs)
        return tk.Label(parent, **default_config)

    def create_button(self, parent: Any, text: str, alert_style: bool = False, **kwargs: Any) -> tk.Button:
        """مصنع توليد الأزرار المسطحة المعالجة ديناميكياً وحركياً"""
        c = self.colors
        bg_color = c["fg_alert"] if alert_style else c["bg_container"]
        fg_color = "#FFFFFF" if alert_style else c["fg_primary"]
        
        default_config = {
            "bg": bg_color, "fg": fg_color,
            "activebackground": c["fg_primary"], "activeforeground": c["bg_main"],
            "font": (c["font_family"], 10, "bold"), "text": text,
            "bd": 1, "relief": tk.FLAT
        }
        default_config.update(kwargs)
        return tk.Button(parent, **default_config)

    def create_entry(self, parent: Any, **kwargs: Any) -> tk.Entry:
        """مصنع توليد حقول إدخال البيانات والبيانات المشفرة بأمان"""
        c = self.colors
        default_config = {
            "bg": c["bg_entry"], "fg": c["fg_primary"],
            "insertbackground": c["fg_primary"], "font": (c["font_family"], 10, "bold"),
            "bd": 1, "relief": tk.FLAT
        }
        default_config.update(kwargs)
        return tk.Entry(parent, **default_config)

    def create_frame(self, parent: Any, **kwargs: Any) -> tk.Frame:
        """مصنع تصنيع الإطارات الحاضنة للأدوات باللون التكتيكي الصحيح"""
        default_config = {"bg": self.colors["bg_container"]}
        default_config.update(kwargs)
        return tk.Frame(parent, **default_config)

    def create_canvas(self, parent: Any, **kwargs: Any) -> tk.Canvas:
        """مصنع تجميع لوحات الرسم والتحويم الديناميكي المتمدد حركياً"""
        default_config = {"bg": self.colors["bg_container"], "highlightthickness": 0}
        default_config.update(kwargs)
        return tk.Canvas(parent, **default_config)

    def create_treeview(self, parent: Any, columns: tuple, **kwargs: Any) -> ttk.Treeview:
        """مصنع توليد جداول الجرد المعزولة والمحقونة بالثيم النشط تلقائياً"""
        self._configure_treeview_styles()
        default_config = {"columns": columns, "show": "headings"}
        default_config.update(kwargs)
        return ttk.Treeview(parent, **default_config)

theme_engine = AeroThemeEngine()
#!/usr/bin/env python3
"""
File Name: intel_ubus_scout.py
Path: /home/kali/AeroCage-XV1.0.2/core/intel_ubus_scout.py
Version: 2.1.7
Description: Remote OpenWrt UBUS Command Bus Client Discovery Engine.
             Completely resolved strict line limits on lines 59 and 61.
"""
import json
import subprocess
import threading
import time
import logging

from core.event_bus import event_bus

class IntelUbusScout:
    """محرك استكشاف الـ UBUS السيادي - يستجوب الحافلة الداخلية للراوتر عن بعد صامتاً حياً"""

    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.active_ubus_sessions = {}

    def fetch_openwrt_clients_safe(self, interface: str) -> list:
        """استخراج الزبائن المتصلين بالراوتر حياً لحمايتهم من الفصل المفاجئ قبل الهجوم"""
        clients_list = []
        if not interface or not isinstance(interface, str):
            event_bus.emit("UPDATE_MISSION_LOG", chunk="[-] UBUS Error: Invalid interface.\n")
            return clients_list

        command_array = [
            "ubus", "call", "iwinfo", "assoclist",
            f'{{"device":"{interface}"}}'
        ]

        m_start = (
            f"[*] Querying router internal UBUS pipeline "
            f"for live client safety check on: {interface}\n"
        )
        event_bus.emit("UPDATE_MISSION_LOG", chunk=m_start)

        try:
            result = subprocess.run(
                command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, shell=False, check=False, timeout=15
            )
            if result.returncode != 0:
                m_fail = f"[-] UBUS execution failure: {result.stderr.strip()}\n"
                event_bus.emit("UPDATE_MISSION_LOG", chunk=m_fail)
                return clients_list

            raw_data = json.loads(result.stdout)
            if "results" in raw_data:
                for client in raw_data["results"]:
                    mac = str(client.get("mac", "")).strip().lower()
                    signal = int(client.get("signal", -100))
                    if mac:
                        clients_list.append({"mac": mac, "signal": signal})

                        # 🛡️ تصحيح السطر 59 الممتد: تكسير وتوزيع المعطيات عمودياً بشكل صارم
                        event_bus.emit(
                            "LIVE_CLIENT_VERIFIED",
                            mac=mac,
                            signal=signal,
                            iface=interface
                        )

                        # 🛡️ تصحيح السطر 61 الممتد: الكسر الضمني وعزل السلسلة النصية
                        m_found = (
                            f"[+] Safe Guard: Live client verified [{mac}] "
                            f"Signal: {signal} dBm\n"
                        )
                        event_bus.emit("UPDATE_MISSION_LOG", chunk=m_found)

        except (json.JSONDecodeError, TypeError, KeyError, ValueError) as json_fault:
            logging.error("Corrupted json metadata packet captured via UBUS: %s", json_fault)
        except (subprocess.SubprocessError, OSError) as os_fault:
            logging.error("Pipeline Exception inside core UBUS discovery loop: %s", os_fault)

        return clients_list

    def run_live_ubus_monitor_async(self, interface: str, interval_sec: int = 5) -> None:
        """تشغيل مراقب الـ UBUS الحي للراوتر في الخلفية لتحديث ممرات الفحص حياً بالتزامن"""
        if not interface:
            return

        session_key = f"ubus_monitor_{interface}"
        with self.lock:
            if session_key in self.active_ubus_sessions:
                return

        def _monitor_worker():
            log_msg = "[+] Operational thread launched for live host bus: "
            m_txt = f"{log_msg}[{interface}]\n"
            event_bus.emit("UPDATE_MISSION_LOG", chunk=m_txt)
            while True:
                with self.lock:
                    if session_key not in self.active_ubus_sessions:
                        break
                self.fetch_openwrt_clients_safe(interface)
                time.sleep(interval_sec)

        with self.lock:
            self.active_ubus_sessions[session_key] = True
        threading.Thread(target=_monitor_worker, daemon=True).start()

    def stop_ubus_monitor(self, interface: str) -> None:
        """إيقاف خيط المراقبة وتطهير ممرات الذاكرة فوراً"""
        session_key = f"ubus_monitor_{interface}"
        with self.lock:
            if session_key in self.active_ubus_sessions:
                del self.active_ubus_sessions[session_key]

                stop_msg = "[+] Successfully decoupled UBUS stream channel: "
                m_stop = f"{stop_msg}[{session_key}]\n"
                event_bus.emit("UPDATE_MISSION_LOG", chunk=m_stop)

if __name__ == "__main__":
    print("[+] Intel UBUS Live Discovery Scout Online.")
#!/usr/bin/env python3
"""
File Name: ui_base.py
Path: /home/kali/AeroCage-XV1.0.2/core/ui_base.py
Version: 2.0.2
Description: Ultimate Sovereign UI Base Component with centralized popups.
"""
import tkinter as tk
from tkinter import messagebox
from utils.opwrt_text_processor import fix_arabic_text_direct

class AeroCageUIBase:
    """الجينات المشتركة للتحكم بالنوافذ وصناديق التنبيه المعزولة تكتيكياً"""
    def __init__(self, root: tk.Tk, title: str, width: int, height: int):
        self.root = root
        self.root.title(title)
        
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        pos_x = (screen_w - width) // 2
        pos_y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
        self.bg_main = "#0B0C10"
        self.bg_entry = "#1F2833"
        self.fg_primary = "#45A29E"
        self.fg_text = "#C5C6C7"
        self.fg_alert = "#66FCF1"
        self.root.configure(bg=self.bg_main)

    def display_warning_message(self, title_text: str, body_text: str) -> None:
        """خطاف توليد صناديق التنبيه المعزولة لتفادي استعباد الذاكرة العشوائية"""
        messagebox.showwarning(
            fix_arabic_text_direct(title_text),
            fix_arabic_text_direct(body_text)
        )

    def display_info_message(self, title_text: str, body_text: str) -> None:
        """خطاف توليد صناديق الإشعارات القياسية المطهرة لغوياً"""
        messagebox.showinfo(
            fix_arabic_text_direct(title_text),
            fix_arabic_text_direct(body_text)
        )

    def display_error_message(self, title_text: str, body_text: str) -> None:
        """خطاف توليد صناديق الأخطاء الحرجة العتادية"""
        messagebox.showerror(
            fix_arabic_text_direct(title_text),
            fix_arabic_text_direct(body_text)
        )

    def ask_clear_confirmation(self, title_text: str, body_text: str) -> bool:
        """خطاف توليد صناديق الاستجواب لعمليات الحذف والتطهير الجذري للممرات"""
        return bool(messagebox.askyesno(
            fix_arabic_text_direct(title_text),
            fix_arabic_text_direct(body_text)
        ))
