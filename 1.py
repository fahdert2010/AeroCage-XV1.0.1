#!/usr/bin/env python3
"""
File Name: plugin_loader.py
Version: 1.1.0
Description: Plugin Loader for AeroCage-X.
             Handles dynamic loading and launching of plugins.
"""

import tkinter as tk
from utils.error_messenger import ErrorMessenger
from core.event_bus import EventBus
from core.logger_manager import LoggerManager

class PluginLoader:
    """مدير الإضافات - مسؤول عن تحميل وتشغيل الإضافات"""

    def __init__(self, root: tk.Tk, event_bus: EventBus):
        self.root = root
        self.event_bus = event_bus
        self.plugins = {}

    def register_plugin(self, name: str, plugin_class) -> None:
        """تسجيل إضافة جديدة"""
        try:
            self.plugins[name] = plugin_class
            LoggerManager.log_info(f"Plugin {name} registered successfully")
            self.event_bus.publish("plugin_registered", name)
        except (KeyError, TypeError) as err:
            LoggerManager.log_error(f"Failed to register plugin {name}. Error: {err}")
            ErrorMessenger.show_error(f"فشل تسجيل الإضافة: {name}")

    def launch_plugin(self, plugin_class) -> None:
        """تشغيل إضافة معينة"""
        if not plugin_class:
            ErrorMessenger.show_warning("⚠️ الإضافة غير موجودة")
            return
        try:
            plugin_instance = plugin_class(self.root)
            plugin_instance.run()
            LoggerManager.log_info("Plugin launched successfully")
            self.event_bus.publish("plugin_launched", plugin_class.__name__)
        except (RuntimeError, TypeError) as err:
            LoggerManager.log_error(f"Failed to launch plugin. Error: {err}")
            ErrorMessenger.show_error("❌ فشل تشغيل الإضافة")

    def open_plugin_manager(self) -> None:
        """فتح نافذة إدارة الإضافات"""
        manager_win = tk.Toplevel(self.root)
        manager_win.title("🔌 إدارة الإضافات")
        manager_win.geometry("400x300")

        for name in self.plugins.keys():
            tk.Label(manager_win, text=name).pack()

#!/usr/bin/env python3
"""
File Name: theme_plugin.py
Version: 1.0.0
Description: Theme Plugin for AeroCage-X.
             Provides theme customization (colors, fonts).
"""

import tkinter as tk
from core.logger_manager import LoggerManager

class ThemePlugin:
    """إضافة الثيمات - لتغيير الألوان والخطوط"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_theme = {
            "background": "#1e1e1e",
            "foreground": "white",
            "font_small": ("Arial", 10),
            "font_medium": ("Arial", 12, "bold"),
            "font_large": ("Courier", 14, "bold")
        }

    def run(self) -> None:
        """تشغيل واجهة إدارة الثيمات"""
        win = tk.Toplevel(self.root)
        win.title("🎨 Theme Manager")
        win.geometry("400x300")
        tk.Label(win, text="اختر ثيم جديد", font=self.current_theme["font_medium"]).pack(pady=10)
        LoggerManager.log_info("Theme Plugin opened")

    def get_color(self, key: str) -> str:
        return self.current_theme.get(key, "white")

    def get_font(self, key: str) -> tuple:
        return self.current_theme.get(f"font_{key}", ("Arial", 10))

#!/usr/bin/env python3
"""
File Name: language_processor.py
Version: 1.4.0
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

    def translate(self, key: str, raw: bool = False) -> str:
        """إرجاع النص المناسب حسب اللغة"""
        text = self.translations.get(self.current_lang, {}).get(key, key)
        if raw:
            return text
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
File Name: ui_layout_builder.py
Version: 1.1.0
Description: UI Layout Builder for AeroCage-X.
"""

import tkinter as tk
from core.logger_manager import LoggerManager

class UILayoutBuilder:
    """منشئ الواجهة - يبني القوائم والأزرار"""

    def __init__(self, root: tk.Tk, plugin_loader):
        self.root = root
        self.plugin_loader = plugin_loader

    def build_main_menu(self) -> None:
        """بناء الواجهة الرئيسية"""
        lbl_title = tk.Label(
            self.root,
            text="⚡ AeroCage-X Unified Launcher ⚡",
            font=("Courier", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        lbl_title.pack(pady=20)

        btn_plugins = tk.Button(
            self.root,
            text="🔌 إدارة الإضافات (Plugins)",
            command=self.plugin_loader.open_plugin_manager
        )
        btn_plugins.pack(pady=10, fill=tk.X, padx=50)

        btn_exit = tk.Button(
            self.root,
            text="❌ إنهاء النظام",
            command=self.root.quit
        )
        btn_exit.pack(pady=10, fill=tk.X, padx=50)

        # إضافة شريط الحالة
        lbl_status = tk.Label(
            self.root,
            text="📥 النظام جاهز للعمل...",
            bd=1,
            relief=tk.SUNKEN,
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

        LoggerManager.log_info("Main UI built successfully")
