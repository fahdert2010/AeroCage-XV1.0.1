سارسل لك ملف احدث ايضا الان واخبرني رايك 
#!/usr/bin/env python3
"""
File Name: launcher.py
Version: 4.3.0
Description: AeroCage-X Unified Launcher.
"""

import tkinter as tk
from core.system_guard import SystemGuard
from core.event_bus import EventBus
from core.logger_manager import LoggerManager
from modules.plugin_loader import PluginLoader
from modules.targets_manager import TargetsManager
from utils.ui_layout_builder import UILayoutBuilder
from utils.language_processor import LanguageProcessor

class AeroCageLauncher:
    """اللانشر الرئيسي لنظام AeroCage-X"""

    def __init__(self, root: tk.Tk):
        """تهيئة اللانشر"""
        self.root = root
        self.root.geometry("700x650")

        # تهيئة اللوج
        LoggerManager.setup_logger()

        # حارس النظام
        SystemGuard.enforce_root_privileges()
        SystemGuard.check_environment()

        # حافلة الأحداث
        self.event_bus = EventBus()

        # مدير الأهداف
        self.targets_manager = TargetsManager(self.event_bus)

        # مدير الإضافات
        self.plugin_loader = PluginLoader(self.root, self.event_bus)

        # معالج اللغة
        self.lang_proc = LanguageProcessor(default_lang="ar")

        # ضبط عنوان النافذة
        self.root.title(self.lang_proc.translate("title"))

        # منشئ الواجهة
        self.ui_builder = UILayoutBuilder(self.root, self.plugin_loader)
        self.ui_builder.build_main_menu()

    def run(self) -> None:
        """تشغيل الواجهة الرئيسية"""
        LoggerManager.log_info("🚀 AeroCage-X Launcher started successfully")
        self.root.mainloop()


def main():
    """نقطة الدخول الرئيسية"""
    root = tk.Tk()
    app = AeroCageLauncher(root)
    app.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
File Name: language_processor.py
Version: 1.3.0
Description: Centralized Language Processor for AeroCage-X.
             Handles RTL shaping for Arabic and translation registry.
"""

import arabic_reshaper
from bidi.algorithm import get_display

class LanguageProcessor:
    """معالج اللغة المركزي - إصلاح النصوص العربية وإدارة الترجمة"""

    def __init__(self, default_lang: str = "ar"):
        self.current_lang = default_lang
        self.translations = {
            "ar": {
                "title": "⚡ AeroCage‑X: الواجهة الموحدة ⚡",
                "plugins": "🔌 إدارة الإضافات",
                "exit": "❌ إنهاء النظام",
                "tools": "🛠️ أدوات",
                "help": "❓ مساعدة",
                "about": "ℹ️ حول AeroCage‑X",
                "about_msg": "AeroCage‑X v4.0.0\nواجهة حديثة لإدارة النظام"
            },
            "en": {
                "title": "⚡ AeroCage‑X Unified Launcher ⚡",
                "plugins": "🔌 Plugin Manager",
                "exit": "❌ Exit",
                "tools": "🛠️ Tools",
                "help": "❓ Help",
                "about": "ℹ️ About AeroCage‑X",
                "about_msg": "AeroCage‑X v4.0.0\nModern interface for system management"
            }
        }

    def set_language(self, lang: str) -> None:
        """تغيير اللغة الحالية"""
        if lang in self.translations:
            self.current_lang = lang

    def translate(self, key: str) -> str:
        """إرجاع النص المناسب حسب اللغة"""
        text = self.translations.get(self.current_lang, {}).get(key, key)
        return self.process_rtl(text)

    @staticmethod
    def process_rtl(raw_text: str) -> str:
        """إصلاح النصوص العربية لتظهر بشكل صحيح"""
        if not raw_text or not isinstance(raw_text, str):
            return ""

        # إذا كان النص كلمة واحدة أو قصير جدًا، نعرضه كما هو
        if len(raw_text.split()) == 1 or len(raw_text) <= 5:
            return raw_text

        try:
            if not any(0x0600 <= ord(char) <= 0x06FF for char in raw_text):
                return raw_text
            reshaped = arabic_reshaper.reshape(raw_text)
            return get_display(reshaped)
        except (ValueError, TypeError):
            return raw_text

#!/usr/bin/env python3
"""
File Name: theme_manager.py
Version: 1.0.0
Description: Theme and Font Manager for AeroCage-X.
             Centralizes colors, fonts, and sizes for consistent UI design.
"""

class ThemeManager:
    """مدير الثيمات والخطوط - مسؤول عن المظهر العام"""

    def __init__(self):
        # الألوان الأساسية
        self.colors = {
            "background": "#1e1e1e",
            "foreground": "#ffffff",
            "highlight": "#007acc",
            "error": "#ff3333"
        }

        # الخطوط الأساسية
        self.fonts = {
            "small": ("Arial", 10),
            "medium": ("Arial", 12),
            "large": ("Arial", 14, "bold")
        }

    def get_color(self, key: str) -> str:
        """إرجاع اللون المطلوب"""
        return self.colors.get(key, "#000000")

    def get_font(self, size: str = "medium"):
        """إرجاع الخط المطلوب"""
        return self.fonts.get(size, ("Arial", 12))

#!/usr/bin/env python3
"""
File Name: ui_layout_builder.py
Version: 1.0.0
Description: UI Layout Builder for AeroCage-X.
             Responsible for constructing menus, buttons, and interface layout.
