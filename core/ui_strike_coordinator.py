#!/usr/bin/env python3
"""
File Name: ui_strike_coordinator.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_strike_coordinator.py
Created Date: 2026-05-26
Version: 1.0.3
Description: Master UI Navigation and Mediator Coordinator for AeroCage-X.
             Enforces dynamic context handover with pure PEP 8 compliance.
"""

import tkinter as tk
from tkinter import messagebox

from core.ui_strike import AeroCageStrikeGUI
from core.ui_mission_control import AeroCageMissionControlGUI
from utils.opwrt_ssh_factory import OpWrtSSHFactory


class UiStrikeCoordinator:
    """
    Mediator Pattern Coordinator Subsystem.
    Orchestrates decoupled execution loops between provisioning and attack menus.
    """

    def __init__(self, root_window: tk.Tk):
        """تهيئة وسيط الملاحة الصامت وحجز مراجع النوافذ العليا بالذاكرة"""
        self.root = root_window
        self.strike_view = None
        self.active_missions = {}

    def launch_strike_provisioning_view(self):
        """إقلاع وبث واجهة التلقيم المبدئي الرشاقة رقم 6 بنقاء تام"""
        self.strike_view = AeroCageStrikeGUI(self.root)
        # إعادة توجيه دالة التحقق للزر لترتبط بـ وسيط التحكم كلياً
        self.strike_view.validate_and_spawn_mission_control = (
            self.navigate_to_mission_control
        )

    def navigate_to_mission_control(self):
        """بوابة العبور الآمنة: قنص معطيات التلقيم وبث غرفة العمليات المنبثقة"""
        view = self.strike_view
        ap_idx = view.combo_ap.current()

        if ap_idx == -1 or not view.hardware_list:
            msg = "الرجاء اختيار خادم الأكسس وتلقيم القناة والنطاق!"
            view.display_warning_message("بيانات ناقصة", msg)
            return

        selected_ap = view.hardware_list[ap_idx]
        ap_ip = selected_ap.get("bssid")
        ap_name = selected_ap.get("essid")

        # مصنع الاتصال الذكي المباشر دون وسيط محلي لتقليص الـ local variables حركياً
        if not OpWrtSSHFactory(ip=ap_ip, password="root").verify_ssh_heartbeat():
            title_err = view.process_mixed_text_safely("خطأ في الاتصال العتادي")
            body_err = view.process_mixed_text_safely(
                f"فشل الاتصال بالهدف [{ap_name}] عبر الـ SSH؛\n"
                "هل تريد فتح نافذة غرفة العمليات على أي حال للمحاكاة؟"
            )
            if not messagebox.askyesno(title_err, body_err):
                return

        print(f"[+] Mediator Route Secured: Provisioning window for: {ap_name}")

        # بناء القاموس مباشرة بالاقتناص من الحقول الرسومية لسحق عداد الـ too-many-locals
        ctx_data = {
            "ap_ip": ap_ip,
            "ap_name": ap_name,
            "channel": view.fields["channel"].get().strip(),
            "band": view.combo_band.get()
        }

        session_key = f"{ap_ip}_{ctx_data['band']}_CH{ctx_data['channel']}"
        sub_win = tk.Toplevel(self.root)

        mission_gui = AeroCageMissionControlGUI(
            root=sub_win, mission_context=ctx_data
        )
        self.active_missions[session_key] = mission_gui

        view.root.withdraw()


if __name__ == "__main__":
    root_main = tk.Tk()
    coordinator = UiStrikeCoordinator(root_main)
    coordinator.launch_strike_provisioning_view()
    root_main.mainloop()
