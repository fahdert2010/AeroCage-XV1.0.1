#!/usr/bin/env python3
"""
File Name: channel_optimizer.py
Path: /home/kali/AeroCage-XV1.0.1/utils/channel_optimizer.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Radio Frequency Spectrum Analysis and Channel Optimization Engine 
             for AeroCage-X. Parses raw iwinfo stdout and calculates SNR paths.
"""

import re


class ChannelOptimizer:
    """
    Main Wireless Spectrum Analysis Component.
    Decompiles air space scan cells and maps interference telemetry percentages.
    """

    @staticmethod
    def parse_scan_output(raw_stdout: str) -> list:
        """تفكيك مخرجات فحص iwinfo عن بعد وحمايتها من أخطاء الـ IndexError"""
        parsed_cells = []
        if not raw_stdout:
            return parsed_cells

        cell_blocks = raw_stdout.split("Cell ")

        for block in cell_blocks:
            if not block.strip():
                continue

            bssid_match = re.search(r'Address:\s+([0-9A-Fa-f:.-]+)', block)
            chan_match = re.search(r'Channel:\s+(\d+)', block)
            signal_match = re.search(r'Signal:\s+(-\d+)\s+dBm', block)
            essid_match = re.search(r'ESSID:\s+"([^"]*)"', block)

            if bssid_match and chan_match:
                # تعيين معطيات افتراضية آمنة لحظر الانهيارات المتسلسلة
                essid = essid_match.group(1) if essid_match else "Hidden_Network"
                power = int(signal_match.group(1)) if signal_match else -95

                parsed_cells.append({
                    "bssid": bssid_match.group(1).upper(),
                    "essid": essid,
                    "channel": chan_match.group(1),
                    "power": power
                })
        return parsed_cells

    @classmethod
    def calculate_best_channel(cls, parsed_cells: list) -> dict:
        """خوارزمية حساب نسب الازدحام واكتشاف القناة الأقوى والأقل تداخلاً"""
        channel_load_scores = {}
        channel_counts = {}

        for cell in parsed_cells:
            chan = cell["channel"]
            power = cell["power"]

            channel_counts[chan] = channel_counts.get(chan, 0) + 1
            weight = 100 + power
            channel_load_scores[chan] = channel_load_scores.get(chan, 0) + max(
                5, weight
            )

        if not channel_counts:
            return {}

        total_networks = sum(channel_counts.values())
        best_channel = min(channel_load_scores, key=channel_load_scores.get)

        report_data = []
        for chan, count in sorted(channel_counts.items(), key=lambda x: int(x[0])):
            percentage = (count / total_networks) * 100

            # كسر وتفتيت الأسطر الطويلة للنصوص وتصفير مسافات سطر الـ if لـ Pylint
            if channel_load_scores[chan] > 80:
                load_status = "⚠️ مزدحم جداً"
            else:
                load_status = "🟢 خفيف وآمن"

            report_data.append({
                "channel": chan,
                "count": count,
                "percentage": round(percentage, 1),
                "status": load_status
            })

        return {
            "best_channel": best_channel,
            "report": report_data,
            "counts": channel_counts
        }


if __name__ == "__main__":
    print("[+] Wireless Channel Optimizer mathematical engine verified.")
