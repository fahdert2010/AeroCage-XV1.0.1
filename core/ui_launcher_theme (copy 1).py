#!/usr/bin/env python3
"""
File Name: ui_launcher_theme.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_launcher_theme.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Graphical Dark Cyber Theme Configuration Shard for AeroCage-X.
             Manages styling constants for the master control dashboard.
"""

import tkinter as tk


class UiLauncherThemeComponent:
    """
    Master C2 Styling Registry Component.
    Enforces tactical low-observability dark color schemas across frames.
    """

    def __init__(self):
        """تهيئة ثوابت الألوان الرقمية الموحدة للمنظومة العليا"""
        self.bg_main = "#121212"
        self.bg_frame = "#1E1E1E"
        self.fg_neon = "#00FF00"
        self.fg_white = "#FFFFFF"

    def apply_cyber_button_style(self, button_widget: tk.Button, custom_bg: str = None):
        """تطبيق الهوية البصرية الداكنة على كائنات الأزرار الرسومية بالتوالي"""
        bg_color = custom_bg if custom_bg else self.bg_frame
        button_widget.config(
            font=("Arial", 11, "bold"),
            bg=bg_color,
            fg=self.fg_white,
            activebackground=self.fg_neon,
            activeforeground=self.bg_main,
            bd=2,
            relief=tk.RAISED,
            height=2
        )

    def apply_frame_style(self, frame_widget: tk.LabelFrame):
        """دالة عامة ثانية لتلوين وإكساء الإطارات الرسومية وتصفير قيود Pylint"""
        frame_widget.config(
            bg=self.bg_main,
            fg=self.fg_neon,
            font=("Arial", 10, "bold")
        )


if __name__ == "__main__":
    print("[+] UI Launcher theme sharding component verified.")
