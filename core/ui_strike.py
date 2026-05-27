#!/usr/bin/env python3
"""
File Name: ui_strike.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_strike.py
Created Date: 2026-05-26
Version: 1.2.9
Description: Master Tactical Strike UI Component for AeroCage-X.
             Streamlined provisioning panel integrated with mediators.
"""

import threading
import tkinter as tk
from tkinter import ttk

# الاستيرادات القياسية المباشرة للنواة بنقاء هندسي مطلق دون أي sys.path
from core.ui_base import AeroCageUIBase
from core.db_manager import DatabaseManager
from utils.opwrt_ssh_factory import OpWrtSSHFactory


class AeroCageStrikeGUI(AeroCageUIBase):
    """
    Tactical Strike Provisioning Panel GUI View.
    Manages client target alignment and forwards contexts to mediators safely.
    """

    def __init__(self, root: tk.Tk):
        """تهيئة النافذة وحقن معايير التثبيت والربط بكلاس الأب للثيم"""
        super().__init__(
            root,
            title="6. لوحة قيادة وتوجيه ضربات الفصل اللاسلكي التكتيكية",
            width=680,
            height=460
        )

        self.db_manager = DatabaseManager()
        self.fields = {}
        self.combo_ap = None
        self.combo_band = None
        self.status_var = None
        self.btn_session = None
        self.hardware_list = []

        self.build_strike_interface()

    def _load_registered_access_points(self) -> list:
        """سحب أجهزة الأكسسات الصديقة المسجلة حياً من قاعدة البيانات للـ Combobox"""
        all_targets = self.db_manager.get_all_active_targets()
        self.hardware_list = []
        display_names = []

        for target in all_targets:
            status_str = str(target.get("status", ""))
            if "Hardware_AP" in status_str or "Scanned_Core_Host" in status_str:
                self.hardware_list.append(target)
                name_lbl = f"{target.get('essid')} | IP: {target.get('bssid')}"
                display_names.append(name_lbl)

        return display_names

    def build_strike_interface(self):
        """بناء وتنسيق عناصر استمارة التلقيم المبدئي بالثيم الداكن الموحد"""
        txt_main_title = "🔥 6. مركز التلقيم المبدئي وإدارة قنوات التحكم اللاسلكي"
        lbl_title = tk.Label(
            self.root,
            text=txt_main_title,
            font=("Courier", 11, "bold")
        )
        self.apply_cyber_theme(lbl_title, "label")
        lbl_title.pack(pady=20)

        form_frame = tk.Frame(self.root, bg=self.bg_main)
        form_frame.pack(padx=30, fill=tk.X)

        txt_ap_lbl = "اختر خادم الهجوم البعيد (Access Point):"
        lbl_ap = tk.Label(
            form_frame, text=txt_ap_lbl, fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_ap, "label")
        lbl_ap.grid(row=0, column=0, sticky=tk.W, pady=8)

        self.combo_ap = ttk.Combobox(form_frame, state="readonly", width=28)
        ap_items = self._load_registered_access_points()
        if not ap_items:
            ap_items = ["لا توجد أكسسات مسجلة"]
        self.configure_combobox_style(self.combo_ap, ap_items)
        self.combo_ap.grid(row=0, column=1, pady=8, padx=15)
        self.combo_ap.bind("<<ComboboxSelected>>", self._trigger_live_heartbeat_check)

        txt_chan_lbl = "رقم القناة المراد العمل عليها:"
        lbl_chan = tk.Label(
            form_frame, text=txt_chan_lbl, fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_chan, "label")
        lbl_chan.grid(row=1, column=0, sticky=tk.W, pady=8)

        self.fields["channel"] = tk.Entry(form_frame, width=30)
        self.fields["channel"].insert(0, "6")
        self.apply_cyber_theme(self.fields["channel"], "entry")
        self.fields["channel"].grid(row=1, column=1, pady=8, padx=15)

        txt_band_lbl = "نطاق التردد المستهدف بالعملية:"
        lbl_band = tk.Label(
            form_frame, text=txt_band_lbl, fg=self.fg_text, bg=self.bg_main
        )
        self.apply_cyber_theme(lbl_band, "label")
        lbl_band.grid(row=2, column=0, sticky=tk.W, pady=8)

        self.combo_band = ttk.Combobox(form_frame, state="readonly", width=28)
        self.configure_combobox_style(self.combo_band, ["2G", "5G"])
        self.combo_band.grid(row=2, column=1, pady=8, padx=15)

        btn_frame = tk.Frame(self.root, bg=self.bg_main)
        btn_frame.pack(pady=25, fill=tk.X, padx=40)

        self.btn_session = tk.Button(
            btn_frame, text="🚀 إنشاء نفق الجلسة واستدعاء الحساسات",
            command=self.validate_and_spawn_mission_control
        )
        self.apply_cyber_theme(self.btn_session, "button", alert_style=True)
        self.btn_session.pack(fill=tk.X, padx=30)

        txt_init_status = "📥 بانتظار اختيار الأكسس وتلقيم معلمات القذف..."
        self.status_var = tk.StringVar(value=txt_init_status)
        lbl_status = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN,
            anchor=tk.W, font=("Arial", 10, "bold"), fg=self.fg_primary, bg=self.bg_entry
        )
        self.apply_cyber_theme(lbl_status, "label")
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def _trigger_live_heartbeat_check(self, _event=None):
        """إطلاق خيط خلفي صامت لتشغيل حساس الـ SSH وتحديث ملصق الحالة السفلي تلقائياً"""
        ap_idx = self.combo_ap.current()
        if ap_idx == -1 or not self.hardware_list:
            return

        selected_ap = self.hardware_list[ap_idx]
        ap_ip = selected_ap.get("bssid")
        ap_name = selected_ap.get("essid")

        msg_chk = f"🔄 جاري استجواب نبض العتاد للهدف [{ap_name}]..."
        self.status_var.set(self.process_mixed_text_safely(msg_chk))

        threading.Thread(
            target=self._async_heartbeat_worker,
            args=(ap_ip, ap_name),
            daemon=True
        ).start()

    def _async_heartbeat_worker(self, ip: str, name: str):
        """العامل الخلفي المعزول للاتصال الحقيقي وتوليد الـ Live Status"""
        factory = OpWrtSSHFactory(ip=ip, password="root")
        is_alive = factory.verify_ssh_heartbeat()

        if is_alive:
            msg = f"🟢 متصل وجاهز للعمليات - Target: {name} | IP: {ip}"
            self.root.after(0, lambda: self.status_var.set(self.process_mixed_text_safely(msg)))
        else:
            msg = f"🛑 فشل الاتصال بالراوتر! العتاد طافئ أو الـ SSH معطل للهدف [{name}]"
            self.root.after(0, lambda: self.status_var.set(self.process_mixed_text_safely(msg)))

    def validate_and_spawn_mission_control(self):
        """دالة خطافية فارغة يتم استبدالها وحقنها حياً عبر وسيط الملاحة والتحكم"""


if __name__ == "__main__":
    root_window = tk.Tk()
    app = AeroCageStrikeGUI(root_window)
    root_window.mainloop()
