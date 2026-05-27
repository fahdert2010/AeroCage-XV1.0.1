#!/usr/bin/env python3
"""
File Name: db_radar.py
Path: /home/kali/AeroCage-XV1.0.1/core/db_radar.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Isolated Database Subcomponent for Tracking Assets Movement Path.
"""

import sqlite3
import threading


class DbRadarComponent:
    """
    Radar Historian Database Shard Component.
    Tracks live client jumping vectors across concurrent network cells.
    """
    _lock: threading.Lock
    _get_secure_connection: callable

    def save_radar_movement_safe(self, client: str, ap_mac: str, essid: str) -> bool:
        """ضخ وأرشفة الحركة الرادارية وحصاد قفزات الأجهزة حياً بأمان خيطي"""
        query = """
        INSERT INTO radar_history_logs (client_mac, associated_bssid, essid_name, movement_time)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP);
        """
        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return False
            try:
                with conn:
                    conn.cursor().execute(query, (client, ap_mac, essid))
                return True
            except sqlite3.Error as e:
                print(f"[-] Database Exception on saving radar log: {e}")
                return False
            finally:
                conn.close()

    def fetch_client_radar_path(self, client_mac: str) -> list:
        """استدعاء وجلب خريطة السير التاريخية وجدول القفزات لهدف هارب"""
        query = "SELECT * FROM radar_history_logs WHERE client_mac = ? ORDER BY movement_time DESC;"
        with self._lock:
            conn = self._get_secure_connection()
            if not conn:
                return []
            try:
                cursor = conn.cursor()
                cursor.execute(query, (client_mac,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            except sqlite3.Error as e:
                print(f"[-] Database Exception pulling historical radar data: {e}")
                return []
            finally:
                conn.close()


if __name__ == "__main__":
    print("[+] Database radar historian sharding component verified.")
