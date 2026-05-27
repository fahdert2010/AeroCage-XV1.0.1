#!/usr/bin/env python3
"""
File Name: db_manager.py
Path: /home/kali/AeroCage-XV1.0.1/core/db_manager.py
Created Date: 2026-05-25
Version: 1.0.9
Description: Centralized SQLite Database Manager Facade Control Node for AeroCage-X.
             Assembles architectural database shards into a single inherited interface.
"""

import sqlite3
import threading
from pathlib import Path

from core.db_targets import DbTargetsComponent
from core.db_loot import DbLootComponent
from core.db_radar import DbRadarComponent
from core.db_intel_shard import DbIntelShardComponent

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "aerocage_core.db"


class DatabaseManager(
    DbTargetsComponent, DbLootComponent, DbRadarComponent, DbIntelShardComponent
):
    """
    Master Database Face Controller.
    Dynamically inherits architectural shards to serve uniform persistence APIs.
    """
    _lock = threading.Lock()

    def __init__(self):
        """تهيئة الجداول السيادية وهيكلة النواة التخزينية الموحدة من الشظايا"""
        super().__init__()
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._initialize_core_tables()

    @staticmethod
    def _get_secure_connection():
        """ميثود محمي لفتح نفق اتصال آمن ومغلق ومحدد الوقت بملف قاعدة البيانات"""
        try:
            conn = sqlite3.connect(str(DB_PATH), timeout=10.0)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"[-] Critical: Failed to open secure database bridge: {e}")
            return None

    def _initialize_core_tables(self):
        """بناء الجداول الكبرى لترسانة الأهداف والغنائم ومؤرخ الرادار مركزياً"""
        query_targets = """
        CREATE TABLE IF NOT EXISTS tactical_targets (
            bssid TEXT PRIMARY KEY,
            essid TEXT,
            channel TEXT,
            power INTEGER,
            status TEXT,
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        query_loot = """
        CREATE TABLE IF NOT EXISTS hijacked_intel_loot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_source TEXT,
            data_category TEXT,
            intercepted_payload TEXT,
            captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        query_radar = """
        CREATE TABLE IF NOT EXISTS radar_history_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_mac TEXT,
            associated_bssid TEXT,
            essid_name TEXT,
            movement_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        query_intel = """
        CREATE TABLE IF NOT EXISTS intel_recon (
            bssid TEXT PRIMARY KEY,
            essid TEXT,
            encryption_type TEXT DEFAULT 'OPEN',
            cipher TEXT DEFAULT 'NONE',
            auth_type TEXT DEFAULT 'NONE',
            recon_notes TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self._lock:
            conn = self._get_secure_connection()
            if conn:
                try:
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute(query_targets)
                        cursor.execute(query_loot)
                        cursor.execute(query_radar)
                        cursor.execute(query_intel)
                    print("[+] Core Database Tables structuralized successfully.")
                except sqlite3.Error as e:
                    print(f"[-] Database Setup Exception: Structural failure: {e}")
                finally:
                    conn.close()


if __name__ == "__main__":
    print("[+] Core Database Master Node facade layout configuration verified.")
    db = DatabaseManager()
