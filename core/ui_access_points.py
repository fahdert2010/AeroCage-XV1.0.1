#!/usr/bin/env python3
"""
File Name: ui_access_points.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_access_points.py
Created Date: 2026-05-25
Version: 1.0.9
Description: Lean Wireless Access Points Tracking GUI View for AeroCage-X.
             Decompiled from database logic handles via AccessPointsController.
"""

import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# ربط المسارات بالنواة المركزية
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard
from core.ui_base import AeroCageUIBase
from core.ui_access_points_logic import AccessPointsController


class AeroCageAccessPointsGUI(AeroCageUIBase):
    """
    Access Points Visual View Component.
    Responsible exclusively for table matrix layouts construction and styling config.
    """

    def __init__(self, root: tk.Tk, db_instance):
        """تهيئة النافذة وحقن أرقام ومطابقة ترويسة شاشة تتبع نقاط الوصول"""
        super().__init__(
            root,
            title="إدارة وتتبع نقاط الوصول اللاسلكية",
            width=800,
            height=520
        )

        self.db_manager = db_instance

        # ربط كائن التحكم المساعد والمنعزل لتصفير تضخم السطور في هذا الملف
        self.controller = AccessPointsController(self)

        self.btn_refresh = None
        self.btn_inject_target = None
        self.tree = None
        self.status_var = None

        self.build_ap_interface()
        self.controller.refresh_ap_list_async()

    def build_ap_interface(self):
        """بناء وتوزيع الهيكل الرسومي وعناصر التحكم بجدول البيانات مع مطابقة الأرقام"""
        lbl_header = tk.Label(
            self.root,
            text="🌐 1. لوحة إدارة وتحليل نقاط الوصول اللاسلكية المكتشفة",
            font=("Courier", 12, "bold")
        )
        self.apply_cyber_theme(lbl_header, "label")
        lbl_header.pack(pady=10)

        control_frame = tk.Frame(self.root)
        self.apply_cyber_theme(control_frame, "frame")
        control_frame.pack(pady=5, fill=tk.X, padx=20)

        self.btn_refresh = tk.Button(
            control_frame,
            text="🔄 تحديث طابور النقاط لـ 1",
            command=self.controller.refresh_ap_list_async
        )
        self.apply_cyber_theme(self.btn_refresh, "button")
        self.btn_refresh.pack(side=tk.LEFT, padx=5)

        self.btn_inject_target = tk.Button(
            control_frame,
            text="🎯 تلقيم هدف الواجهة 1 للموجه",
            command=self.controller.inject_selected_ap_to_strike
        )
        self.apply_cyber_theme(self.btn_inject_target, "button", alert_style=True)
        self.btn_inject_target.pack(side=tk.RIGHT, padx=5)

        table_frame = tk.Frame(self.root)
        self.apply_cyber_theme(table_frame, "frame")
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("BSSID", "ESSID", "Channel", "Power", "LastSeen"),
            show="headings"
        )
        self.tree.heading("BSSID", text="BSSID / MAC Address")
        self.tree.heading("ESSID", text="ESSID / Wi-Fi Name")
        self.tree.heading("Channel", text="القناة")
        self.tree.heading("Power", text="قوة الإشارة (Signal)")
        self.tree.heading("LastSeen", text="آخر رصد تكتيكي")

        for col in ("BSSID", "ESSID", "Channel", "Power", "LastSeen"):
            self.tree.column(col, anchor=tk.CENTER)

        self.configure_treeview_style(self.tree)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="")
        lbl_status = tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 10, "bold"),
            fg=self.fg_primary,
            bg=self.bg_entry
        )
        lbl_status.config(text="📥 جاهز بانتظار قراءة سجلات نقاط البث...")
        self.apply_cyber_theme(lbl_status, "label")
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    from core.db_manager import DatabaseManager
    SystemGuard.enforce_root_privileges("واجهة النقاط")
    root_window = tk.Tk()
    app = AeroCageAccessPointsGUI(root_window, DatabaseManager())
    root_window.mainloop()
