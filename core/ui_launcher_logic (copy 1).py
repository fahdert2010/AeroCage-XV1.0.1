#!/usr/bin/env python3
"""
File Name: ui_launcher_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_launcher_logic.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Execution Pipeline Logic Component for AeroCage-X Launcher.
             Handles isolated process mapping and environmental parameters.
"""

import os
import sys
import subprocess
from pathlib import Path
from tkinter import messagebox

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

    def trigger_integrated_module(self, action_key: str):
        """التحكم والتشغيل المتسلسل للمحركات المدمجة بالاعتماد على النواة الصلبة"""
        if not self.ap_ip or not self.ap_password:
            msg = "الرجاء تلقيم بيانات الاتصال بالراوتر أولاً قبل بدء العملية التكتيكية!"
            messagebox.showwarning(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("نقص بيانات"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            )
            return

        if action_key == "LAUNCH_ORCHESTRATOR":
            orchestrator = CoreAttackOrchestrator(self.ap_ip, self.ap_password)
            success = orchestrator.execute_protected_mission_pipeline(
                radio="radio1", section="default_radio1", channel="6", band="2G"
            )
            if success:
                info = "تم تهيئة العتاد وحصاد الأجهزة وإطلاق المايسترو وثبات القناة!"
                messagebox.showinfo(
                    SharedVisualLinguisticToolkit.process_mixed_text_safely("المايسترو نشط"),
                    SharedVisualLinguisticToolkit.process_mixed_text_safely(info)
                )

        elif action_key == "LAUNCH_SILENT_SNIFFER":
            sniffer = SilentSigIntSniffer(self.ap_ip, self.ap_password)
            sniffer.start_silent_intel_harvesting(ap_interface="phy1-ap1")
            info = "بدأ محرك الاعتراض الصامت في امتصاص حزم البيانات وتصفية الغنائم."
            messagebox.showinfo(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("جناح التجسس نشط"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(info)
            )

    @staticmethod
    def spawn_subsystem_safe(script_relative_path: str, module_title: str):
        """تشغيل الملفات البرمجية كعمليات فرعية معزولة ومحمية من ثغرات مسارات النظام"""
        full_script_path = BASE_DIR / script_relative_path
        if not full_script_path.exists():
            msg = f"الملف البرمجي غير موجود في المسار: {script_relative_path}"
            messagebox.showerror(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("خطأ في المنظومة"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            )
            return

        # نسف ثغرة ModuleNotFoundError بحقن الـ PYTHONPATH الثابت للعملية المعزولة
        env_context = os.environ.copy()
        env_context["PYTHONPATH"] = str(BASE_DIR)

        try:
            print(f"[*] جاري إطلاق الواجهة الفرعية المؤمنة [{module_title}]...")
            # pylint: disable=consider-using-with
            subprocess.Popen([sys.executable, str(full_script_path)], env=env_context, shell=False)
        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            # تفتيت طول السطر للامتثال لـ PEP 8 وحصد الـ 10/10 الصافية كلياً
            msg_err = f"تعذر تشغيل الوحدة الفرعية: {e}"
            messagebox.showerror(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("فشل الإطلاق"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg_err)
            )


if __name__ == "__main__":
    print("[+] UI Launcher execution logic sharding component verified.")
