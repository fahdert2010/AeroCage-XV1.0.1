"""
File Name: config.py
Path: /home/kali/AeroCage-XV1.0.1/config.py
Created Date: 2026-05-25
Version: 1.0.1
Description: AeroCage-X Configuration Module. Handles dynamic path resolution 
             and secure environment variable parsing using pure OOP.
"""

import os
from pathlib import Path

class Config:
    """
    Main Configuration Object.
    Encapsulates core variables and custom .env parsing logic.
    """
    VERSION = "1.0.1"
    APP_NAME = "AeroCage-X"

    BASE_DIR = Path(__file__).resolve().parent
    LOG_DIR = BASE_DIR / "logs"
    DATA_DIR = BASE_DIR / "data"
    ENV_FILE = BASE_DIR / ".env"

    def __init__(self):
        """تهيئة الكائن وتحميل متغيرات البيئة محلياً"""
        self.env_data = {}
        self._load_custom_env()

    def _load_custom_env(self):
        """قراءة ملف .env يدوياً بكفاءة لتفادي الحزم الخارجية مع معالجة حرج المتغيرات"""
        if not self.ENV_FILE.exists():
            return

        current_line = 0
        try:
            with open(self.ENV_FILE, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    current_line = line_num
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        key, value = line.split('=', 1)
                        self.env_data[key.strip()] = value.strip()
        except (IOError, OSError) as e:
            # استخدام current_line يضمن وجود قيمة عددية دائماً حتى لو فشل الفتح
            print(f"[-] Critical: Failed to read .env file at line {current_line}. Error: {e}")

    def get(self, key, default=None):
        """جلب آمن للمتغيرات مع معالجة حظر الأخطاء (KeyError)"""
        return self.env_data.get(key, os.getenv(key, default))

    @classmethod
    def initialize_system(cls):
        """إنشاء مجلدات النظام مع معالجة الصلاحيات (PermissionError)"""
        try:
            cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
            cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            print(f"[-] Critical: Write permission denied on system directories. Error: {e}")
            raise e
