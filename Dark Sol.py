# DPI Setup
import ctypes
ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
# Imports
import os, sys, threading, pyautogui, time, ctypes, pathlib, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QMessageBox, QProgressBar, QStackedWidget, QComboBox, QLineEdit, QDialog, QDialogButtonBox, QScrollArea, QCheckBox, QFrame
from pyscreeze import ImageNotFoundException as pyscreeze_ImageNotFoundException
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PIL import Image, ImageDraw, ImageGrab
from mousekey import MouseKey
from pynput import keyboard
import numpy as np
from copy import deepcopy

mkey = MouseKey()
mkey.enable_failsafekill('ctrl+e')
local_appdata_directory = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Dark Sol"
CONFIG_PATH = local_appdata_directory / "Dark Sol config.json"
os.makedirs(local_appdata_directory, exist_ok=True)

"""
# *Tasks (For Mr. Bored)

# Nessesary for Release:
1. Add amount button logic (Necessary for release) (Completed?)
2. Add item selection for each potion / presets (Necessary for release)
3. Make auto add checks ignore manual click slots (lucky potions) (Necessary for release)
4. Implement Semi-Auto and Manual Calibration modes (Necessary for release)
5. Make confidence for template find be specific per template (Necessary for release)

# Might be added for Release:
6. Add settings tab functionality (Might be added by release)

# Optional for Release:
7. Fix other widgets not closing properly
8. Add multi template for single location
9. Add actual logger
10. Make plugins system
11. Add theme tab functionality
12. # Able to handle corrupt config
13. Add config backups
14. Add ability to export/import presets
15. Add ability to change hotkeys
"""
# Loading Screen
class loading_thread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str, int)
    def run(self):
        self.progress.emit("Settings Import Properties (%p%)", 0)
        global easyocr, reader
        self.progress.emit("Import Properties Set (%p%)", 1)
        self.progress.emit("Importing EasyOCR (%p%)", 1)
        import easyocr
        self.progress.emit("EasyOCR Imported (%p%)", 2)
        self.progress.emit("Initializing EasyOCR (%p%)", 2)
        reader = easyocr.Reader(['en'])
        self.progress.emit("EasyOCR Initialized (%p%)", 3)
        self.finished.emit()

class loading_screen(QWidget):
    def __init__(self):
        super().__init__()
        parts_to_load = 3
        self.loading_bar = QProgressBar(self)
        self.setWindowTitle("Loading Dark Sol")
        self.setStyleSheet(""" QProgressBar {background-color: black; color: white; border-radius: 5px; border: 1px solid black; font-size: 20px; height: 40px;} QProgressBar::chunk {background-color: lime; }""")
        self.setGeometry(0, 0, 500, 100)
        self.loading_bar.setGeometry(0, 0, 500, 100)
        self.loading_bar.setRange(0, parts_to_load)
        self.loading_bar.setValue(0)
        self.loading_bar.setFormat("Loading Dark Sol (You should not see this)")
        self.loading_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.loader_thread = loading_thread()
        self.loader_thread.progress.connect(self.update_bar)
        self.loader_thread.finished.connect(self.on_loaded)
        self.loader_thread.start()

    def update_bar(self, text, value):
        self.loading_bar.setFormat(text)
        self.loading_bar.setValue(value)

    def on_loaded(self):
        self.close()
        main_window = Dark_Sol()
        main_window.show()

