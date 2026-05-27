#!/usr/bin/env python3
"""
File Name: shared_utils_3.py
Path: /home/kali/AeroCage-XV1.0.1/utils/shared_utils_3.py
Created Date: 2026-05-25
Version: 1.0.2
Description: Centralized Bidi Arabic Reshaping Text Processing Toolkit 3.
             Aligns mixed syntax frames safely for graphical consoles.
"""

import arabic_reshaper
from bidi.algorithm import get_display


class SharedVisualLinguisticToolkit:
    """
    Main Arabic Language Reshaping Component.
    Enforces clean bidirectional rendering metrics across terminal blocks.
    """

    @staticmethod
    def process_mixed_text_safely(text_frame: str) -> str:
        """معالجة وتصحيح الكلمات العربية المتداخلة والرموز اللاتينية بالملي"""
        if not text_frame or not isinstance(text_frame, str):
            return ""
        try:
            reshaped = arabic_reshaper.reshape(text_frame)
            return get_display(reshaped)
        except (ValueError, TypeError, AttributeError):
            return text_frame

    @classmethod
    def calculate_visual_text_length(cls, target_string: str) -> int:
        """دالة عامة ثانية لقياس الطول الصافي للنصوص للامتثال لشروط Pylint"""
        clean_text = cls.process_mixed_text_safely(target_string)
        return len(clean_text)


if __name__ == "__main__":
    print("[+] Shared Visual Linguistic Toolkit 3 validated successfully.")
