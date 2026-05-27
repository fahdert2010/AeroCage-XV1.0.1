#!/usr/bin/env python3
"""
File Name: ui_access_points_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_access_points_logic.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Business Logic Controller for AeroCageAccessPointsGUI.
             Manages dynamic database queries and thread-safe dataset mapping.
"""

import threading
import tkinter as tk
from tkinter import messagebox


class AccessPointsController:
    """
    Main Controller Object for the Access Points Subsystem.
    Handles non-blocking asynchronous network queries and targets filtration.
    """

    def __init__(self, view_subsystem):
        """تهيئة معالج الأحداث وحقن مرجع واجهة العرض الرسومية الموحد"""
        self.view = view_subsystem

    def refresh_ap_list_async(self):
        """تجهيز وإطلاق الخيط الخلفي لجلب البيانات لمنع تجميد الواجهة الرسومية"""
        msg = "🔄 جاري جلب وتحديث سجلات نقاط البث من قاعدة البيانات..."
        self.view.status_var.set(self.view.process_mixed_text_safely(msg))
        self.view.btn_refresh.config(state=tk.DISABLED)
        threading.Thread(target=self._fetch_ap_worker, daemon=True).start()

    def _fetch_ap_worker(self):
        """خيط العمل الخلفي - جلب البيانات وتنقيتها جراحياً من راوترات الترسانة"""
        try:
            self.view.root.after(0, lambda: self.view.clear_treeview_records(self.view.tree))

            targets = self.view.db_manager.get_all_active_targets()
            rendered_count = 0
            for target in targets:
                # خط الدفاع التكتيكي: عزل واستبعاد راوترات العتاد الخاصة بك وحظر عرضها كأهداف
                if target.get("status") == "Hardware_AP_Active":
                    continue

                row_data = (
                    target.get("bssid", "غير معروف"),
                    target.get("essid", "مخفي"),
                    target.get("channel", "1"),
                    f"{target.get('power', -100)} dBm",
                    target.get("last_seen", "غير محدد")
                )

                self.view.root.after(0, self._append_row_to_tree, row_data)
                rendered_count += 1

            msg = f"📥 تم تحميل {rendered_count} نقطة بث لاسلكية بنجاح."
            self.view.root.after(
                0,
                lambda: self.view.status_var.set(self.view.process_mixed_text_safely(msg))
            )

        except (ValueError, KeyError, AttributeError, SystemError) as e:
            err_msg = f"🔴 خطأ جلب سجلات نقاط البث: {e}"
            self.view.root.after(
                0,
                lambda: self.view.status_var.set(self.view.process_mixed_text_safely(err_msg))
            )
        finally:
            self.view.root.after(0, lambda: self.view.btn_refresh.config(state=tk.NORMAL))

    def _append_row_to_tree(self, row_data: tuple):
        """دالة مساعدة مخصصة لتلقيم الصفوف داخلياً من خيط المعالجة الرئيسي"""
        self.view.tree.insert("", tk.END, values=row_data)

    def inject_selected_ap_to_strike(self):
        """تثبيت وعزل أرقام الماك أدرس للهدف اللاسلكي المختار وتطهير الرسائل من التخبيص"""
        selected_item = self.view.tree.selection()
        if not selected_item:
            warn_txt = "الرجاء اختيار نقطة بث من الجدول أولاً لتلقيمها!"
            messagebox.showwarning(
                self.view.process_mixed_text_safely("تنبيه تكتيكي لـ 1"),
                self.view.process_mixed_text_safely(warn_txt),
                parent=self.view.root
            )
            return

        item_values = self.view.tree.item(selected_item, "values")
        target_mac = item_values[0]
        target_name = item_values[1]

        # صياغة السطور بشكل نظيف وتمريرها للمشكل المركزي الصافي لمنع قفز الحروف واللغات
        suc_title = "تم التلقيم بنجاح للواجهة 1"
        suc_body = (
            f"تم تثبيت وعزل هدف الواجهة 1 في المنظومة\n\n"
            f"الاسم : {target_name}\nالماك : {target_mac}"
        )

        messagebox.showinfo(
            self.view.process_mixed_text_safely(suc_title),
            self.view.process_mixed_text_safely(suc_body),
            parent=self.view.root
        )


if __name__ == "__main__":
    print("[+] Access Points UI Controller subsystem blueprint verified.")
