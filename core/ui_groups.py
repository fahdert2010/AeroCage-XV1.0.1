#!/usr/bin/env python3
"""
File Name: ui_groups.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_groups.py
Created Date: 2026-05-25
Version: 1.0.6
Description: Tactical Target Groups and Hardware Infrastructure Classification GUI 
             for AeroCage-X. Optimized for clean dynamic RAM caching filtration.
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
from core.ui_groups_logic import GroupsGUIController


class AeroCageGroupsGUI(AeroCageUIBase):
    """
    Target Groups and Infrastructure Segmentation View Window.
    Responsible exclusively for discrete graphical categorizations setup.
    """

    def __init__(self, root: tk.Tk, db_instance):
        """تهيئة النافذة الفرعية وحقن مقبض قاعدة البيانات والمعالج المساعد المنفصل"""
        super().__init__(
            root,
            title="إدارة مجموعات الاستهداف والعتاد",
            width=780,
            height=500
        )

        self.db_manager = db_instance
        self.controller = GroupsGUIController(self)

        self.combo_group = None
        self.btn_refresh = None
        self.tree = None
        self.status_var = None

        self.build_groups_interface()
        self.controller.load_groups_async()

    def build_groups_interface(self):
        """بناء الهيكل الرسومي وتوزيع عناصر الفلترة والفرز والتحكم بالثيم الموحد"""
        lbl_header = tk.Label(
            self.root,
            text="👥 2. مركز إدارة وتصنيف المجموعات والبنية التحتية للعتاد",
            font=("Courier", 12, "bold")
        )
        self.apply_cyber_theme(lbl_header, "label")
        lbl_header.pack(pady=10)

        control_frame = tk.Frame(self.root)
        self.apply_cyber_theme(control_frame, "frame")
        control_frame.pack(pady=5, fill=tk.X, padx=20)

        lbl_select = tk.Label(control_frame, text="اختر فئة العرض للواجهة 2:", font=("Arial", 10))
        self.apply_cyber_theme(lbl_select, "label")
        lbl_select.pack(side=tk.LEFT, padx=5)

        grp_values = [
            "أجهزة الترسانة والعتاد الملقم",
            "جميع الشبكات المرصودة في الجو",
            "أهداف عالية الأهمية (VIP)"
        ]
        self.combo_group = ttk.Combobox(control_frame, state="readonly", width=28)
        self.configure_combobox_style(self.combo_group, grp_values)

        self.combo_group.bind(
            "<<ComboboxSelected>>",
            lambda e: self.controller.load_groups_async()
        )
        self.combo_group.pack(side=tk.LEFT, padx=10)

        self.btn_refresh = tk.Button(
            control_frame,
            text="🔄 تحديث حركي لـ 2",
            command=self.controller.load_groups_async
        )
        self.apply_cyber_theme(self.btn_refresh, "button")
        self.btn_refresh.pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(self.root)
        self.apply_cyber_theme(table_frame, "frame")
        table_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("BSSID", "ESSID", "Channel", "Power", "Status"),
            show="headings"
        )
        self.tree.heading("BSSID", text="عنوان IP / MAC Address")
        self.tree.heading("ESSID", text="اسم الجهاز / ESSID")
        self.tree.heading("Channel", text="القناة")
        self.tree.heading("Power", text="قوة الإشارة / النطاق")
        self.tree.heading("Status", text="الحالة التكتيكية للعتاد")

        for col in ("BSSID", "ESSID", "Channel", "Power", "Status"):
            self.tree.column(col, anchor=tk.CENTER)

        self.configure_treeview_style(self.tree)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar(value="")
        lbl_status = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN,
            anchor=tk.W, font=("Arial", 10, "bold"), fg=self.fg_primary, bg=self.bg_entry
        )
        lbl_status.config(text="📥 جاهز بانتظار استدعاء سجلات المجموعات...")
        self.apply_cyber_theme(lbl_status, "label")
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    from core.db_manager import DatabaseManager
    SystemGuard.enforce_root_privileges("واجهة المجموعات")
    root_window = tk.Tk()
    app = AeroCageGroupsGUI(root_window, DatabaseManager())
    root_window.mainloop()
