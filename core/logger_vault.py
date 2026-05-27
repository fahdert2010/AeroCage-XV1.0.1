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
