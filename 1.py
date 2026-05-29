#!/usr/bin/env python3
"""
File Name: system_guard.py
Version: 1.1.0
Description: System Guard for AeroCage-X.
             Ensures proper privileges and runtime safety checks.
"""

import os
import sys
from core.logger_manager import LoggerManager

class SystemGuard:
    """حارس النظام - مسؤول عن التحقق من الصلاحيات والأمان"""

    @staticmethod
    def enforce_root_privileges() -> None:
        """يتأكد من أن البرنامج يعمل بصلاحيات الجذر"""
        if os.name != "nt":  # تحقق فقط في الأنظمة الشبيهة بـ Unix
            if os.geteuid() != 0:
                LoggerManager.log_error("❌ يجب تشغيل البرنامج بصلاحيات الجذر (sudo).")
                sys.exit("❌ يجب تشغيل البرنامج بصلاحيات الجذر (sudo).")

    @staticmethod
    def check_environment() -> None:
        """يتأكد من أن البيئة مناسبة للتشغيل"""
        logs_path = "/home/kali/AeroCage-XV4.0.0/logs"
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
            LoggerManager.log_info("Logs directory created successfully")
#!/usr/bin/env python3
"""
File Name: event_bus.py
Version: 1.0.0
Description: Event Bus for AeroCage-X.
             Provides a publish-subscribe mechanism for modules to communicate.
"""

from typing import Callable, Dict, List

class EventBus:
    """حافلة الأحداث - تربط الوحدات ببعضها عبر نظام publish/subscribe"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """تسجيل دالة للاستماع لحدث معين"""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """إلغاء الاشتراك من حدث معين"""
        if event_name in self._subscribers:
            self._subscribers[event_name] = [
                cb for cb in self._subscribers[event_name] if cb != callback
            ]

    def publish(self, event_name: str, *args, **kwargs) -> None:
        """نشر حدث لجميع المشتركين"""
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)
#!/usr/bin/env python3
"""
File Name: logger_vault.py
Version: 4.0.0
Description: Logger Vault for AeroCage-X
             Centralized logging configuration.
"""

import logging
import os

def setup_logging(log_dir: str = "/home/kali/AeroCage-XV4.0.0/logs") -> None:
    """تهيئة نظام التسجيل Logging"""
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "aerocage.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.info("LoggerVault: Logging system initialized.")