# Main Dark Sol Script
class Dark_Sol(QMainWindow):
    start_macro_signal = pyqtSignal()
    stop_macro_signal = pyqtSignal()

    def __init__(self):
        # Create main window
        super().__init__()
        self.initalize_config()
        self.setWindowTitle("Dark Sol")
        self.setGeometry(100, 100, 400, 100)
        # Create Tabs
        self.tabs_widget = QTabWidget()
        self.main_tab = QWidget()
        self.presets_tab = QWidget()
        self.calibrations_tab = QWidget()
        self.theme_tab = QWidget()
        self.settings_tab = QWidget()
        # Create Main Tab Elements
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.status_label = QLabel("Status: Stopped")
        # Create Presets Tab Elements
        self.current_preset = config["current_preset"]
        self.preset_selector = QComboBox()
        self.presets_tab_scroller = QScrollArea()
        self.presets_tab_content = QWidget()
        # Create Calibration Tab Elements
        self.calibration_mode = "auto"
        self.calibration_mode_button = QPushButton("Current Mode: Automatic Calibration")
        # Auto Calibration mode
        self.find_add_button = QPushButton("Find Add Buttons")
        self.find_amount_box = QPushButton("Find Amount Boxes")
        self.find_auto_add_button = QPushButton("Find Auto Add Button")
        self.find_craft_button = QPushButton("Find Craft Button")
        self.find_search_bar = QPushButton("Find Search Bar")
        self.find_potion_selection_button = QPushButton("Find Potion Selection Button")
        # Semi Auto Calibration mode
        self.set_add_button_template = QPushButton("Set Add Button Template")
        # Manual Calibration mode
        self.add_button_coordinates_selector = QWidget()
        self.add_button_coordinates_selector.setWindowTitle("Set Add Button Coordinates")
        self.add_button_coordinates_selector_layout = QVBoxLayout(self.add_button_coordinates_selector)
        self.set_add_button_coordinates = QPushButton("Set Add Button Coordinates", self)
        self.set_add_button_1_coordinates = QPushButton("Set Add Button 1 Coordinates")
        self.set_add_button_2_coordinates = QPushButton("Set Add Button 2 Coordinates")
        self.set_add_button_3_coordinates = QPushButton("Set Add Button 3 Coordinates")
        self.set_add_button_4_coordinates = QPushButton("Set Add Button 4 Coordinates")
        self.amount_box_coordinates_selector = QWidget()
        self.amount_box_coordinates_selector.setWindowTitle("Set Amount Box Coordinates")
        self.amount_box_coordinates_selector_layout = QVBoxLayout(self.amount_box_coordinates_selector)
        self.set_amount_box_coordinates = QPushButton("Set Amount Box Coordinates", self)
        self.set_amount_box_1_coordinates = QPushButton("Set Amount Box 1 Coordinates")
        self.set_amount_box_2_coordinates = QPushButton("Set Amount Box 2 Coordinates")
        self.set_amount_box_3_coordinates = QPushButton("Set Amount Box 3 Coordinates")
        self.set_amount_box_4_coordinates = QPushButton("Set Amount Box 4 Coordinates")
        self.set_auto_add_button_coordinates = QPushButton("Set Auto Add Button Coordinates")
        self.set_craft_button_coordinates = QPushButton("Set Craft Button Coordinates")
        self.set_search_bar_coordinates = QPushButton("Set Search Bar Coordinates")
        self.set_potion_selection_button_coordinates = QPushButton("Set Potion Selection Button Coordinates")
        #Status Label Setup
        self.mini_status_widget = QWidget()
        self.mini_status_label = QLabel("Stopped", self.mini_status_widget)
        # Create Running Variables
        self.auto_add_waitlist = []
        self.current_auto_add_potion = None
        self.macro_timer = QTimer(self)
        self.run_event = threading.Event()
        self.worker = None
        self.init_ui()
        
    def init_ui(self):
        # Initialize Tabs
        self.setCentralWidget(self.tabs_widget)
        self.tabs_widget.addTab(self.main_tab, "Main")
        self.tabs_widget.addTab(self.presets_tab, "Presets")
        self.tabs_widget.addTab(self.calibrations_tab, "Calibrations")
        self.tabs_widget.addTab(self.theme_tab, "Theme")
        self.tabs_widget.addTab(self.settings_tab, "Settings")
        # Set Main Tab Layout
        main_tab_vbox = QVBoxLayout()
        main_tab_hbox = QHBoxLayout()
        main_tab_hbox.addWidget(self.start_button)
        main_tab_hbox.addWidget(self.stop_button)
        main_tab_vbox.addWidget(self.status_label)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_tab_vbox.addLayout(main_tab_hbox)
        self.main_tab.setLayout(main_tab_vbox)
        #Set Presets Tab Layout
        self.preset_selector.addItems(list(config["item presets"].keys()) + ["Create New Preset"])
        self.preset_selector.setStyleSheet("color: cyan; background: #111; font-size: 24px; padding: 6px;")
        self.preset_selector.setMinimumHeight(52)
        self.preset_selector.blockSignals(True)
        self.preset_selector.setCurrentText(self.current_preset)
        self.preset_selector.blockSignals(False)
        self.presets_tab.setStyleSheet("""
            QWidget { background-color: black; }
            QLabel { color: cyan; font-size: 18px; }
            QCheckBox { color: cyan; font-size: 14px; }
            QScrollArea { border: 0px; }
        """)
        self.presets_tab_scroller.setFrameShape(QFrame.Shape.NoFrame)
        self.presets_tab_scroller.setWidgetResizable(True)
        self.presets_tab_scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.presets_tab_scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.presets_tab_main_vbox = QVBoxLayout()
        self.presets_tab_main_vbox.addWidget(self.preset_selector)
        self.presets_tab_main_vbox.addWidget(self.presets_tab_scroller)
        self.presets_tab.setLayout(self.presets_tab_main_vbox)
        self.presets_tab_content_layout = QVBoxLayout(self.presets_tab_content)
        self.presets_tab_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.presets_tab_scroller.setWidget(self.presets_tab_content)
        self.build_potions_ui()
        # Set Calibrations Tab Layout
        self.calibrations_tab_main_vbox = QVBoxLayout()
        self.calibrations_stack = QStackedWidget()
        self.calibration_mode_button.setToolTip("Switch between automatic and manual calibration mode.")
        # Auto Calibration Page
        auto_calibration_page = QWidget()
        auto_layout = QVBoxLayout(auto_calibration_page)
        auto_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        auto_layout.addWidget(self.find_add_button)
        auto_layout.addWidget(self.find_amount_box)
        auto_layout.addWidget(self.find_auto_add_button)
        auto_layout.addWidget(self.find_craft_button)
        auto_layout.addWidget(self.find_search_bar)
        auto_layout.addWidget(self.find_potion_selection_button)
        # Semi Auto Calibration Page
        semi_auto_calibration_page = QWidget()
        semi_auto_layout = QVBoxLayout(semi_auto_calibration_page)
        semi_auto_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        semi_auto_layout.addWidget(self.set_add_button_template)
        # Manual Calibration Page
        manual_calibration_page = QWidget()
        manual_layout = QVBoxLayout(manual_calibration_page)
        manual_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_1_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_2_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_3_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_4_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_1_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_2_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_3_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_4_coordinates)
        manual_layout.addWidget(self.set_add_button_coordinates)
        manual_layout.addWidget(self.set_amount_box_coordinates)
        manual_layout.addWidget(self.set_auto_add_button_coordinates)
        manual_layout.addWidget(self.set_craft_button_coordinates)
        manual_layout.addWidget(self.set_search_bar_coordinates)
        manual_layout.addWidget(self.set_potion_selection_button_coordinates)
        self.add_button_coordinates_selector.setStyleSheet("QWidget {background-color: black;} QPushButton {color: cyan;border: 2px solid cyan; border-radius: 6px; font-size: 30px;}")
        self.amount_box_coordinates_selector.setStyleSheet("QWidget {background-color: black;} QPushButton {color: cyan;border: 2px solid cyan; border-radius: 6px; font-size: 30px;}")
        self.add_button_coordinates_selector.adjustSize()
        self.amount_box_coordinates_selector.adjustSize()
        # Calibration Pages Setup
        self.calibrations_stack.addWidget(auto_calibration_page)       # index 0
        self.calibrations_stack.addWidget(semi_auto_calibration_page)  # index 1
        self.calibrations_stack.addWidget(manual_calibration_page)     # index 2
        self.calibrations_tab_main_vbox.addWidget(self.calibration_mode_button)
        self.calibrations_tab_main_vbox.addWidget(self.calibrations_stack)
        self.calibrations_stack.setCurrentIndex(0)
        self.calibrations_tab.setLayout(self.calibrations_tab_main_vbox)
        # Button Connectors
        self.calibration_mode_button.clicked.connect(lambda: self.switch_calibration_mode())
        self.set_add_button_coordinates.clicked.connect(lambda: self.add_button_coordinates_selector.show())
        self.set_amount_box_coordinates.clicked.connect(lambda: self.amount_box_coordinates_selector.show())
        self.find_add_button.clicked.connect(lambda: self.auto_find_image("add button.png", True, True, True))
        self.find_amount_box.clicked.connect(lambda: self.auto_find_image("amount box.png", True, True))
        self.find_auto_add_button.clicked.connect(lambda: self.auto_find_image("auto add button.png", True, bbox_required=True))
        self.find_craft_button.clicked.connect(lambda: self.auto_find_image("craft button.png", True))
        self.find_search_bar.clicked.connect(lambda: self.auto_find_image("cauldren search bar.png", True))
        self.find_potion_selection_button.clicked.connect(lambda: self.auto_find_image("heavenly potion potion selector button.png", True))
        self.preset_selector.currentTextChanged.connect(lambda: self.switch_preset(self.preset_selector.currentText()) if self.preset_selector.currentText() != "Create New Preset" else self.create_new_preset())
        #Status Label Setup
        self.mini_status_widget.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowTransparentForInput)
        self.mini_status_widget.setStyleSheet("background-color: black; border: 2px solid cyan; border-radius: 6px;")
        self.mini_status_label.setStyleSheet("color: cyan; font-size: 20px;")
        self.mini_status_qv = QVBoxLayout(self.mini_status_widget)
        self.mini_status_qv.setContentsMargins(0, 0, 0, 0)
        self.mini_status_qv.addWidget(self.mini_status_label)
        self.mini_status_label.adjustSize()
        self.mini_status_widget.adjustSize()
        self.mini_status_widget.move(600, 75)
        # Set Ui Theme
        self.setStyleSheet("""
            QMainWindow {background-color: black; }
            QTabWidget::pane { border: 0px; padding: 0px; margin: 0px; }
            QTabBar::tab { background-color: #222; }
            QTabBar::tab:selected { background-color: black; }
            QTabBar {color: cyan;}
            QWidget {background-color: black;}
            QPushButton {background-color: black; color: cyan; border-radius: 5px; border: 1px solid cyan; font-size: 30px;}
            QLabel {color: cyan; font-size: 50px;}
        """)
        # Setup  Hotkeys
        self.start_button.clicked.connect(self.start_macro)
        self.stop_button.clicked.connect(self.stop_macro)
        self.setup_hotkeys()
        
    def initalize_config(self):
        global config, hidden_config
        hidden_config = {
                    "positions": {
                        "add button 1": {"bbox": [757, 656, 837, 688], "center": [797, 672]},
                        "add button 2": {"bbox": [757, 711, 837, 743], "center": [797, 727]},
                        "add button 3": {"bbox": [757, 765, 837, 797], "center": [797, 781]},
                        "add button 4": {"bbox": [757, 794, 837, 826], "center": [797, 810]},
                        "amount box 1": [715, 672],
                        "amount box 2": [715, 726],
                        "amount box 3": [715, 780],
                        "amount box 4": [715, 810],
                        "potion selection button": [1146, 460],
                        "search bar": [1137, 381],
                        "auto add button": [707, 618],
                        "craft button": [573, 618],
                    },
                    "current_preset": "Main",

                    "item presets": {
                        "Main": {
                            "bound": {
                                "buttons to check": ["add button 1", "add button 2"],
                                "additional buttons to click": ["add button 4"],
                                "crafting slots": 4,
                                "instant craft": False,
                                "enabled": True,
                                "collapsed": True
                            },
                            "heavenly": {
                                "buttons to check": ["add button 2", "add button 3"],
                                "additional buttons to click": ["add button 1"],
                                "crafting slots": 5,
                                "instant craft": False,
                                "enabled": True,
                                "collapsed": True
                            },
                            "zeus": {
                                "buttons to check": ["add button 3"],
                                "additional buttons to click": ["add button 1", "add button 2"],
                                "crafting slots": 5,
                                "instant craft": False,
                                "enabled": True,
                                "collapsed": True
                            },
                            "poseidon": {
                                "buttons to check": ["add button 2"],
                                "additional buttons to click": ["add button 1"],
                                "crafting slots": 4,
                                "instant craft": False,
                                "enabled": True,
                                "collapsed": True
                            },
                            "hades": {
                                "buttons to check": ["add button 2"],
                                "additional buttons to click": ["add button 1"],
                                "crafting slots": 4,
                                "instant craft": False,
                                "enabled": True,
                                "collapsed": True
                            },
                            "warp": {
                                "buttons to check": ["add button 1", "add button 2", "add button 4", "add button 5", "add button 6"],
                                "additional buttons to click": ["add button 1", "add button 2"],
                                "crafting slots": 6,
                                "instant craft": False,
                                "enabled": False,
                                "collapsed": False
                            },
                            "protected": True
                        }
                    }
                    }
                    
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            
        else:
            config = hidden_config
        self.nice_config_save()

    def nice_config_save(self, ind=4):
        S = (str, int, float, bool, type(None))

        stack_ids = set()

        def d(o, l=0):
            p = " " * (ind * l)
            np = " " * (ind * (l + 1))

            def dump_simple_list(vals):
                return "[" + ", ".join(json.dumps(x) for x in vals) + "]"

            if isinstance(o, dict):
                oid = id(o)
                stack_ids.add(oid)
                try:
                    if not o:
                        return "{}"
                    it = list(o.items())
                    if len(it) <= 2 and all(isinstance(k, str) for k, _ in it) and all(
                        isinstance(v, S)
                        or (isinstance(v, (list, tuple)) and len(v) <= 6 and all(isinstance(x, S) for x in v))
                        for _, v in it
                    ):
                        parts = []
                        for k, v in it:
                            if isinstance(v, (list, tuple)):
                                parts.append(f"{json.dumps(k)}: {dump_simple_list(list(v))}")
                            else:
                                parts.append(f"{json.dumps(k)}: {json.dumps(v)}")
                        return "{" + ", ".join(parts) + "}"
                    return "{\n" + "\n".join(
                        f"{np}{json.dumps(k)}: {d(v, l + 1)}{',' if i < len(it) - 1 else ''}" for i, (k, v) in enumerate(it)
                    ) + f"\n{p}}}"
                finally:
                    stack_ids.discard(oid)
            if isinstance(o, (list, tuple)):
                oid = id(o)
                stack_ids.add(oid)
                try:
                    a = list(o)
                    if len(a) <= 6 and all(isinstance(x, S) for x in a):
                        return dump_simple_list(a)
                    if not a:
                        return "[]"
                    return "[\n" + "\n".join(
                        f"{np}{d(v, l + 1)}{',' if i < len(a) - 1 else ''}" for i, v in enumerate(a)
                    ) + f"\n{p}]"
                finally:
                    stack_ids.discard(oid)
            return json.dumps(o)

        text = d(config) + "\n"
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(text)
    
    def update_config(self, key, new_value):
        config[key] = new_value
        self.nice_config_save()

    global data
    data = {
            "img scales": {"add button.png": {"scale": 1.25, "resolution": (1920, 1080), "position name": ["add button 1", "add button 2", "add button 3", "add button 4"]},
                                "amount box.png": {"scale": 1.25, "resolution": (1920, 1200), "position name": ["amount box 1", "amount box 2", "amount box 3", "amount box 4"]},
                                "auto add button.png": {"scale": 1.25, "resolution": (1920, 1200), "position name": "auto add button"},
                                "craft button.png": {"scale": 1.25, "resolution": (1920, 1200), "position name": "craft button"},
                                "cauldren search bar.png": {"scale": 1.25, "resolution": (1920, 1200), "position name": "search bar"},
                                    "heavenly potion potion selector button.png": {"scale": 1.25, "resolution": (1920, 1200), "position name": "potion selection button"},
                            },
            "item data": {
                    "bound": {
                        "name to search": "bound",
                        "button names": {
                            "add button 1": "Bounded",
                            "add button 2": "Permafrost",
                            "add button 3": "Lost Soul",
                            "add button 4": "Lucky Potion",
                        },
                        "amounts to add": {"add button 2": 3, "add button 4": 100},
                        "crafting slots": 4,
                    },
                    "heavenly": {
                        "name to search": "heavenly",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Celestial",
                            "add button 3": "Exotic",
                            "add button 4": "Powered",
                            "add button 5": "Quartz",
                        },
                        "amounts to add": {"add button 1": 250, "add button 2": 2},
                        "crafting slots": 5,
                    },
                    "zeus": {
                        "name to search": "zeus",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Speed Potion",
                            "add button 3": "Zeus",
                            "add button 4": "Stormal",
                            "add button 5": "Wind",
                        },
                        "amounts to add": {"add button 1": 25, "add button 2": 25},
                        "crafting slots": 5,
                    },
                    "poseidon": {
                        "name to search": "poseidon",
                        "button names": {
                            "add button 1": "Speed Potion",
                            "add button 2": "Poseidon",
                            "add button 3": "Nautilus",
                            "add button 4": "Aquatic",
                        },
                        "amounts to add": {"add button 1": 50},
                        "crafting slots": 4,
                    },
                    "hades": {
                        "name to search": "hades",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Hades",
                            "add button 3": "Diaboli",
                            "add button 4": "Bleeding"
                        },
                        "amounts to add": {"add button 1": 50},
                        "crafting slots": 4,
                    },
                    "warp": {
                        "name to search": "warp",
                        "button names": {
                            "add button 1": "<PLACEHOLDER NAME>",  # PLACEHOLDER: replace
                            "add button 2": "<PLACEHOLDER NAME>",  # PLACEHOLDER: replace
                            "add button 3": "<PLACEHOLDER NAME>",  # PLACEHOLDER: replace
                            "add button 4": "<PLACEHOLDER NAME>",  # PLACEHOLDER: replace
                            "add button 5": "<PLACEHOLDER NAME>",  # PLACEHOLDER: replace
                            "add button 6": "<PLACEHOLDER NAME>"  # PLACEHOLDER: replace
                        },
                        "amounts to add": {

                        },
                        "crafting slots": 6,
                    },
                }
                }

    def create_new_preset(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Create New Preset")
        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("Set Preset Name:"))

        name_edit = QLineEdit()
        name_edit.setStyleSheet("color: cyan; background: #111;")
        layout.addWidget(name_edit)

        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.StandardButton.Ok)
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        if dlg.exec() != QDialog.DialogCode.Accepted:
            self.preset_selector.setCurrentText(config.get("current_preset", ""))
            return

        preset_name = name_edit.text().strip()
        if not preset_name or preset_name == None or "":
            QMessageBox.warning(self, "Invalid Name", "Preset name cannot be empty.")
            self.preset_selector.setCurrentText(config.get("current_preset", ""))
            return
        if preset_name in config["item presets"].keys():
            QMessageBox.warning(self, "Name Exists", "A preset with that name already exists.")
            self.preset_selector.setCurrentText(config.get("current_preset", ""))
            return

        source_key = config.get("current_preset")
        if source_key not in config.get("item presets", {}):
            presets = list(config.get("item presets", {}).keys())
            source_key = presets[0] if presets else None

        new_preset_value = deepcopy(config["item presets"][source_key]) if source_key else {}
        config.setdefault("item presets", {})[preset_name] = new_preset_value
        self.switch_preset(preset_name)

    def switch_preset(self, preset_name):
        if config.get("current_preset") == preset_name:
            return
        config["current_preset"] = preset_name
        self.current_preset = preset_name
        self.nice_config_save()
        self.preset_selector.blockSignals(True)
        self.preset_selector.clear()
        self.preset_selector.addItems(list(config.get("item presets", {}).keys()) + ["Create New Preset"])
        self.preset_selector.setCurrentText(preset_name)
        self.preset_selector.blockSignals(False)

        self.rebuild_potions_ui()

    def rebuild_potions_ui(self):
        while self.presets_tab_content_layout.count():
            old_preset = self.presets_tab_content_layout.takeAt(0)
            if old_preset is None:
                break
            preset_widget = old_preset.widget()
            if preset_widget is not None:
                preset_widget.deleteLater()
        self.build_potions_ui()

    def build_potions_ui(self):
        def checkbox_into_toggler(checkbox: QCheckBox):
            checkbox.setStyleSheet("""
                QCheckBox { color: cyan; font-size: 16px; spacing: 8px; }
                QCheckBox::indicator { width: 44px; height: 22px; border-radius: 11px; }
                QCheckBox::indicator:unchecked { background-color: #222; border: 1px solid cyan; }
                QCheckBox::indicator:checked { background-color: #0aa; border: 1px solid cyan; }
            """)

        def on_potion_toggle_changed(checked: bool):
            sender = self.sender()
            if sender is None:
                return
            potion = sender.property("potion")
            config_key = sender.property("config_key")
            config["item presets"][self.current_preset][potion][config_key] = bool(checked)
            self.nice_config_save()

        def on_potion_list_toggle_changed(checked: bool):
            sender = self.sender()
            if sender is None:
                return
            potion = sender.property("potion")
            list_key = sender.property("list_key")
            btn = sender.property("btn")

            items = config["item presets"][self.current_preset][potion][list_key]

            if checked:
                if btn not in items:
                    items.append(btn)
            else:
                if btn in items:
                    items.remove(btn)

            def button_order_key(name: str):
                last = name.rsplit(" ", 1)[-1]
                return (int(last), name)
            
            items.sort(key=button_order_key)
            self.nice_config_save()

        def on_potion_collapse_clicked():
            sender = self.sender()
            if sender is None or not isinstance(sender, QPushButton):
                return
            potion = sender.property("potion")
            body = sender.property("body")
            instant = sender.property("instant")
            cb_enabled = sender.property("cb enabled")
            potion_config = config["item presets"][self.current_preset][potion]

            if not cb_enabled.isChecked():
                return

            potion_config["collapsed"] = not potion_config["collapsed"]
            collapsed = potion_config["collapsed"]
            body.setVisible(not collapsed)
            instant.setVisible(not collapsed)
            sender.setText("▶" if collapsed else "▼")

            self.nice_config_save()
            self.presets_tab_content.adjustSize()

        def on_enabled_ui_changed(checked: bool):
            sender = self.sender()
            if sender is None or not isinstance(sender, QCheckBox):
                return
            potion = sender.property("potion")
            body = sender.property("body")
            instant = sender.property("instant")
            collapse_button = sender.property("collapse button")
            potion_config = config["item presets"][self.current_preset][potion]

            collapsed = potion_config["collapsed"]
            body.setVisible(checked and not collapsed)
            instant.setVisible(checked and not collapsed)
            collapse_button.setEnabled(checked)
            collapse_button.setText("▼" if checked and not collapsed else "▶")
            self.nice_config_save()
            self.presets_tab_content.adjustSize()

        for potion in data["item data"].keys():
            # Data References
            potion_config = config["item presets"][self.current_preset][potion]
            potion_data = data["item data"][potion]
            # Potion Section
            potion_section = QWidget()
            QVLayout = QVBoxLayout(potion_section)
            QVLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            potion_section.setStyleSheet("QWidget { background: #0b0b0b; border: 1px solid #033; border-radius: 8px; }")
            # Header
            potion_header = QWidget()
            potion_header.setStyleSheet("QWidget { background: #111; border: 0px; }")
            QHLayout = QHBoxLayout(potion_header)
            QHLayout.setContentsMargins(0, 0, 0, 0)
            title = QLabel(potion.capitalize())
            title.setStyleSheet("color: cyan; font-size: 24px;")
            # Instant Craft Checkbox
            instant_craft_checkbox = QCheckBox("Instant Craft")
            instant_craft_checkbox.setChecked(bool(potion_config["instant craft"]))
            checkbox_into_toggler(instant_craft_checkbox)
            instant_craft_checkbox.setProperty("potion", potion)
            instant_craft_checkbox.setProperty("config_key", "instant craft")
            instant_craft_checkbox.toggled.connect(on_potion_toggle_changed)
            # Enabled Checkbox
            enabled_checkbox = QCheckBox("Enabled")
            enabled_checkbox.setChecked(bool(potion_config["enabled"]))
            checkbox_into_toggler(enabled_checkbox)
            enabled_checkbox.setProperty("potion", potion)
            enabled_checkbox.setProperty("config_key", "enabled")
            enabled_checkbox.toggled.connect(on_potion_toggle_changed)
            # Collapse Button
            collapse_button = QPushButton("▶" if potion_config["collapsed"] else "▼")
            collapse_button.setFixedWidth(45)
            collapse_button.setStyleSheet("color: cyan; background: #111; border: 1px solid cyan; font-size: 22px;")
            # Header Layout
            QHLayout.addWidget(title)
            QHLayout.addStretch()
            QHLayout.addWidget(instant_craft_checkbox)
            QHLayout.addWidget(enabled_checkbox)
            QHLayout.addWidget(collapse_button)
            QVLayout.addWidget(potion_header)
            # Body
            body = QWidget()
            body.setStyleSheet("QWidget { background: #0f0f0f; border: 0px; }")
            columns_QH_Layout = QHBoxLayout(body)
            columns_QH_Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            columns_QH_Layout.setContentsMargins(2, 2, 2, 2)
            columns_QH_Layout.setSpacing(10)
            # Buttons To Check Column (Left)
            left_column = QWidget()
            left_column_QV_Layout = QVBoxLayout(left_column)
            left_column_QV_Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            left_column_QV_Layout.setContentsMargins(0, 0, 0, 0)
            left_column_QV_Layout.setSpacing(4)
            left_title = QLabel("Buttons To Check")
            left_title.setStyleSheet("color: cyan; font-size: 20px;")
            left_column_QV_Layout.addWidget(left_title)
            # Additional Buttons To Click Column (Right)
            right_column = QWidget()
            right_column_QV_Layout = QVBoxLayout(right_column)
            right_column_QV_Layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            right_column_QV_Layout.setContentsMargins(0, 0, 0, 0)
            right_column_QV_Layout.setSpacing(4)
            right_title = QLabel("Additional Buttons To Click")
            right_title.setStyleSheet("color: cyan; font-size: 20px;")
            right_column_QV_Layout.addWidget(right_title)
    
            slots = int(potion_config["crafting slots"])
            for i in range(1, slots + 1):
                btn = f"add button {i}"
                label = potion_data["button names"][btn]
                # Fill Buttons To Check Column (Left)
                temp_checkbox1 = QCheckBox(label)
                temp_checkbox1.setStyleSheet("color: cyan; font-size: 14px;")
                temp_checkbox1.setChecked(btn in potion_config["buttons to check"])
                temp_checkbox1.setProperty("potion", potion)
                temp_checkbox1.setProperty("list_key", "buttons to check")
                temp_checkbox1.setProperty("btn", btn)
                temp_checkbox1.toggled.connect(on_potion_list_toggle_changed)
                left_column_QV_Layout.addWidget(temp_checkbox1)
                # Fill Additional Buttons To Click Column (Right)
                temp_checkbox2 = QCheckBox(label)
                temp_checkbox2.setStyleSheet("color: cyan; font-size: 14px;")
                temp_checkbox2.setChecked(btn in potion_config["additional buttons to click"])
                temp_checkbox2.setProperty("potion", potion)
                temp_checkbox2.setProperty("list_key", "additional buttons to click")
                temp_checkbox2.setProperty("btn", btn)
                temp_checkbox2.toggled.connect(on_potion_list_toggle_changed)
                right_column_QV_Layout.addWidget(temp_checkbox2)
            columns_QH_Layout.addWidget(left_column)
            columns_QH_Layout.addStretch(1)
            columns_QH_Layout.addWidget(right_column)
            QVLayout.addWidget(body)

            # Collapse wiring (hide/show only the selections body)
            collapsed = potion_config["collapsed"]
            body.setVisible(potion_config["enabled"] and not collapsed)
            instant_craft_checkbox.setVisible(potion_config["enabled"] and not collapsed)
            collapse_button.setProperty("potion", potion)
            collapse_button.setProperty("body", body)
            collapse_button.setProperty("instant", instant_craft_checkbox)
            collapse_button.setProperty("cb enabled", enabled_checkbox)
            collapse_button.clicked.connect(on_potion_collapse_clicked)

            collapse_button.setEnabled(potion_config["enabled"])
            collapse_button.setText("▼" if potion_config["enabled"] and not collapsed else "▶")

            enabled_checkbox.setProperty("body", body)
            enabled_checkbox.setProperty("instant", instant_craft_checkbox)
            enabled_checkbox.setProperty("collapse button", collapse_button)
            enabled_checkbox.toggled.connect(on_enabled_ui_changed)

            self.presets_tab_content_layout.addWidget(potion_section)

    def switch_calibration_mode(self):
        if self.calibration_mode == "auto":
            self.calibrations_stack.setCurrentIndex(1)
            self.calibration_mode_button.setText("Current Mode: Semi-Automatic Calibration")
            self.calibration_mode = "semi-auto"

        elif self.calibration_mode == "semi-auto":
            self.calibrations_stack.setCurrentIndex(2)
            self.calibration_mode_button.setText("Current Mode: Manual Calibration")
            self.calibration_mode = "manual"

        elif self.calibration_mode == "manual":
            self.calibrations_stack.setCurrentIndex(0)
            self.calibration_mode_button.setText("Current Mode: Automatic Calibration")
            self.calibration_mode = "auto"
        
    def hotkey_listener(self):
        def on_press(key):
            if key == keyboard.Key.f1:
                self.start_macro_signal.emit()
            elif key == keyboard.Key.f2:
                self.stop_macro_signal.emit()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()

    def setup_hotkeys(self):
        self.start_macro_signal.connect(self.start_macro)
        self.stop_macro_signal.connect(self.stop_macro)
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    def find_pixels_with_color(self, *targets, bbox=None):
        if bbox == None:
            img = ImageGrab.grab()
        else:
            img = ImageGrab.grab(*bbox)

        pixels = np.asarray(img, dtype=np.uint8)
        mask = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=bool)

        for target in targets:
            if isinstance(target, str):
                clean = target.strip()
                if clean.startswith("#"):
                    clean = clean[1:]
                value = int(clean, 16)
                r = (value >> 16) & 0xFF
                g = (value >> 8) & 0xFF
                b = value & 0xFF
            else:
                r, g, b = target

            mask |= ((pixels[:, :, 0] == r) & (pixels[:, :, 1] == g) & (pixels[:, :, 2] == b))

        match_count = int(mask.sum())
        return match_count

    def auto_find_image(self, template, save=False, multiple=False, bbox_required=False):
            add_start_index = None
            template_path = f"{local_appdata_directory}\\Lib\\Images\\{template}"
             
            def save_position(position_name, center, bbox):
                if not save:
                    return
                if QMessageBox.information(self, "Template Found", "Would you like to save the found coordinates", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
                    return
                if bbox != None:
                    config["positions"][position_name] = {"bbox": bbox, "center": center}
                    self.nice_config_save()
                else:
                    config["positions"][position_name] = center
                    self.nice_config_save()

            def rescale_template(template):
                base_scale = data["img scales"][template]["scale"]   
                base_resolution =data["img scales"][template]["resolution"]

                user32 = ctypes.windll.user32
                gdi32 = ctypes.windll.gdi32
                hdc = user32.GetDC(0)
                scale_dpi = gdi32.GetDeviceCaps(hdc, 88)  # Returns 96, 120, 144, etc.
                user32.ReleaseDC(0, hdc)
                px_width, px_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
                current_scale = scale_dpi / 96.0
                scale_ratio = current_scale / base_scale
                res_ratio_x = px_width / base_resolution[0]
                res_ratio_y = px_height / base_resolution[1]
                total_scale_x = scale_ratio * res_ratio_x
                total_scale_y = scale_ratio * res_ratio_y
                self.log(f"Total Scale X: {total_scale_x}, Total Scale Y: {total_scale_y}")
                self.log(f"Screen Resolution: {px_width}x{px_height}, DPI Scale: {current_scale*100:.2f}%")
                self.log(f"Base Scale: {base_scale}, Base Resolution: {base_resolution}")
                self.log(f"Scale Ratio: {scale_ratio}, Resolution Ratio X: {res_ratio_x}, Resolution Ratio Y: {res_ratio_y}")

                template_img = Image.open(template_path)
                template_scaled = template_img.resize((int(template_img.width * total_scale_x), int(template_img.height * total_scale_y)), Image.Resampling.LANCZOS)
                template_scaled.show()
                return template_scaled
                    
            def find_template():
                count = 0
                screen = ImageGrab.grab()
                single_match_screen = screen.copy()
                all_matches_screen = screen.copy()
                bbox, center = None, None
            
                try:
                    if not multiple:
                        match = pyautogui.locateOnScreen(template_scaled, confidence=.70)
                        if match:
                            bbox = (int(match.left), int(match.top), int(match.left + match.width), int(match.top + match.height))
                            center = (int(match.left + match.width // 2), int(match.top + match.height // 2))
                            self.log(f"  bbox : {bbox}, center: {center}")
                            ImageDraw.Draw(all_matches_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                            all_matches_screen.show()
                            save_position(data["img scales"][template]["position name"], center, bbox if bbox_required else None)
                        else:
                            self.log(f"No match found for template: {template_path}")

                    elif multiple:
                        self.log("Searching for multiple matches...")
                        matches = list(pyautogui.locateAllOnScreen(template_scaled, confidence=.85))
                        sorted_matches = sorted(matches, key=lambda box: (box.top))

                        def multi_image_template_find(match):
                            nonlocal single_match_screen, bbox, center
                            bbox = (int(match.left), int(match.top), int(match.left + match.width), int(match.top + match.height))
                            center = (int(match.left + match.width // 2), int(match.top + match.height // 2))
                            self.log(f"  bbox : {bbox}, center: {center}")
                            single_match_screen = screen.copy()
                            ImageDraw.Draw(all_matches_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                            ImageDraw.Draw(single_match_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                            
                        if add_start_index == None:
                            for count, match in enumerate(sorted_matches):
                                self.log("1st to 3rd button logic")
                                self.log(count)
                                multi_image_template_find(match)
                                single_match_screen.show()
                                save_position(data["img scales"][template]["position name"][count], center, bbox if bbox_required else None)
                                
                        elif add_start_index != None:
                            for count, match in enumerate(sorted_matches, start=add_start_index[0]):
                                self.log("4th button and up logic")
                                self.log(count)
                                multi_image_template_find(match)
                                if count in add_start_index[1]:
                                    single_match_screen.show()
                                    save_position(data["img scales"][template]["position name"][count], center, bbox if bbox_required else None)
                        
                except (pyscreeze_ImageNotFoundException, pyautogui.ImageNotFoundException):
                    self.log(f"No matches found for template: {template_path}")
                    screen.show()

                except Exception as e:
                    self.log(f"Error finding matches: {e}")
                    screen.show()
                count = 0

            if template == "add button.png":
                what_add_buttons = QMessageBox(self)
                what_add_buttons.setWindowTitle("Add Button Selector")
                what_add_buttons.setText("Are the add button(s) 1–3 or 4?")
                btn_1_3 = what_add_buttons.addButton("1–3", QMessageBox.ButtonRole.AcceptRole)
                btn_4  = what_add_buttons.addButton("4",   QMessageBox.ButtonRole.AcceptRole)
                what_add_buttons.exec()

                if what_add_buttons.clickedButton() == btn_4:
                    add_start_index = 1, (3,)
                else :
                    add_start_index = None

            elif template == "amount box.png":
                what_amount_boxes = QMessageBox(self)
                what_amount_boxes.setWindowTitle("Amount Box Selector")
                what_amount_boxes.setText("Are the amount box(es) 1–3 or 4?")
                btn_1_3 = what_amount_boxes.addButton("1–3", QMessageBox.ButtonRole.AcceptRole)
                btn_4  = what_amount_boxes.addButton("4",   QMessageBox.ButtonRole.AcceptRole)
                what_amount_boxes.exec()

                if what_amount_boxes.clickedButton() == btn_4:
                    add_start_index = 1, (3,)
                else:
                    add_start_index = None

            template_scaled = rescale_template(template)
            find_template()

    def start_macro(self):
        if self.worker is not None and self.worker.is_alive():
            return
        self.mini_status_widget.show()
        self.update_status("Running")
        self.run_event.set()
        self.worker = threading.Thread(target=self._macro_worker, daemon=True)
        self.worker.start()

    def stop_macro(self):
        self.run_event.clear()

    def _macro_worker(self):
        while self.run_event.is_set():
            self.main_macro_loop()
            if not self.run_event.wait(0.1):
                self.update_status("Stopped")
                self.mini_status_widget.hide()

    def log(self, *args):
        self.update_status(" ".join(str(a) for a in args))

    def update_status(self, status_text):
        print("Status:", status_text)
        self.status_label.setText(f"Status: {status_text}")
        if self.mini_status_label != None:
            self.mini_status_label.setText(status_text)
            self.mini_status_label.adjustSize()
            self.mini_status_widget.adjustSize()

    def move_and_click(self, position, click=True):
        try:
            if click:
                mkey.left_click_xy_natural(*position)
            elif not click:
                mkey.move_to_natural(*position)
        except Exception:
            if click:
                mkey.left_click_xy(*position)
            elif not click:
                mkey.move_to(*position)

    def main_macro_loop(self, slowdown=0.01):
        def add_to_button(button_to_add_to):
            time.sleep(slowdown)
            if int(button_to_add_to[-1]) < 4:
                self.move_and_click(config[f"amount box {int(button_to_add_to[-1])}"], False)
                self.log("Moved to", "amount box", button_to_add_to[-1])
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                mkey.left_click()
                self.log("Amount box clicked to focus")
                time.sleep(slowdown)
                if button_to_add_to in data["item data"][item]["amounts to add"]:
                    keyboard.Controller().type(data["item data"][item]["amounts to add"][button_to_add_to])
                    self.log(f"Typed amount: {data['item data'][item]['amounts to add'][button_to_add_to]}")
                else:
                    keyboard.Controller().type("1")
                    self.log("Typed amount: 1")
                time.sleep(slowdown)
                self.move_and_click(config["positions"][button_to_add_to]["center"])
                self.log(f"{button_to_add_to} clicked")
            elif int(button_to_add_to[-1]) >= 4:
                self.move_and_click(config["positions"]["amount box 4"], False)
                self.log("Moved to amount box ((4)) center")
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                pyautogui.scroll(-18)
                self.log("Scrolled down to slot 4")
                time.sleep(slowdown)
                for x in range(4, int(button_to_add_to[-1])):
                    pyautogui.scroll(-40)
                    time.sleep(slowdown)
                    self.log("Scrolled down to slot", x + 1)
                time.sleep(slowdown)
                mkey.left_click()
                self.log("Amount box clicked to focus")
                time.sleep(slowdown)
                if button_to_add_to in data["item data"][item]["amounts to add"]:
                    keyboard.Controller().type(data["item data"][item]["amounts to add"][button_to_add_to])
                    self.log(f"Typed amount: {data['item data'][item]['amounts to add'][button_to_add_to]}")
                else:
                    keyboard.Controller().type("1")
                    self.log("Typed amount: 1")
                time.sleep(slowdown)

        def check_button(button_to_check):
            img = None
            time.sleep(slowdown)
            if int(button_to_check[-1]) < 4:
                self.move_and_click(config["positions"][f"amount box {int(button_to_check[-1])}"], False)
                self.log(f"Moved to amount box {int(button_to_check[-1])}")
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                img = ImageGrab.grab(config["positions"][button_to_check]["bbox"])
                self.log(button_to_check, "image captured")
                time.sleep(slowdown)
            elif int(button_to_check[-1]) >= 4:
                self.move_and_click(config["positions"]["amount box 4"], False)
                self.log("Moved to amount box ((4))")
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                pyautogui.scroll(-18)
                self.log("Scrolled down to slot 4")
                time.sleep(slowdown)
                for x in range(4, int(button_to_check[-1])):
                    time.sleep(slowdown)
                    pyautogui.scroll(-40)
                    self.log("Scrolled down to slot", x + 1)
                time.sleep(slowdown)
                img = ImageGrab.grab(config["positions"]["add button 4"]["bbox"])
                self.log(button_to_check, "image captured")
                time.sleep(slowdown)
            if img is None:
                raise Exception("Image capture failed in check_button")
            for t in reader.readtext(np.array(img), detail=0):
                self.log(f"Detected text for {button_to_check}:", t)
                if not t == "":
                    self.log("Item not ready, 'Add' detected.")
                    return False
            self.log("No 'Add' detected. for", button_to_check)
            time.sleep(slowdown)
            return True
            
        def search_for_potion(potion):
                self.move_and_click(config["positions"]["search bar"])
                self.log("Search bar clicked")
                time.sleep(slowdown)
                keyboard.Controller().type(data["item data"][potion]["name to search"])
                self.log("Item searched:", data["item data"][potion]["name to search"].capitalize())
                time.sleep(slowdown)
                self.move_and_click(config["positions"]["potion selection button"], False)
                self.log("Moved to potion selection button")
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                mkey.left_click()
                self.log("Selection button clicked")
                time.sleep(slowdown)

        def macro_loop_iteration(item):
            if item not in self.auto_add_waitlist and self.current_auto_add_potion != item:
                search_for_potion(item)

                for button_to_add_to in config["item presets"][self.current_preset][item]["buttons to check"]:
                    add_to_button(button_to_add_to)
                    time.sleep(slowdown)

                item_ready = True
                self.log(f"{item} set to ready")
                time.sleep(slowdown)
                
                for button_to_check in config["item presets"][self.current_preset][item]["buttons to check"]:
                    item_ready = check_button(button_to_check)
                    time.sleep(slowdown)
                    if not item_ready:
                        break

                time.sleep(slowdown)
                if item_ready:
                    self.log(f"Clicking additional buttons for {item}")
                    time.sleep(slowdown)
                    for button_to_click in config["item presets"][self.current_preset][item]["additional buttons to click"]:
                        add_to_button(button_to_click)
                        time.sleep(slowdown)

                    if not config["item presets"][self.current_preset][item]["instant craft"]:
                        if self.current_auto_add_potion == None:
                            if self.find_pixels_with_color("#C2FFA6", "#C1FEA5" ,bbox=config["positions"]["auto add button"]["bbox"]) == 0:
                                self.move_and_click(config["positions"]["auto add button"]["center"])
                            self.current_auto_add_potion = item
                            self.log("Clicked auto add button")
                            time.sleep(slowdown)
                        elif not self.current_auto_add_potion == None and item not in self.auto_add_waitlist:
                            self.auto_add_waitlist.append(item)
                            self.log(f"{item.capitalize()} added to auto add waitlist")
                            time.sleep(slowdown)
                    else:
                        self.move_and_click(config["positions"]["craft button"])
                        self.log("Clicked craft button")
                        time.sleep(slowdown)

            elif item == self.current_auto_add_potion:
                search_for_potion(item)
                item_ready = True
                self.log(f"{item.capitalize()} set to ready")
                time.sleep(slowdown)
                self.log("Checking All Buttons")
                time.sleep(slowdown)

                for slot in range(1, config["item presets"][self.current_preset][item]["crafting slots"] + 1):  # ignore manual click slots
                    if not check_button("add button " + str(slot)):
                        time.sleep(slowdown)
                        item_ready = False
                        break

                if item_ready:
                    self.move_and_click(config["positions"]["craft button"])
                    self.log("Clicked craft button")
                    time.sleep(slowdown)
                    if len(self.auto_add_waitlist) > 0:
                        search_for_potion(self.auto_add_waitlist[0])
                        if self.find_pixels_with_color("#C2FFA6", "#C1FEA5" ,bbox=config["positions"]["auto add button"]["bbox"]) == 0:
                            self.move_and_click(config["positions"]["auto add button"]["center"])
                            self.log("Clicked auto add button")
                        else:
                            self.log("Auto add button already active")
                        time.sleep(slowdown)
                        self.current_auto_add_potion = self.auto_add_waitlist.pop(0)
                           
        for item in data["item data"].keys():
                if config["item presets"][self.current_preset][item]["enabled"]:
                    macro_loop_iteration(item)
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = loading_screen()
    loader.show()
    sys.exit(app.exec())