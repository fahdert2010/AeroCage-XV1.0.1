#!/usr/bin/env python3
"""
File Name: test_db.py
Path: /home/kali/AeroCage-XV1.0.1/test_db.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Legacy SQLite Database Connection and Queries Testing Script.
             Fully optimized for standalone structural diagnostics pipelines.
"""

import sqlite3
from pathlib import Path

# ربط وتوجيه المسار تلقائياً ومباشرة نحو ملف قاعدة البيانات الصلب والموحد
DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "aerocage_core.db"


class DatabaseEngine:
    """
    Isolated Test Database Controller Component.
    Manages transient test sockets connections and verifies SQL formatting.
    """

    @staticmethod
    def get_connection():
        """إنشاء اتصال آمن وقراءة المسار من ملف الإعدادات الموحد"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"[-] Database Connection Exception: {e}")
            return None

    @classmethod
    def initialize_database(cls) -> bool:
        """إنشاء الجداول الأساسية للمشروع بشكل آمن ومحمي من الأخطاء التراكبية"""
        # تصحيح الخطأ التركيبي القديم وضبط معيار المفتاح الفريد بشكل معزول وصاف
        query = """
        CREATE TABLE IF NOT EXISTS legacy_test_targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT UNIQUE,
            mac_address TEXT,
            status TEXT DEFAULT 'unknown',
            last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with cls.get_connection() as conn:
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    conn.commit()
                    print("[+] Standalone test database initialized successfully.")
                    return True
                except sqlite3.Error as e:
                    print(f"[-] Database Query Exception inside tables creation: {e}")
        return False

    @classmethod
    def add_target_safe(cls, ip: str, mac: str) -> bool:
        """إدخل بيانات الأهداف بطريقة محمية 100% من ثغرات الـ SQL Injection"""
        query = "INSERT OR IGNORE INTO legacy_test_targets (ip_address, mac_address) VALUES (?, ?)"

        with cls.get_connection() as conn:
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query, (ip, mac))
                    conn.commit()
                    return True
                except sqlite3.Error as e:
                    print(f"[-] Database Exception inside query insertion: {e}")
        return False


if __name__ == "__main__":
    print("[*] Launching standalone database engine diagnostic checks...")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DatabaseEngine.initialize_database()
    DatabaseEngine.add_target_safe("192.168.1.1", "AA:BB:CC:DD:EE:FF")
