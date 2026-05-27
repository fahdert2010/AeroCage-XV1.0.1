#!/usr/bin/env python3
"""
File Name: ui_launcher_theme.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_launcher_theme.py
Description: Graphical Dark Cyber Theme Configuration Component for AeroCage-X.
"""

import tkinter as tk


class UiLauncherThemeComponent:
    """إدارة الألوان الرقمية وتنسيق كائنات الأزرار والإطارات للـ GUI"""

    def __init__(self):
        self.bg_main = "#121212"
        self.bg_frame = "#1E1E1E"
        self.fg_neon = "#00FF00"
        self.fg_white = "#FFFFFF"

    def apply_cyber_button_style(self, button_widget: tk.Button, custom_bg: str = None):
        """تطبيق الهوية البصرية الداكنة على كائنات الأزرار الرسومية"""
        bg_color = custom_bg if custom_bg else self.bg_frame
        button_widget.config(
            font=("Arial", 11, "bold"), bg=bg_color, fg=self.fg_white,
            activebackground=self.fg_neon, activeforeground=self.bg_main,
            bd=2, relief=tk.RAISED, height=2
        )

    def apply_frame_style(self, frame_widget: tk.LabelFrame):
        """تلوين وإكساء الإطارات الرسومية الموحدة للمنظومة"""
        frame_widget.config(bg=self.bg_main, fg=self.fg_neon, font=("Arial", 10, "bold"))


if __name__ == "__main__":
    print("[+] UI Launcher theme sharding component verified.")
