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

