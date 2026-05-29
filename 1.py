#!/usr/bin/env python3
"""
File Name: launcher.py
Version: 4.0.0
Description: AeroCage-X Unified Launcher
             Stable entry point with modular plugin support.
"""

import tkinter as tk
import logging
from tkinter import messagebox   # ← أضف هذا السطر

from core.event_bus import EventBus
from core.system_guard import SystemGuard
from core.logger_vault import setup_logging
from modules.plugin_loader import PluginLoader

class AeroCageLauncher:
    """واجهة الإقلاع الرئيسية - نقطة الدخول المستقرة للنظام"""


    def __init__(self, root: tk.Tk) -> None:
        # إعداد نظام التسجيل Logging
        setup_logging()
        logging.info("Initializing AeroCage-X Launcher...")

        # التحقق من الصلاحيات
        try:
            SystemGuard.enforce_root_privileges()
        except PermissionError as e:
            logging.error(f"صلاحيات غير كافية: {e}")
            messagebox.showerror("خطأ", "يجب تشغيل النظام بصلاحيات Root")
            root.destroy()
            return

        self.root = root
        self.root.title("AeroCage-X v4.0.0 | Unified Launcher")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")

        # إنشاء شريط القوائم
        menubar = tk.Menu(self.root)

        # قائمة "ملف"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="🔌 إدارة الإضافات", command=self.plugin_loader.open_plugin_manager)
        file_menu.add_separator()
        file_menu.add_command(label="❌ إنهاء", command=self.root.quit)
        menubar.add_cascade(label="📂 ملف", menu=file_menu)

        # قائمة "أدوات"
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="⚡ تشغيل ضربة تجريبية", command=lambda: self.plugin_loader.launch_plugin(self.plugin_loader.plugins["Strike GUI"]))
        tools_menu.add_command(label="🛰️ فتح التحكم بالمهام", command=lambda: self.plugin_loader.launch_plugin(self.plugin_loader.plugins["Mission Control"]))
        menubar.add_cascade(label="🛠️ أدوات", menu=tools_menu)
        # قائمة "اللغة"
        lang_menu = tk.Menu(menubar, tearoff=0)
        lang_menu.add_command(label="🇸🇦 عربي", command=lambda: self.set_language("ar"))
        lang_menu.add_command(label="🇬🇧 English", command=lambda: self.set_language("en"))
        menubar.add_cascade(label="🌐 اللغة / Language", menu=lang_menu)

        # قائمة "مساعدة"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="ℹ️ حول AeroCage-X", command=lambda: messagebox.showinfo("حول", "AeroCage-X v4.0.0\nواجهة حديثة لإدارة النظام"))
        menubar.add_cascade(label="❓ مساعدة", menu=help_menu)


        # ربط شريط القوائم بالنافذة
        self.root.config(menu=menubar)

        # تهيئة نظام الأحداث
        self.event_bus = EventBus()

        # تحميل الإضافات (Plugins)
        self.plugin_loader = PluginLoader(self.root, self.event_bus)

        # بناء الواجهة
        self.build_main_ui()

    def set_language(self, lang: str) -> None:
        """تغيير لغة الواجهة"""
        self.language = lang
        if lang == "ar":
            messagebox.showinfo("اللغة", "تم تغيير اللغة إلى العربية.")
        else:
            messagebox.showinfo("Language", "Interface language switched to English.")
        # هنا ممكن نضيف لاحقًا تحديث النصوص في الأزرار والقوائم حسب اللغة

    def build_main_ui(self) -> None:
        """بناء واجهة الإقلاع الرئيسية"""
        lbl_title = tk.Label(
            self.root,
            text="⚡ AeroCage-X Unified Launcher ⚡",
            font=("Courier", 14, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        lbl_title.pack(pady=20)

        # زر تحميل الإضافات
        btn_plugins = tk.Button(
            self.root,
            text="🔌 إدارة الإضافات (Plugins)",
            command=self.plugin_loader.open_plugin_manager
        )
        btn_plugins.pack(pady=10, fill=tk.X, padx=50)

        # زر إنهاء
        btn_exit = tk.Button(
            self.root,
            text="❌ إنهاء النظام",
            command=self.root.quit
        )
        btn_exit.pack(pady=10, fill=tk.X, padx=50)

        self.language = "ar"  # اللغة الافتراضية: عربي

if __name__ == "__main__":
    root = tk.Tk()
    app = AeroCageLauncher(root)
    root.mainloop()
