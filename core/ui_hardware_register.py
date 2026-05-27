#!/usr/bin/env python3
"""
File Name: ui_hardware_register.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_hardware_register.py
Created Date: 2026-05-25
Version: 1.0.5
Description: Lean Hardware Access Point Registration GUI View for AeroCage-X.
             Decompiled from operational business logic via HardwareRegisterController.
"""

import tkinter as tk
from tkinter import ttk

from core.ui_base import AeroCageUIBase
from core.ui_hardware_register_logic import HardwareRegisterController


class AeroCageHardwareRegisterGUI(AeroCageUIBase):
    """
    Hardware Registration Visual View Component.
    Responsible exclusively for form matrix construction and layout styling.
    """

    def __init__(self, root: tk.Tk, db_instance):
        """تهيئة النافذة وحقن معايير الترتيب والمعالج المساعد المنفصل"""
        super().__init__(
            root,
            title="0. مركز تهيئة وتلقيم بيانات الـ Root للراوتر",
            width=550,
            height=480
        )

        self.db_manager = db_instance
        self.controller = HardwareRegisterController(self)
        self.parent_callback = None

        self.fields = {}
        self.combo_group = None

        self.build_register_form()

    def set_parent_callback(self, callback_func):
        """حقن دالة رد الاتصال الراجع لتحديث بيانات ملف الإطلاق الرئيسي حياً"""
        self.parent_callback = callback_func

    def build_register_form(self):
        """بناء وتنسيق عناصر استمارة تلقيم بيانات الراوتر البعيد بالثيم الموحد"""
        available_groups = self.db_manager.get_unique_statuses_safe()
        if not available_groups:
            available_groups = ["Default_Target_Group"]

        lbl_title = tk.Label(
            self.root,
            text="🔒 0. مركز تهيئة وتلقيم بيانات الـ Root للراوتر",
            font=("Courier", 11, "bold")
        )
        self.apply_cyber_theme(lbl_title, "label")
        lbl_title.pack(pady=20)

        form_frame = tk.Frame(self.root, bg=self.bg_main)
        form_frame.pack(padx=30, fill=tk.X)

        # صف 1: اسم الجهاز المستهدف
        lbl_name = tk.Label(
            form_frame, text="اسم خادم التلقيم (ESSID):",
            fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_name, "label")
        lbl_name.grid(row=0, column=0, sticky=tk.W, pady=8)

        self.fields["name"] = tk.Entry(form_frame, width=24)
        self.apply_cyber_theme(self.fields["name"], "entry")
        self.fields["name"].grid(row=0, column=1, pady=8, padx=15)

        # صف 2: عنوان الـ IP للراوتر المستهدف
        lbl_ip = tk.Label(
            form_frame, text="عنوان IP للراوتر (OpenWrt):",
            fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_ip, "label")
        lbl_ip.grid(row=1, column=0, sticky=tk.W, pady=8)

        self.fields["ip"] = tk.Entry(form_frame, width=24)
        self.fields["ip"].insert(0, "192.168.1.1")
        self.apply_cyber_theme(self.fields["ip"], "entry")
        self.fields["ip"].grid(row=1, column=1, pady=8, padx=15)

        # صف 3: مستخدم الـ SSH
        lbl_user = tk.Label(
            form_frame, text="اسم مستخدم الـ SSH للراوتر:",
            fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_user, "label")
        lbl_user.grid(row=2, column=0, sticky=tk.W, pady=8)

        self.fields["user"] = tk.Entry(form_frame, width=24)
        self.fields["user"].insert(0, "root")
        self.apply_cyber_theme(self.fields["user"], "entry")
        self.fields["user"].grid(row=2, column=1, pady=8, padx=15)

        # صف 4: كلمة المرور للـ Root
        lbl_pass = tk.Label(
            form_frame, text="كلمة مرور الـ Root للراوتر:",
            fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_pass, "label")
        lbl_pass.grid(row=3, column=0, sticky=tk.W, pady=8)

        self.fields["pass"] = tk.Entry(form_frame, width=24, show="*")
        self.apply_cyber_theme(self.fields["pass"], "entry")
        self.fields["pass"].grid(row=3, column=1, pady=8, padx=15)

        # صف 5: المجموعة التنظيمية
        lbl_grp = tk.Label(
            form_frame, text="اختر المجموعة الاستراتيجية:",
            fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_grp, "label")
        lbl_grp.grid(row=4, column=0, sticky=tk.W, pady=8)

        self.combo_group = ttk.Combobox(form_frame, state="readonly", width=22)
        self.configure_combobox_style(self.combo_group, available_groups)
        self.combo_group.grid(row=4, column=1, pady=8, padx=15)

        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(pady=35, fill=tk.X, padx=40)

        btn_save = tk.Button(
            btn_frame, text="💾 تثبيت وحفظ الخادم",
            command=self.controller.commit_hardware_registration
        )
        self.apply_cyber_theme(btn_save, "button")
        btn_save.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.X)

        btn_close = tk.Button(
            btn_frame, text="❌ إلغاء وإغلاق",
            command=self.root.destroy
        )
        self.apply_cyber_theme(btn_close, "button", alert_style=True)
        btn_close.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.X)


if __name__ == "__main__":
    from core.db_manager import DatabaseManager
    root_window = tk.Tk()
    app = AeroCageHardwareRegisterGUI(root_window, DatabaseManager())
    root_window.mainloop()
