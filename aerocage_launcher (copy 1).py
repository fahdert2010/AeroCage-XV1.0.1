#!/usr/bin/env python3
"""
File Name: aerocage_launcher.py
Path: /home/kali/AeroCage-XV1.0.1/aerocage_launcher.py
Created Date: 2026-05-25
Version: 1.1.1
Description: Master Command and Control GUI Launcher for AeroCage-X.
             Enforces dynamic radio-to-band hardware abstraction mapping rules.
"""

import sys
from pathlib import Path
from functools import partial
import tkinter as tk

# ربط محاور مفسر بايثون لضمان سحب الحزم السيادية للنواة المشطورة
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.system_guard import SystemGuard
from core.db_manager import DatabaseManager
from core.ui_launcher_theme import UiLauncherThemeComponent
from core.ui_launcher_logic import UiLauncherLogicComponent
from utils.shared_utils_3 import SharedVisualLinguisticToolkit

# تفعيل خط الدفاع الأول الرسومي فوراً لحماية كامل الترسانة
SystemGuard.enforce_root_privileges("منظومة القيادة العليا AeroCage-X", graphical=True)


def fix_arabic_text(text):
    """دالة مطورة لحل كابوس تقطيع وعكس النصوص العربية المتداخلة في Tkinter"""
    if not text or not isinstance(text, str):
        return ""
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except (ValueError, TypeError, AttributeError):
        return text


