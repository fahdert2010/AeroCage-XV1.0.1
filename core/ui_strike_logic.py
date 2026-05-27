#!/usr/bin/env python3
"""
File Name: ui_strike_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_strike_logic.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Business Logic Controller for AeroCageStrikeGUI.
             Manages event handles and thread-safe process monitoring pulses.
"""

import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ربط المسارات بالنواة المركزية للمنظومة
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position, no-name-in-module
from core.system_guard import SystemGuard
from modules.strike_launcher import StrikeLauncher


class StrikeGUIController:
    """
    Main Controller Object for the Strike GUI Module.
    Handles background executions, terminations, and continuous life polling.
    """

    def __init__(self, view_subsystem):
        """تهيئة المساعد وربطه بالواجهة الرسومية الحية للانشر الوسيط"""
        self.view = view_subsystem
        self.strike_orchestrator = StrikeLauncher()
        self.active_target_mac = None

    def handle_strike_activation(self, interface: str, bssid: str):
        """إرسال المدخلات للانشر ليتولى الإطلاق بأمان ومنع تجمد خيط الواجهة"""
        if not interface or not bssid:
            messagebox.showwarning(
                "بيانات ناقصة لـ 6",
                "الرجاء ملء حقول المدخلات بصيغة صحيحة!",
                parent=self.view.root
            )
            return

        self.view.btn_fire.config(state=tk.DISABLED)

        success = self.strike_orchestrator.launch_strike_session(interface, bssid)
        if success:
            self.active_target_mac = SystemGuard.sanitize_input(bssid, "bssid")
            status_msg = f"🔄 جاري تشغيل خطوة الفصل ضد [{self.active_target_mac}] للواجهة 6..."
            self.view.status_var.set(self.view.process_mixed_text_safely(status_msg))
        else:
            self.view.btn_fire.config(state=tk.NORMAL)
            msg_err = "🔴 فشل إطلاق الأنبوب التشغيلي للواجهة 6."
            self.view.status_var.set(self.view.process_mixed_text_safely(msg_err))

    def handle_strike_termination(self):
        """إخماد وقطع المهمة النشطة الموجهة بالماك بدقة وتنظيف قنوات الذاكرة"""
        if self.active_target_mac:
            status_msg = f"🔄 جاري إلغاء الماك [{self.active_target_mac}] للواجهة 6..."
            self.view.status_var.set(self.view.process_mixed_text_safely(status_msg))

            self.strike_orchestrator.stop_strike_session(self.active_target_mac)

            msg_stop = "📥 تم قطع المهام وتنظيف قنوات الذاكرة للواجهة 6 بنجاح."
            self.view.root.after(
                0,
                lambda: self.view.status_var.set(
                    self.view.process_mixed_text_safely(msg_stop)
                )
            )
            self.active_target_mac = None
            self.view.btn_fire.config(state=tk.NORMAL)
        else:
            messagebox.showinfo(
                "تنبيه تكتيكي لـ 6",
                "لا توجد مهام نشطة حالياً لإيقافها.",
                parent=self.view.root
            )

    def run_live_polling_pulse(self):
        """محرك النبض التناظري لاستجواب حالة استقرار الأنبوب التشغيلي حياً بالخلفية"""
        if self.active_target_mac:
            p_manager = self.strike_orchestrator.manager.proc_manager
            if self.active_target_mac in p_manager.active_processes:
                process = p_manager.active_processes[self.active_target_mac]
                if process.poll() is not None:
                    err_msg = f"🔴 تنبيه: انتهت عملية الفحص للهدف [{self.active_target_mac}] قسرياً!"
                    self.view.status_var.set(self.view.process_mixed_text_safely(err_msg))
                    self.active_target_mac = None
                    self.view.btn_fire.config(state=tk.NORMAL)

        self.view.root.after(1000, self.run_live_polling_pulse)


if __name__ == "__main__":
    print("[+] Strike GUI Controller helper logic module verified.")
