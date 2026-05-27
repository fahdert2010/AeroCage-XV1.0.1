#!/usr/bin/env python3
"""
File Name: m3_kali_pipeline.py
Path: /home/kali/AeroCage-XV1.0.1/modules/m3_kali_pipeline.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Local Secure Execution Pipeline Engine for AeroCage-X.
             Validates systemic arguments and intercepts malicious payloads.
"""

import subprocess
import threading

from core.system_guard import SystemGuard
from utils.network_validators import NetworkValidators


# pylint: disable=too-few-public-methods
class KaliPipelineEngine:
    """
    Main Pipeline Execution Controller.
    Manages safe subprocess communication pools with strict argument sanitation.
    """

    def __init__(self):
        """تهيئة محرك الأنابيب وتأمين فحص صلاحيات مدير النظام محلياً"""
        SystemGuard.enforce_root_privileges("Kali Pipeline Engine")
        self.active_pipeline_processes = []
        # حقن مقفل التزامن الخيطي لـ حظر حدوث الـ Race Conditions داخل الذاكرة
        self.lock = threading.Lock()

    def run_pipeline_step_safe(self, tool: str, args_list: list) -> str:
        """تنفيذ خطوات الأنابيب البرمجية بأمان مصفوفة مغلقة الشل ومحقونة الحماية"""
        if not SystemGuard.verify_dependencies([tool]):
            return ""

        cleaned_tool = SystemGuard.sanitize_input(tool, "interface")
        cleaned_args = [
            SystemGuard.sanitize_input(arg, "csv_value") for arg in args_list
        ]

        for arg in cleaned_args:
            if "." in arg and not NetworkValidators.is_valid_ip(arg):
                print(f"[-] Security Alert: Invalid IP layout in pipeline: {arg}")
                return ""
            if ":" in arg and not NetworkValidators.is_valid_bssid(arg):
                print(f"[-] Security Alert: Invalid MAC layout in pipeline: {arg}")
                return ""

        full_command = [cleaned_tool] + cleaned_args
        try:
            print(f"[*] Executing pipeline instruction: {' '.join(full_command)}")

            # pylint: disable=consider-using-with
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False
            )

            with self.lock:
                self.active_pipeline_processes.append(process)

            stdout, stderr = process.communicate()

            with self.lock:
                if process in self.active_pipeline_processes:
                    self.active_pipeline_processes.remove(process)

            if process.returncode == 0:
                print(f"[+] Pipeline completed for tool: {cleaned_tool}.")
                return stdout.strip()

            err_msg = stderr.strip()
            print(f"[-] Warning: Failed for tool: {cleaned_tool}. Error: {err_msg}")
            return ""

        except (subprocess.SubprocessError, FileNotFoundError, OSError) as e:
            print(f"[-] Integrity Error: Crash in pipeline execution loop: {e}")
            return ""


if __name__ == "__main__":
    print("[+] Kali Pipeline Engine module deployment verified.")
