#!/usr/bin/env python3
"""
File Name: ui_scout.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_scout.py
Created Date: 2026-05-25
Version: 1.0.8
Description: Live Client Discovery and Radio Signals Monitoring GUI View for AeroCage-X.
             Optimized for asynchronous thread-safe polling via IntelUbusScout APIs.
"""

import sys
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# ربط محاور مفسر بايثون بجذر المستودع لضمان قراءة التبعيات الفرعية
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# pylint: disable=import-error, wrong-import-position
from core.ui_base import AeroCageUIBase
from core.intel_ubus_scout import IntelUbusScout


class AeroCageScoutGUI(AeroCageUIBase):
    """
    Live Wireless Signal Scout GUI View Component.
    Manages runtime polling grids for captured OpenWrt client devices.
    """

    def __init__(self, root: tk.Tk):
        """تهيئة واجهة الرصد والربط بمحرك استكشاف الـ Ubus الخلفي المطور"""
        super().__init__(
            root,
            title="3. مستكشف وراصد الإشارات وفحص الزباين حياً",
            width=760,
            height=520
        )

        self.ubus_scout = IntelUbusScout()
        self.status_var = None
        self.btn_start = None
        self.tree = None
        self.is_scouting = False

        self.build_scout_interface()

    def build_scout_interface(self):
        """بناء الجداول والـ Widgets الرسومية بالثيم الداكن الموحد للأب"""
        lbl_title = tk.Label(
            self.root,
            text="📡 3. مستكشف وراصد الإشارات وفحص الزباين في الأثير البعيد",
            font=("Courier", 11, "bold")
        )
        self.apply_cyber_theme(lbl_title, "label")
        lbl_title.pack(pady=15)

        tree_frame = tk.Frame(self.root, bg=self.bg_main)
        tree_frame.pack(padx=25, fill=tk.BOTH, expand=True)

        columns = ("mac", "signal", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

        # تفتيت كتل نصوص العناوين لحظر تخطي معيار الـ 100 حرف نهائياً
        title_mac = self.process_mixed_text_safely("🔒 البصمة الفيزيائية (MAC Address)")
        title_sig = self.process_mixed_text_safely("📶 قوة الإشارة (Signal dBm)")
        title_stat = self.process_mixed_text_safely("📊 الحالة التكتيكية")

        self.tree.heading("mac", text=title_mac)
        self.tree.heading("signal", text=title_sig)
        self.tree.heading("status", text=title_stat)

        self.tree.column("mac", anchor=tk.CENTER, width=240)
        self.tree.column("signal", anchor=tk.CENTER, width=160)
        self.tree.column("status", anchor=tk.CENTER, width=160)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview", background="#1E1E1E", foreground="#FFFFFF",
            fieldbackground="#1E1E1E", rowheight=25
        )
        style.map(
            "Treeview", background=[("selected", "#00FF00")],
            foreground=[("selected", "#121212")]
        )

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(pady=20, fill=tk.X, padx=30)

        self.btn_start = tk.Button(
            btn_frame, text="📡 بدء الرصد والتقاط الحزم حياً",
            command=self.start_scouting_async
        )

        if hasattr(self, 'apply_cyber_button_style'):
            self.apply_cyber_button_style(self.btn_start)
        else:
            self.apply_cyber_theme(self.btn_start, "button")

        self.btn_start.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.X)

        btn_stop = tk.Button(
            btn_frame, text="🛑 إيقاف الرصد وتفكيك الجلسة",
            command=self.stop_scouting_context
        )
        self.apply_cyber_theme(btn_stop, "button")
        btn_stop.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.X)

        self.status_var = tk.StringVar()
        lbl_status = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN,
            anchor=tk.W, font=("Arial", 10, "bold"), fg=self.fg_primary, bg=self.bg_entry
        )

        msg_init = "📥 جاهز ومستقر.. بانتظار إشارة إطلاق نفق الاستطلاع للـ UBUS."
        self.status_var.set(self.process_mixed_text_safely(msg_init))
        self.apply_cyber_theme(lbl_status, "label")
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def start_scouting_async(self):
        """إطلاق جلسة مراقبة الـ ubus الحي للراوتر في الخلفية وتحديث الجداول حياً"""
        if self.is_scouting:
            return

        self.is_scouting = True
        self.btn_start.config(state=tk.DISABLED)

        msg = "🔄 جاري حفر الأنبوب الاستكشافي واستجواب حافلة أوامر الراوتر البعيد حياً..."
        self.status_var.set(self.process_mixed_text_safely(msg))

        self.ubus_scout.run_live_ubus_monitor_async(interface="phy1-ap1", interval_sec=5)
        self.root.after(1000, self._refresh_live_scout_grid)

    def _refresh_live_scout_grid(self):
        """تحديث تزامني حركي للـ Treeview لقراءة غنائم الأجهزة المكتشفة من الـ DB حياً"""
        if not self.is_scouting:
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        all_targets = self.ubus_scout.db_manager.get_all_active_targets()

        for target in all_targets:
            if "OpenWrt_Client" in target.get("status", ""):
                mac_lbl = target.get("bssid", "00:00:00:00:00:00")
                sig_lbl = f"{target.get('power', -100)} dBm"
                status_lbl = self.process_mixed_text_safely("🟢 نشط متصل بالبث")

                self.tree.insert("", tk.END, values=(mac_lbl, sig_lbl, status_lbl))

        self.root.after(3000, self._refresh_live_scout_grid)

    def stop_scouting_context(self):
        """إيقاف جلسة مراقبة الأثير وتطهير ممرات الذاكرة لحظر العمليات العالقة"""
        self.is_scouting = False
        self.ubus_scout.stop_ubus_monitor(interface="phy1-ap1")
        self.btn_start.config(state=tk.NORMAL)

        msg_done = "❌ تم قطع قنوات الاستطلاع العكسية وتفكيك النفق الاستخباراتي بنجاح."
        self.status_var.set(self.process_mixed_text_safely(msg_done))


if __name__ == "__main__":
    root_window = tk.Tk()
    app = AeroCageScoutGUI(root_window)
    root_window.mainloop()
