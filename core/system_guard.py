#!/usr/bin/env python3
"""
File Name: system_guard.py
Path: /home/kali/AeroCage-XV1.0.1/core/system_guard.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Cyber Security Guard Module for AeroCage-X. Handles privileges,
             input sanitization, and cryptographically secure token generation.
"""

import os
import sys
import shutil
import secrets
import tkinter as tk
from tkinter import messagebox


class SystemGuard:
    """
    Main Security Guard Object.
    Provides static protection mechanisms and system validation pipelines.
    """

    @staticmethod
    def enforce_root_privileges(module_name: str, graphical: bool = False):
        """حارس صلاحيات الـ Root القياسي - يمنع العمليات العمياء ويغلق السكربت فوراً"""
        if os.geteuid() != 0:
            msg = f"[-] خطأ أمني فادح: [{module_name}] يتطلب صلاحيات مدير النظام (sudo)."
            if graphical:
                try:
                    root_err = tk.Tk()
                    root_err.withdraw()
                    err_title = "AeroCage-X | خطأ صلاحيات تكتيكي"
                    err_msg = f"{msg}\n\nيرجى إعادة تشغيل الأداة باستخدام أمر: sudo"
                    messagebox.showerror(err_title, err_msg)
                    root_err.destroy()
                except tk.TclError:
                    # معالجة فشل تشغيل الواجهة الرسومية في بيئات الطرفية الصافية أو SSH
                    print("[-] Graphical environment not available for root warning dialog.")

            print(msg)
            sys.exit(1)

    @staticmethod
    def verify_dependencies(tools: list) -> bool:
        """التحقق العتادي الصارم من توفر أدوات كالي الخارجية قبل إطلاق العمليات"""
        for tool in tools:
            if shutil.which(tool) is None:
                print(f"[-] خطأ نظامي حرج: الأداة '{tool}' مفقودة في بيئة كالي.")
                return False
        return True

    @staticmethod
    def sanitize_input(user_input: str, input_type: str = "alphanumeric") -> str:
        """مطهر المدخلات التكتيكي العتادي - القضاء التام على ثغرات الـ Injection"""
        if not user_input:
            return ""
        user_input = user_input.strip()

        if input_type == "interface":
            # السماح فقط بالأحرف والأرقام ورموز الواجهات القياسية
            return "".join(ch for ch in user_input if ch.isalnum() or ch in "._-")

        if input_type == "bssid":
            # تطهير الماك أدرس تماماً والسماح فقط بصيغ الـ Hex والفواصل
            return "".join(ch for ch in user_input if ch.isalnum() or ch in ":-")

        if input_type == "csv_value":
            # حماية ملفات الـ CSV من التلاعب البرمجي والرموز التنفيذية الخبيثة
            if user_input.startswith(('=', '+', '-', '@')):
                user_input = "'" + user_input
            return "".join(ch for ch in user_input if ch.isalnum() or ch in " ._-@:")

        # الافتراضي: تصفية النصوص العادية لمنع الرموز الغريبة
        return "".join(ch for ch in user_input if ch.isalnum() or ch in " ._-")

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """توليد مفاتيح وتوكنات تشفير عشوائية حصينة سيبرانياً تضمن دقة الأطوال الفردية"""
        # حساب دقيق لعدد البايتات المطلوبة لإنتاج السلسلة النصية بدون نقص منطقي
        num_bytes = (length + 1) // 2
        token = secrets.token_hex(num_bytes)
        return token[:length]


if __name__ == "__main__":
    print("[+] حارس النظام المركزي وخط الدفاع الأول (System Guard) نشط.")
    # اختبار تشغيلي صامت للتحقق من كفاءة فلاتر التطهير والحماية
    assert SystemGuard.sanitize_input("wlan0; rm -rf /", "interface") == "wlan0"
    assert SystemGuard.sanitize_input("=cmd|' /C calc'!A1", "csv_value") == "'cmd /C calc!A1"
    assert len(SystemGuard.generate_secure_token(7)) == 7
    print("[+] نجحت كافة الفحوصات الذاتية التكتيكية للحارس المركزي.")