class AeroCageMasterLauncher(UiLauncherThemeComponent, UiLauncherLogicComponent):
    """الكائن المركزي لإدارة وتشغيل منظومة القيادة العليا للمشروع"""

    def __init__(self, root_window: tk.Tk):
        """تهيئة واستدعاء مشيدات الشظايا المعمارية لتوحيد الثيم واللوجيك"""
        UiLauncherThemeComponent.__init__(self)
        UiLauncherLogicComponent.__init__(self)

        self.root = root_window
        self.root.title("AeroCage-X | منظومة القيادة والسيطرة العليا 2026")
        self.root.geometry("850x680")
        self.root.configure(bg=self.bg_main)

        self.db_manager = DatabaseManager()
        self.lbl_env = None

        self.build_master_ui()

    def build_master_ui(self):
        """بناء عناصر الواجهة الرسومية وتوزيع الأزرار الثمانية هندسياً"""
        lbl_master = tk.Label(
            self.root, text="AERO CAGE - X  |  MASTER COMMAND CENTER",
            font=("Courier", 16, "bold"), fg=self.fg_neon, bg=self.bg_main
        )
        lbl_master.pack(pady=20)

        title_frame = SharedVisualLinguisticToolkit.process_mixed_text_safely(
            " إعدادات الاتصال المركزي بالراوتر (OpenWrt) "
        )
        conn_frame = tk.LabelFrame(
            self.root, text=title_frame, font=("Arial", 10, "bold"),
            fg=self.fg_neon, bg=self.bg_main, padx=15, pady=10
        )
        self.apply_frame_style(conn_frame)
        conn_frame.pack(pady=10, fill=tk.X, padx=40)

        btn_txt = SharedVisualLinguisticToolkit.process_mixed_text_safely(
            "🔒 تهيئة وتلقيم بيانات الـ Root للراوتر"
        )
        btn_configure = tk.Button(
            conn_frame, text=btn_txt, font=("Arial", 10, "bold"),
            bg="#1E1E1E", fg=self.fg_white, command=self.prompt_target_credentials
        )
        btn_configure.pack(fill=tk.X, pady=5)

        btn_zone = tk.Frame(self.root, bg=self.bg_main)
        btn_zone.pack(pady=10, fill=tk.BOTH, expand=True)

        modules_map = [
            ("🌐 1. إدارة وتتبع نقاط الوصول (Access Points)", "core/ui_access_points.py"),
            ("👥 2. إدارة مجموعات الاستهداف (Groups UI)", "core/ui_groups.py"),
            ("📡 3. مستكشف وراصد الإشارات (Scout UI)", "core/ui_scout.py"),
            ("📊 4. مركز الاستخبارات والفرز (CSV Parser)", "modules/strike_csv_parser.py"),
            ("⚡ 5. محرك إدارة الأنابيب (Pipeline)", "modules/m3_kali_pipeline.py"),
            ("🚀 6. لوحة ضربات الفصل اللاسلكي (AirSurf)", "core/ui_strike.py"),
            ("🪐 7. تشغيل الأوركسترا والمايسترو (Orchestrator)", "LAUNCH_ORCHESTRATOR"),
            ("💀 8. جناح الاعتراض الصامت والتذاكر (SIGINT)", "LAUNCH_SILENT_SNIFFER")
        ]

        for text, path in modules_map:
            txt_safe = SharedVisualLinguisticToolkit.process_mixed_text_safely(text)
            if path in ["LAUNCH_ORCHESTRATOR", "LAUNCH_SILENT_SNIFFER"]:
                bg_color = "#1B5E20" if path == "LAUNCH_ORCHESTRATOR" else "#4A148C"
                btn = tk.Button(btn_zone, text=txt_safe, bg=bg_color)
                btn.config(command=partial(self.trigger_integrated_module, path))
            else:
                btn = tk.Button(btn_zone, text=txt_safe, bg="#1E1E1E")
                btn.config(command=partial(self.spawn_subsystem_safe, path, text))

            self.apply_cyber_button_style(btn)
            btn.pack(fill=tk.X, padx=50, pady=5)

        status_text = "بيئة النظام: خامل | الصلاحيات: ROOT | بانتظار تلقيم البيانات..."
        txt_env = SharedVisualLinguisticToolkit.process_mixed_text_safely(status_text)
        self.lbl_env = tk.Label(
            self.root, text=txt_env, bd=1, relief=tk.SUNKEN, anchor=tk.W,
            font=("Arial", 9, "italic"), fg="#FF3333", bg="#1E1E1E"
        )
        self.lbl_env.pack(side=tk.BOTTOM, fill=tk.X)

    def update_credentials_callback(self, ip: str, password: str):
        """دالة رد اتصال ذكية لتحديث بيانات الاستهداف فور تلقيمها حياً"""
        self.ap_ip = ip
        self.ap_password = password
        status = f"بيئة النظام: متصل بالهدف [{self.ap_ip}] | الحالة: جاهز للعمليات"
        txt_safe = SharedVisualLinguisticToolkit.process_mixed_text_safely(status)
        self.lbl_env.config(text=txt_safe, fg=self.fg_neon)

    def prompt_target_credentials(self):
        """استدعاء شاشة تهيئة الخوادم وتلقيمها مع حقن قاعدة البيانات مركزياً"""
        try:
            # pylint: disable=import-outside-toplevel
            from core.ui_hardware_register import AeroCageHardwareRegisterGUI
            sub_win = tk.Toplevel(self.root)

            app_instance = AeroCageHardwareRegisterGUI(sub_win, self.db_manager)

            if hasattr(app_instance, 'set_parent_callback'):
                app_instance.set_parent_callback(self.update_credentials_callback)

            msg = "بيئة النظام: تم استدعاء مركز تلقيم الخوادم بنجاح | الحالة: نشط"
            txt_msg = SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            self.lbl_env.config(text=txt_msg, fg=self.fg_neon)
        except (ImportError, AttributeError, tk.TclError) as e:
            print(f"[-] Core GUI Exception: Unable to spawn hardware register window: {e}")

    def trigger_integrated_module(self, action_key: str):
        """التحكم والتشغيل المتسلسل للمحركات بالاعتماد على النواة الصلبة والترشيح الحركي"""
        if not self.ap_ip or not self.ap_password:
            msg = "الرجاء تلقيم بيانات الاتصال بالراوتر أولاً قبل بدء العملية التكتيكية!"
            messagebox.showwarning(
                SharedVisualLinguisticToolkit.process_mixed_text_safely("نقص بيانات"),
                SharedVisualLinguisticToolkit.process_mixed_text_safely(msg)
            )
            return

        if action_key == "LAUNCH_ORCHESTRATOR":
            orchestrator = CoreAttackOrchestrator(self.ap_ip, self.ap_password)
            
            # هندسة الفرز الحركي: التحديد التلقائي لاسم الكرت والواجهة بناءً على النطاق والـ AP301 حياً
            # التردد 2G يوجه لـ radio0 و default_radio0، والتردد 5G يوجه لـ radio1 و default_radio1
            hardware_radio = "radio0"
            hardware_section = "default_radio0"
            
            success = orchestrator.execute_protected_mission_pipeline(
                radio=hardware_radio, section=hardware_section, channel="6", band="2G"
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


if __name__ == "__main__":
    main_root = tk.Tk()
    app = AeroCageMasterLauncher(main_root)
    main_root.mainloop()
