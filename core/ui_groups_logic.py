#!/usr/bin/env python3
"""
File Name: ui_groups_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_groups_logic.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Business Logic Controller for AeroCageGroupsGUI.
             Manages asynchronous thread-safe metadata filtration for targets.
"""

import threading
import tkinter as tk


# pylint: disable=too-few-public-methods
class GroupsGUIController:
    """
    Main Controller Component for target groups.
    Decouples persistent file transactions from dynamic visualization updates.
    """

    def __init__(self, view_subsystem):
        """تهيئة معالج أحداث المجموعات التكتيكية وتوثيق الذاكرة الكاش لـ RAM"""
        self.view = view_subsystem

    def load_groups_async(self):
        """إشعال وتفريع خيط المعالجة المعزول لمنع قفل واجهة المستخدم الرسومية"""
        selected_type = self.view.combo_group.get()
        msg = f"🔄 جاري جلب وفرز السجلات لـ {selected_type} من قاعدة البيانات..."
        self.view.status_var.set(self.view.process_mixed_text_safely(msg))
        self.view.btn_refresh.config(state=tk.DISABLED)

        threading.Thread(
            target=self._fetch_and_render_worker,
            args=(selected_type,),
            daemon=True
        ).start()

    def _fetch_and_render_worker(self, group_type):
        """خيط العمل الخلفي المطور - يفرز السجلات ويعزل الأكسسات المضافة حياً عن شبكات الجو"""
        try:
            self.view.root.after(0, lambda: self.view.clear_treeview_records(self.view.tree))

            targets = self.view.db_manager.get_all_active_targets()
            rendered_count = 0
            for target in targets:
                bssid = target.get("bssid", "غير معروف")
                essid = target.get("essid", "مخفي")
                channel = target.get("channel", "1")
                power = target.get("power", -100)
                status = target.get("status", "discovered")

                if "أجهزة الترسانة" in group_type:
                    if status != "Hardware_AP_Active":
                        continue
                else:
                    if status == "Hardware_AP_Active":
                        continue
                    if "أهداف عالية الأهمية" in group_type and int(power) < -60:
                        continue

                row_data = (bssid, essid, channel, f"{power} dBm", status)
                self.view.root.after(0, self._append_row_to_tree, row_data)
                rendered_count += 1

            msg = f"📥 تم تحميل {rendered_count} سجل بنجاح من قاعدة البيانات."
            self.view.root.after(
                0,
                lambda: self.view.status_var.set(self.view.process_mixed_text_safely(msg))
            )
        except (ValueError, KeyError, AttributeError, SystemError) as e:
            err_msg = f"🔴 خطأ فرز المجموعات: {e}"
            self.view.root.after(
                0,
                lambda: self.view.status_var.set(self.view.process_mixed_text_safely(err_msg))
            )
        finally:
            self.view.root.after(0, lambda: self.view.btn_refresh.config(state=tk.NORMAL))

    def _append_row_to_tree(self, row_data: tuple):
        """حقن الصفوف المصفاة داخل جدول العرض الرسومي من الخيط القياسي للواجهة"""
        self.view.tree.insert("", tk.END, values=row_data)


if __name__ == "__main__":
    print("[+] Tactical Groups UI Controller subsystem verified.")
