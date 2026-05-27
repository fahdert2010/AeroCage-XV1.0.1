#!/usr/bin/env python3
"""
File Name: network_validators.py
Path: /home/kali/AeroCage-XV1.0.1/utils/network_validators.py
Created Date: 2026-05-25
Version: 1.0.1
Description: Network Inputs and Assets Validation Engine for AeroCage-X.
             Implements strict mathematical regex verification for IPs and MACs.
"""

import re


class NetworkValidators:
    """
    Main Network Validators Object.
    Provides utility methods for validating corporate IPv4 and BSSID boundaries.
    """
    # تحصين الأنماط التعبيرية ومحددات الحواف الصارمة لمنع ثغرات التجاوز النصي
    _BSSID_STRICT_REGEX = re.compile(
        r'^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$'
    )
    # تعبير رياضي صارم يضمن أن أرقام الـ IPv4 تقع حصراً بين 0 و 255 لكل مقطع
    _IP_STRICT_REGEX = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    )
    # تعبير مساعد لاقتناص الماك أدرس من النصوص الطويلة أو سجلات tshark
    _BSSID_GLOBAL_REGEX = re.compile(
        r'\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b'
    )

    @classmethod
    def is_valid_bssid(cls, bssid: str) -> bool:
        """التحقق الصارم الكامل من صحة صيغة الماك أدرس الفردي لمنع الصدمات"""
        if not bssid or not isinstance(bssid, str):
            return False
        return bool(cls._BSSID_STRICT_REGEX.fullmatch(bssid.strip()))

    @classmethod
    def is_valid_ip(cls, ip: str) -> bool:
        """التحقق الرياضي الصارم من صحة نطاقات الـ IPv4 الملقمة للأنابيب"""
        if not ip or not isinstance(ip, str):
            return False
        return bool(cls._IP_STRICT_REGEX.fullmatch(ip.strip()))

    @classmethod
    def extract_bssids_from_text(cls, text: str) -> list:
        """اقتناص كافة عينات الماك أدرس المتواجدة داخل كتل النصوص الضخمة"""
        if not text or not isinstance(text, str):
            return []
        return cls._BSSID_GLOBAL_REGEX.findall(text)


if __name__ == "__main__":
    print("[+] Network Validators module validation verified.")
    # فحوصات ذاتية صارمة للتأكد من سحق ثغرات عناوين الـ IP الملوثة
    assert NetworkValidators.is_valid_ip("192.168.1.1") is True
    assert NetworkValidators.is_valid_ip("999.888.777.666") is False
    assert NetworkValidators.is_valid_bssid("AA:BB:CC:DD:EE:FF") is True
    print("[+] All strict mathematical network checks passed successfully.")
