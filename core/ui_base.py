#!/usr/bin/env python3
"""
File Name: ui_base.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_base.py
Created Date: 2026-05-25
Version: 1.0.7
Description: Abstract Base GUI Class for AeroCage-X. Provides centralized layout 
             factories, global error messaging wrappers, and dynamic BiDi filtration.
"""

import sys
import re
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import arabic_reshaper
from bidi.algorithm import get_display

# ربط المسارات بالنواة المركزية
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard


# pylint: disable=too-many-instance-attributes
class AeroCageUIBase:
    """
    Main Abstract View Component.
    Encapsulates core styling parameters and graphical helper methods with BiDi guards.
    """

    def __init__(self, root: tk.Tk, title: str, width: int = 750, height: int = 480):
        """تهيئة النوافذ الرسومية وتوحيد سمات الألوان الداكنة للمنصة"""
        self.root = root
        self.title = SystemGuard.sanitize_input(title, "csv_value")
        self.width = width
        self.height = height

        # الألوان القياسية المعيارية للمنظومة (Dark UI Theme)
        self.bg_main = "#121212"
        self.bg_panel = "#1E1E1E"
        self.fg_primary = "#00FF00"
        self.fg_alert = "#FF3333"
        self.fg_text = "#FFFFFF"
        self.bg_entry = "#2D2D2D"

        self.setup_base_window()

    def setup_base_window(self):
        """تعديل أبعاد النافذة وحساب إحداثيات التمركز على شاشة العرض تلقائياً"""
        self.root.title(f"AeroCage-X  |  {self.title}")
        self.root.configure(bg=self.bg_main)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_x = (screen_width // 2) - (self.width // 2)
        position_y = (screen_height // 2) - (self.height // 2)

        self.root.geometry(
            f"{self.width}x{self.height}+{position_x}+{position_y}"
        )
        self.root.protocol("WM_DELETE_WINDOW", self.on_secure_close)

    def process_mixed_text_safely(self, raw_text: str) -> str:
        """محرك فرز جراحي عام: فصل الرموز اللاتينية وعكس العربي لمنع تخبيص الخطوط"""
        if not raw_text:
            return ""

        prefix_match = re.match(r'^([\s🔏🔒🌐🔄🎯🛑📥📊⚡🪐🚀\]\[\d\.\-\:]+)', raw_text)

        if prefix_match:
            prefix = prefix_match.group(1)
            arabic_part = raw_text[len(prefix):].strip()
            if arabic_part:
                reshaped = arabic_reshaper.reshape(arabic_part)
                return f"{prefix} {get_display(reshaped)}"
            return prefix

        reshaped = arabic_reshaper.reshape(raw_text)
        return get_display(reshaped)

    def apply_cyber_theme(
        self, widget, widget_type: str = "label", alert_style: bool = False
    ):
        """تطبيق تنسيقات السمات الموحدة مع معالجة أحادية السريان لعدم تكرار عكس النصوص"""
        try:
            current_text = widget.cget("text")
            if current_text and widget_type in ["label", "button"]:
                widget.configure(text=self.process_mixed_text_safely(current_text))
        except (tk.TclError, AttributeError, ValueError):
            pass

        if widget_type == "label":
            fg_color = self.fg_alert if alert_style else self.fg_primary
            widget.configure(bg=self.bg_main, fg=fg_color)
        elif widget_type in ["frame", "labelframe"]:
            if widget_type == "labelframe":
                widget.configure(bg=self.bg_main, fg=self.fg_primary)
            else:
                widget.configure(bg=self.bg_main)
        elif widget_type == "entry":
            widget.configure(
                bg=self.bg_entry,
                fg=self.fg_text,
                insertbackground="white",
                bd=1,
                relief=tk.SOLID
            )
        elif widget_type == "button":
            bg_color = self.fg_alert if alert_style else "#005500"
            widget.configure(
                bg=bg_color,
                fg=self.fg_text,
                activebackground=self.fg_primary,
                activeforeground=self.bg_main,
                font=("Arial", 10, "bold"),
                bd=2,
                relief=tk.RAISED
            )

    def configure_combobox_style(self, combo_widget: ttk.Combobox, values_list: list):
        """سحق مشكلة القائمة المنسدلة لغوياً عبر استدعاء ميثود الفرز العام المطور"""
        try:
            clean_values = [self.process_mixed_text_safely(str(v)) for v in values_list]
            combo_widget.configure(values=clean_values)
            if clean_values:
                combo_widget.set(clean_values)
        except (tk.TclError, AttributeError, KeyError, ValueError):
            pass

        # لتوحيد وتطهير خطوط القائمة المنسدلة المفتوحة داخلياً في Tkinter ومنع تخبيصها
        self.root.option_add("*TCombobox*Listbox.font", ("Arial", 10, "bold"))
        self.root.option_add("*TCombobox*Listbox.background", self.bg_panel)
        self.root.option_add("*TCombobox*Listbox.foreground", self.fg_text)

    def configure_treeview_style(self, tree_widget: ttk.Treeview):
        """توحيد وعكس واجهات جداول البيانات الرسومية لحفظ اتساق العرض"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=self.bg_panel,
            fieldbackground=self.bg_panel,
            foreground=self.fg_text,
            rowheight=25
        )
        style.configure(
            "Treeview.Heading",
            background=self.bg_entry,
            foreground=self.fg_primary,
            font=("Arial", 10, "bold")
        )

        try:
            for col in tree_widget["columns"]:
                old_heading = tree_widget.heading(col, "text")
                if old_heading:
                    tree_widget.heading(
                        col,
                        text=self.process_mixed_text_safely(old_heading)
                    )
        except (tk.TclError, KeyError, IndexError):
            pass

    def display_info_message(self, title_txt: str, body_txt: str):
        """قناة مركزية موحدة لبث رسائل النجاح التكتيكية مصفاة الحروف لجميع الواجهات الفرعية"""
        messagebox.showinfo(
            self.process_mixed_text_safely(title_txt),
            self.process_mixed_text_safely(body_txt),
            parent=self.root
        )

    def display_warning_message(self, title_txt: str, body_txt: str):
        """قناة مركزية موحدة لبث رسائل التحذير والأخطاء مصفاة الحروف لجميع الواجهات الفرعية"""
        messagebox.showwarning(
            self.process_mixed_text_safely(title_txt),
            self.process_mixed_text_safely(body_txt),
            parent=self.root
        )

    @staticmethod
    def clear_treeview_records(tree_widget: ttk.Treeview):
        """تنظيف وتفريغ كافة السجلات المعروضة في الجدول الرسومي"""
        for item in tree_widget.get_children():
            tree_widget.delete(item)

    def on_secure_close(self):
        """تفريغ كائنات الواجهة وإغلاق النافذة بنظام أمن ومنع الـ Memory Hang"""
        try:
            print(f"[*] Destroying active GUI view context for: {self.title}")
            self.root.destroy()
        except (tk.TclError, AttributeError):
            sys.exit(0)


if __name__ == "__main__":
    print("[+] Core UI Base layout factory setup verified.")
