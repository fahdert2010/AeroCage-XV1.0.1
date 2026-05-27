#!/usr/bin/env python3
"""
File Name: opwrt_storage_engine.py
Path: /home/kali/AeroCage-XV1.0.1/utils/opwrt_storage_engine.py
Created Date: 2026-05-26
Version: 1.3.2
Description: Advanced RAM Disk and Storage Subsystem Engine for AeroCage-X.
             Enforces non-blocking sovereign mounting and asynchronous cleanup.
"""

import os
import subprocess


class OpWrtStorageEngine:
    """
    Sovereign Virtual Memory and Dispatched Hard-Drive File Router.
    Controls dynamic isolated disk allocation loops for concurrent strikes.
    """

    def __init__(self, mission_context: dict, base_project_dir: str):
        """تهيئة الكلاس وحقن السياق التكتيكي والمسار السيادي الأعلى رتبة"""
        self.ctx = mission_context
        self.base_dir = base_project_dir
        self.ap_name = self.ctx["ap_name"]
        self.band = self.ctx["band"]
        self.chan = self.ctx["channel"]

    def resolve_target_logging_path(self, mode: str) -> tuple:
        """توليد مسارات الحفظ حياً بناءً على النمط المختار دون مسارات ثابتة"""
        if mode == "RAM":
            path = f"/dev/shm/AeroCage-X/{self.ap_name}/{self.band}/CH_{self.chan}/"
            msg = "🧠 حظر الهارد! جاري الكتابة داخل الـ RAM Disk بسرعة الخارق..."
        else:
            base = self.base_dir
            path = os.path.join(base, "data", self.ap_name, self.band, f"CH_{self.chan}")
            path = os.path.normpath(path) + "/"
            msg = "📂 جاري قذف الحزم وكتابة سجلات الـ CSV القياسية على الهارد..."

        return path, msg

    def _is_path_mounted(self, target_path: str) -> bool:
        """دالة مدمجة صامتة لمنع تكرار وتشابه دوال استعلام الـ Mount داخل النواة"""
        try:
            with open("/proc/mounts", "r", encoding="utf-8") as f_mounts:
                return target_path in f_mounts.read()
        except (OSError, ValueError):
            return False

    def provision_storage_environment(self, mode: str) -> bool:
        """... تهيئة وإنشاء الـ RAM Disk غير المتزامن وسحق التداخلات الفيزيائية"""
        target_path, _ = self.resolve_target_logging_path(mode)

        try:
            os.makedirs(target_path, exist_ok=True)
            if mode == "RAM":
                # استدعاء الدالة المدمجة الموحدة لمنع التكرار العملياتي العبثي
                if self._is_path_mounted(target_path):
                    return True

                opts = "size=2M"
                cmd_mount = ["mount", "-t", "tmpfs", "-o", opts, "tmpfs", target_path]

                # ربط وإغلاق بافر الـ Popen بقنوات معزولة وسحق مخالفة الـ R1732 نهائياً
                with subprocess.Popen(
                    cmd_mount, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                ) as proc:
                    proc.wait(timeout=1.0)
            return True
        except (OSError, ValueError, subprocess.TimeoutExpired):
            return False

    def cleanup_storage_environment(self, mode: str) -> bool:
        """[محرك الكنس والتطهير]: فك الارتباط قسرياً وتحرير الرام بالملي فور الخروج"""
        target_path, _ = self.resolve_target_logging_path(mode)

        try:
            if mode == "RAM" and self._is_path_mounted(target_path):
                cmd_unmount = ["umount", "-f", target_path]
                subprocess.run(
                    cmd_unmount, check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )

            if os.path.exists(target_path):
                subprocess.run(
                    ["rm", "-rf", target_path], check=False,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
            return True
        except (OSError, ValueError):
            return False


if __name__ == "__main__":
    TEST_CTX = {"ap_name": "Fahd_Net", "band": "2G", "channel": "6"}
    TEST_BASE = "/home/kali/AeroCage-XV1.0.1"

    ENGINE_INSTANCE = OpWrtStorageEngine(TEST_CTX, TEST_BASE)
    P_ROUTE, M_LOG = ENGINE_INSTANCE.resolve_target_logging_path("DISK")
    print(f"[+] Storage Engine Framework Consolidated. Route: {P_ROUTE}")
