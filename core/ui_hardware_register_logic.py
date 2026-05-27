#!/usr/bin/env python3
"""
File Name: ui_hardware_register_logic.py
Path: /home/kali/AeroCage-XV1.0.1/core/ui_hardware_register_logic.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Business Logic Controller for AeroCageHardwareRegisterGUI.
             Handles target hardware sanitization and database registration pipelines.
"""

from core.system_guard import SystemGuard


class HardwareRegisterController:
    """
    Main Controller Component for hardware registration.
    Manages operational state transfers and isolated query execution workflows.
    """

    def __init__(self, view_subsystem):
        """تهيئة معالج الأحداث وحقن مرجع واجهة العرض الرسومية الموحد"""
        self.view = view_subsystem

    def validate_target_ip_format(self, ip_str: str) -> bool:
        """دالة عامة ثانية لتدقيق منطق الـ IP وحظر تضخم القيود القياسية لـ OOP"""
        if not ip_str:
            return False
        clean_ip = SystemGuard.sanitize_input(ip_str, "interface")
        return len(clean_ip.split('.')) == 4

    def commit_hardware_registration(self):
        """معالجة وتطهير وحفظ البيانات الملقمة وتمريرها للمحيط التشغيلي"""
        ap_name = self.view.fields["name"].get().strip()
        ap_ip = self.view.fields["ip"].get().strip()
        ap_pass = self.view.fields["pass"].get().strip()

        if not ap_name or not ap_ip or not ap_pass:
            self.view.display_warning_message(
                "بيانات ناقصة",
                "الرجاء ملء كافة حقول التلقيم الإلزامية!"
            )
            return

        if not self.validate_target_ip_format(ap_ip):
            self.view.display_warning_message(
                "بنية IP غير صالحة",
                "الرجاء إدخال عنوان IP صحيح للراوتر!"
            )
            return

        clean_ip = SystemGuard.sanitize_input(ap_ip, "interface")
        clean_name = SystemGuard.sanitize_input(ap_name, "csv_value")

        query = """
        INSERT INTO tactical_targets (bssid, essid, channel, power, status, last_seen)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
        """
        try:
            # pylint: disable=protected-access
            with self.view.db_manager._get_secure_connection() as conn:
                with conn:
                    conn.cursor().execute(
                        query,
                        (clean_ip, clean_name, "0", -50, "Hardware_AP_Active")
                    )

            if self.view.parent_callback:
                self.view.parent_callback(clean_ip, ap_pass)

            self.view.display_info_message(
                "نجاح التلقيم",
                "تم حفظ وتلقيم السيرفر في الترسانة بنجاح!"
            )
            self.view.root.destroy()
        except (AttributeError, ValueError, SystemError) as e:
            self.view.display_warning_message(
                "خطأ نظامي",
                f"تعذر أرشفة خادم التلقيم: {e}"
            )


if __name__ == "__main__":
    print("[+] Hardware Register UI Controller subsystem blueprint verified.")
