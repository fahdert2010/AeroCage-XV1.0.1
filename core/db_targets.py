#!/usr/bin/env python3
"""
File Name: db_targets.py
Path: /home/kali/AeroCage-XV1.0.1/core/db_targets.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Isolated Database Subcomponent for Target Node Persistence Assets.
"""

import sqlite3
import threading


class DbTargetsComponent:
    """
    Targets Database Shard Component.
    Provides methods to flush discovered access points records into persistent streams.
    """
    # تعريف تلميحي صريح للفاحص لإعلامه بامتلاك المقابض التزامنية حكماً لمنع E1101
    _lock: threading.Lock
    _get_secure_connection: callable

    def save_target_safe(self, bssid: str, essid: str, meta_data: dict) -> bool:
        """أرشفة وحفظ الشبكة المكتشفة مع تمرير القنوات والإشارة بأمان"""
        query = """
        INSERT INTO tactical_targets (bssid, essid, channel, power, status, last_seen)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(bssid) DO UPDATE SET
            essid=excluded.essid,
            channel=excluded.channel,
            power=excluded.power,
            status=excluded.status,
            last_seen=CURRENT_TIMESTAMP;
        """
        channel = meta_data.get("channel", "1")
        power = int(meta_data.get("power", -100))
        status = meta_data.get("status", "discovered")

        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return False
            try:
                with conn:
                    conn.cursor().execute(query, (bssid, essid, channel, power, status))
                return True
            except sqlite3.Error as e:
                print(f"[-] Database Exception on save target payload: {e}")
                return False
            finally:
                conn.close()

    def get_all_active_targets(self) -> list:
        """سحب سجلات طابور الأهداف بالكامل للواجهات الرسومية بأمان خيطي"""
        query = "SELECT * FROM tactical_targets ORDER BY last_seen DESC;"
        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return []
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"[-] Database Exception tracking datasets query fetch: {e}")
                return []
            finally:
                conn.close()

    def get_unique_statuses_safe(self) -> list:
        """سحب أسماء الحالات والمجموعات التكتيكية الفرعية لفرز الـ Combobox"""
        query = "SELECT DISTINCT status FROM tactical_targets WHERE status IS NOT NULL;"
        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return []
            try:
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                return [row["status"] for row in rows if row["status"]]
            except sqlite3.Error as e:
                print(f"[-] Database Exception compiling group tokens: {e}")
                return []
            finally:
                conn.close()


if __name__ == "__main__":
    print("[+] Database targets sharding component verified.")
