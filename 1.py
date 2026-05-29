test_error_messenger.py
import pytest
from utils.error_messenger import ErrorMessenger

def test_error_messenger_methods_exist():
    assert hasattr(ErrorMessenger, "show_error")
    assert hasattr(ErrorMessenger, "show_warning")
    assert hasattr(ErrorMessenger, "show_info")

test_theme_plugin.py
import pytest
import tkinter as tk
from modules.theme_plugin import ThemePlugin

def test_theme_plugin_colors_fonts():
    root = tk.Tk()
    theme = ThemePlugin(root)
    assert theme.get_color("background") == "#1e1e1e"
    assert isinstance(theme.get_font("small"), tuple)
    root.destroy()

test_language_processor.py
import pytest
from utils.language_processor import LanguageProcessor

def test_translate_arabic_title():
    lp = LanguageProcessor(default_lang="ar")
    assert "الواجهة الموحدة" in lp.translate("title", raw=True)

def test_translate_english_title():
    lp = LanguageProcessor(default_lang="en")
    assert "Unified Launcher" in lp.translate("title")

def test_process_rtl_short_word():
    lp = LanguageProcessor()
    assert lp.process_rtl("عربي") == "عربي"

┌──(kali㉿kali)-[~/AeroCage-XV4.0.0]
└─$ pytest -v tests/

============================================= test session starts =============================================
platform linux -- Python 3.13.12, pytest-9.0.2, pluggy-1.6.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: /home/kali/AeroCage-XV4.0.0
plugins: anyio-4.12.1, typeguard-4.4.4
collected 5 items                                                                                             

tests/test_error_messenger.py::test_error_messenger_methods_exist PASSED                                [ 20%]
tests/test_language_processor.py::test_translate_arabic_title PASSED                                    [ 40%]
tests/test_language_processor.py::test_translate_english_title PASSED                                   [ 60%]
tests/test_language_processor.py::test_process_rtl_short_word PASSED                                    [ 80%]
tests/test_theme_plugin.py::test_theme_plugin_colors_fonts PASSED                                       [100%]

============================================== 5 passed in 0.17s ==============================================
                                                                                                               
┌──(kali㉿kali)-[~/AeroCage-XV4.0.0]

