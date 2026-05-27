#!/usr/bin/env python3
"""
File Name: strike_panel_ui.py
Path: /home/kali/AeroCage-XV1.0.1/modules/strike_panel_ui.py
Created Date: 2026-05-25
Version: 1.0.3
Description: Strike Panel GUI Adapter Module for AeroCage-X.
             Eliminates code redundancy by inheriting clean controller models.
"""

import tkinter as tk

from core.system_guard import SystemGuard
from core.ui_strike import AeroCageStrikeGUI


class AeroCageStrikePanelGUI(AeroCageStrikeGUI):
    """
    Lean Visual View Component.
    Acts as an entry point adapter for the secure operational strike subsystem.
    """

    def __init__(self, root: tk.Tk):
        """تهيئة الواجهة وتمرير المشيد المركزي لأب الـ UI والمصلح لغوياً"""
        SystemGuard.enforce_root_privileges("AeroCage Strike Panel GUI", graphical=True)
        super().__init__(root)


if __name__ == "__main__":
    root_window = tk.Tk()
    app = AeroCageStrikePanelGUI(root_window)
    root_window.mainloop()
