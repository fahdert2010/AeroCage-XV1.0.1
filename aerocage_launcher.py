#!/usr/bin/env python3
"""
File Name: aerocage_launcher.py
Path: /home/kali/AeroCage-XV1.0.1/aerocage_launcher.py
Created Date: 2026-05-26
Version: 1.4.2
Description: Dynamic Sovereign System Launcher Dashboard for AeroCage-X.
             Enforces pure PEP 8 compliance with zero runtime path hacks.
"""

import tkinter as tk

# استيرادات النواة والمشروع في السطر الأول تماماً بنقاء هندسي مطلق 100%
from core.ui_base import AeroCageUIBase
from core.ui_strike_coordinator import UiStrikeCoordinator

# مصفوفة التسجيل المركزي الذكي لخيارات المنظومة الحالية والتطويرات القادمة
AVAILABLE_MODULES = {
    "6": {
        "text": "🚀 [ الخيار 6 ]: غرف عمليات الغزو وحراسة الأثير",
        "coordinator_class": UiStrikeCoordinator
    }
}


class AeroCageMasterLauncher(AeroCageUIBase):
    """
    Main Sovereign Dynamic Launcher GUI Dashboard View.
    Generates interface options recursively using the centralized modules registry.
    """

    def __init__(self, root: tk.Tk):
        """تهيئة اللانشر وتوجيه جينات الأب للثيم السيبراني الموحد للـ RAM"""
        super().__init__(
            root,
            title="AeroCage-X: نظام القيادة اللاسلكي الموزع الحركي",
            width=620,
            height=400
        )
        self.active_coordinator = None
        self.build_launcher_interface()

    def build_launcher_interface(self):
        """بناء لوحة الاختيارات الرئيسية وقراءة مصفوفة التسجيل ديناميكياً حياً"""
        txt_title = "⚡ AEROCAGE-X: PLUG-AND-PLAY MISSION DASHBOARD ⚡"
        lbl_title = tk.Label(self.root, text=txt_title, font=("Courier", 12, "bold"))
        self.apply_cyber_theme(lbl_title, "label")
        lbl_title.pack(pady=30)

        menu_frame = tk.Frame(self.root, bg=self.bg_main)
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=50)

        for _, meta in AVAILABLE_MODULES.items():
            btn_text = meta["text"]
            coord_class = meta["coordinator_class"]

            btn_dyn = tk.Button(
                menu_frame,
                text=btn_text,
                command=lambda cl=coord_class: self.delegate_to_target_mediator(cl)
            )
            self.apply_cyber_theme(btn_dyn, "button", alert_style=True)
            btn_dyn.pack(pady=10, fill=tk.X)

        btn_exit = tk.Button(
            menu_frame, text="❌ إنهاء الجلسة وإغلاق المنظومة", command=self.root.quit
        )
        self.apply_cyber_theme(btn_exit, "button")
        btn_exit.pack(pady=15, fill=tk.X)

        lbl_status = tk.Label(
            self.root, text="📥 جاهز، منصة الإقلاع الحركي مستعدة لتوجيه الممرات...",
            bd=1, relief=tk.SUNKEN, font=("Arial", 10, "bold")
        )
        self.apply_cyber_theme(lbl_status, "label")
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def delegate_to_target_mediator(self, coordinator_class):
        """إحالة وبث القيادة الكاملة صامتاً للوسيط المختار لكسر الاقتران الوثيق للواجهات"""
        print("[+] Launcher Context: Instantiating dynamic mediator engine Loop.")

        self.active_coordinator = coordinator_class(self.root)
        self.active_coordinator.launch_strike_provisioning_view()


if __name__ == "__main__":
    root_window = tk.Tk()
    app = AeroCageMasterLauncher(root_window)
    root_window.mainloop()