"""

import tkinter as tk
from utils.language_processor import LanguageProcessor
from utils.theme_manager import ThemeManager
from utils.error_messenger import ErrorMessenger

class UILayoutBuilder:
    """منشئ الواجهة - مسؤول عن بناء القوائم والأزرار"""
    def __init__(self, root: tk.Tk, plugin_loader):
        self.root = root
        self.plugin_loader = plugin_loader
        self.lang_proc = LanguageProcessor(default_lang="ar")
        self.theme = ThemeManager()
    def build_main_menu(self) -> None:
        """بناء شريط القوائم الرئيسي"""
        menubar = tk.Menu(self.root, font=self.theme.get_font("medium"))

        # قائمة ملف
        file_menu = tk.Menu(menubar, tearoff=0, font=self.theme.get_font("medium"))
        file_menu.add_command(label=self.lang_proc.translate("plugins"),
                              command=self.plugin_loader.open_plugin_manager)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang_proc.translate("exit"),
                              command=self.root.quit)
        menubar.add_cascade(label=self.lang_proc.translate("plugins"), menu=file_menu)
        # قائمة أدوات
        tools_menu = tk.Menu(menubar, tearoff=0, font=self.theme.get_font("medium"))
        tools_menu.add_command(label="⚡ Strike GUI",
                               command=lambda: self.plugin_loader.launch_plugin(
                                   self.plugin_loader.plugins.get("Strike GUI")))
        tools_menu.add_command(label="🛰️ Mission Control",
                               command=lambda: self.plugin_loader.launch_plugin(
                                   self.plugin_loader.plugins.get("Mission Control")))
        menubar.add_cascade(label=self.lang_proc.translate("tools"), menu=tools_menu)
        # قائمة مساعدة
        help_menu = tk.Menu(menubar, tearoff=0, font=self.theme.get_font("medium"))
        help_menu.add_command(label=self.lang_proc.translate("about"),
                              command=lambda: ErrorMessenger.show_info(
                                  self.lang_proc.translate("about_msg"),
                                  self.lang_proc.translate("about")))
        menubar.add_cascade(label=self.lang_proc.translate("help"), menu=help_menu)

        # قائمة اللغة
        lang_menu = tk.Menu(menubar, tearoff=0, font=self.theme.get_font("medium"))
        lang_menu.add_command(label="🇸🇦 عربي", command=lambda: self.set_language("ar"))
        lang_menu.add_command(label="🇬🇧 English", command=lambda: self.set_language("en"))
        menubar.add_cascade(label="🌐 Language", menu=lang_menu)
        self.root.config(menu=menubar)
    def set_language(self, lang: str) -> None:
        """تغيير اللغة وإعادة بناء القوائم"""
        self.lang_proc.set_language(lang)
        self.build_main_menu()
#!/usr/bin/env python3
"""
File Name: error_messenger.py
Version: 1.1.0
Description: Centralized Error Messenger for AeroCage-X.
             Provides unified methods to show error, warning, and info messages.
"""
import tkinter as tk
from tkinter import messagebox
class ErrorMessenger:
    """مدير رسائل الأخطاء - عرض موحد للرسائل"""
    @staticmethod
    def show_error(message: str, title: str = "خطأ") -> None:
        """عرض رسالة خطأ (بدون إعادة تشكيل النصوص العربية)"""
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(message: str, title: str = "تحذير") -> None:
        """عرض رسالة تحذير"""
        messagebox.showwarning(title, message)
    @staticmethod
    def show_info(message: str, title: str = "معلومة") -> None:
        """عرض رسالة معلومات"""
        messagebox.showinfo(title, message)
#!/usr/bin/env python3
"""
File Name: logger_manager.py
Version: 1.0.0
Description: Centralized Logger Manager for AeroCage-X.
             Provides unified logging configuration and helper methods.
"""
import logging
class LoggerManager:
    """مدير التسجيل - مسؤول عن إعدادات اللوج وعرض الرسائل"""

    @staticmethod
    def setup_logger(level: int = logging.INFO) -> None:
        """تهيئة إعدادات اللوج"""
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        logging.info("✅ Logger initialized successfully")
    @staticmethod
    def log_info(message: str) -> None:
        """تسجيل رسالة معلومات"""
        logging.info(message)

    @staticmethod
    def log_warning(message: str) -> None:
        """تسجيل رسالة تحذير"""
        logging.warning(message)

    @staticmethod
    def log_error(message: str) -> None:
        """تسجيل رسالة خطأ"""
        logging.error(message)
from core.logger_manager import LoggerManager

def set_language(self, lang: str) -> None:
    """تغيير اللغة وإعادة بناء القوائم"""
    self.lang_proc.set_language(lang)
    LoggerManager.log_info(f"Language changed to {lang}")
    self.build_main_menu()
2. عند فتح نافذة إدارة الإضافات في plugin_loader.py
def open_plugin_manager(self) -> None:
    """فتح نافذة إدارة الإضافات"""
    manager_win = tk.Toplevel(self.root)
    manager_win.title("🔌 إدارة الإضافات")
    manager_win.geometry("400x300")
    for name in self.plugins.keys():
        tk.Label(manager_win, text=name).pack()
    LoggerManager.log_info("Plugin Manager window opened")
