#!/usr/bin/env python3
"""
File Name: ui_launcher_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_launcher_logic.py
Created Date: 2026-05-25
Version: 1.0.4
Description: Execution Pipeline Logic Component for AeroCage-X Launcher.
             Handles isolated process mapping and environmental parameters.
"""

import os
import sys
from pathlib import Path
from tkinter import messagebox

from core.process_manager import ProcessManager
from core.core_attack_orchestrator import CoreAttackOrchestrator
from modules.silent_sigint_sniffer import SilentSigIntSniffer
from utils.shared_utils_3 import SharedVisualLinguisticToolkit

BASE_DIR = Path(__file__).resolve().parent.parent


class UiLauncherLogicComponent:
    """
    Subsystem Process Coordinator Component.
    Deploys asynchronous backend loops and manages explicit python paths.
    """

    def __init__(self):
        """تهيئة معطيات الاتصال ومراجع التحكم الكائني للمايسترو والـ Sniffer"""
        self.ap_ip = None
        self.ap_password = None
        # إحالة إدارة العمليات الفرعية للنواة المعتمدة صراحة لسحق قيد R1732
        self.proc_manager = ProcessManager()

    def trigger_integrated_module(self, action_key: str):
        """التحكم والتشغيل للمحركات المدمجة (المايسترو وجناح التجسس)"""
        if not self.ap_ip or not self.ap_password:
            msg = "الرجاء تلقيم بيانات الاتصال بالراوتر أولاً قبل بدء العملية!"
            messagebox.showwarning(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("نقص بيانات"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            )
            return

        if action_key == "LAUNCH_ORCHESTRATOR":
            orchestrator = CoreAttackOrchestrator(self.ap_ip, self.ap_password)
            success = orchestrator.execute_protected_mission_pipeline(
                radio="radio0", section="default_radio0", channel="6", band="2G"
            )
            if success:
                info = "تم تهيئة العتاد وحصاد الأجهزة وإطلاق المايسترو وثبات القناة!"
                messagebox.showinfo(
                    SharedVisualLinguisticToolkit.process_mixed_text_safely("المايسترو نشط"),
                    SharedVisualLinguisticToolkit.process_mixed_text_safely(info)
                )

        elif action_key == "LAUNCH_SILENT_SNIFFER":
            sniffer = SilentSigIntSniffer(self.ap_ip, self.ap_password)
            sniffer.start_silent_intel_harvesting(ap_interface="phy1-ap0")
            info = "بدأ محرك الاعتراض الصامت في امتصاص حزم البيانات وتصفية الغنائم."
            messagebox.showinfo(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("جناح التجسس نشط"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(info)
            )

    def spawn_subsystem_safe(self, script_relative_path: str, module_title: str):
        """تشغيل الملفات البرمجية كعمليات فرعية مستقلة ومحمية عبر مدير النواة الموحد"""
        full_script_path = BASE_DIR / script_relative_path
        if not full_script_path.exists():
            msg = f"الملف البرمجي غير موجود في المسار: {script_relative_path}"
            messagebox.showerror(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("خطأ في المنظومة"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            )
            return

        env_context = os.environ.copy()
        env_context["PYTHONPATH"] = str(BASE_DIR)

        try:
            print(f"[*] جاري إطلاق الواجهة الفرعية المؤمنة [{module_title}]...")
            command_array = [sys.executable, str(full_script_path)]
            # استخدام مصنع تفريع العمليات الآمن للنواة لحظر تحذيرات تخصيص الموارد كلياً
            self.proc_manager.spawn_process_safe(script_relative_path, command_array)
        except (ValueError, KeyError, AttributeError, SystemError) as e:
            msg_err = f"تعذر تشغيل الوحدة الفرعية: {e}"
            messagebox.showerror(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("فشل الإطلاق"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg_err)
            )


if __name__ == "__main__":
    print("[+] UI Launcher execution logic sharding component verified.")
