# DPI Setup
import ctypes
ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
# Imports
import os, sys, threading, pyautogui, time, ctypes, pathlib, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QFormLayout, QMessageBox, QProgressBar, QStackedWidget
from pyscreeze import ImageNotFoundException as pyscreeze_ImageNotFoundException
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PIL import Image, ImageDraw, ImageGrab
from mousekey import MouseKey
from pynput import keyboard
import numpy as np

mkey = MouseKey()
mkey.enable_failsafekill('ctrl+e')
local_appdata_directory = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Dark Sol"
CONFIG_PATH = local_appdata_directory / "Dark Sol config.json"
os.makedirs(local_appdata_directory, exist_ok=True)

# Tasks (For Mr. Bored)
# 1. Add amount button logic
# 2. Add potion selection
# 3. Add item selection for each potion
# 4. Add additional buttons to click check to prevent softlock 
# 5. Make auto add checks ignore manual click slots (lucky potions)
# 6. Fix other widgets not closing properly

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
        self.setWindowTitle("Dark Sol")
        self.setGeometry(100, 100, 400, 100)
        # Create Tabs
        self.tabs_widget = QTabWidget()
        self.main_tab = QWidget()
        self.calibrations_tab = QWidget()
        self.theme_tab = QWidget()
        self.settings_tab = QWidget()
        # Create Main Tab Elements
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.status_label = QLabel("Status: Stopped")
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
        # Calibrations Page Setup
        self.calibrations_stack.addWidget(auto_calibration_page)       # index 0
        self.calibrations_stack.addWidget(semi_auto_calibration_page)  # index 1
        self.calibrations_stack.addWidget(manual_calibration_page)     # index 2
        self.calibrations_tab_main_vbox.addWidget(self.calibration_mode_button)
        self.calibrations_tab_main_vbox.addWidget(self.calibrations_stack)
        self.calibrations_stack.setCurrentIndex(0)
        self.calibrations_tab.setLayout(self.calibrations_tab_main_vbox)
        # Button Connectors
        self.calibration_mode_button.clicked.connect(lambda: self.switch_calibration_mode())
        self.set_add_button_coordinates.clicked.connect(lambda: self.show_add_button_coordinates_selector())
        self.set_amount_box_coordinates.clicked.connect(lambda: self.show_amount_box_coordinates_selector())
        self.find_add_button.clicked.connect(lambda: self.auto_find_image("add button.png", True, True, True))
        self.find_amount_box.clicked.connect(lambda: self.auto_find_image("amount box.png", True, True))
        self.find_auto_add_button.clicked.connect(lambda: self.auto_find_image("auto add button.png", True, False))
        self.find_craft_button.clicked.connect(lambda: self.auto_find_image("craft button.png", True, False))
        self.find_search_bar.clicked.connect(lambda: self.auto_find_image("cauldren search bar.png", True, False))
        self.find_potion_selection_button.clicked.connect(lambda: self.auto_find_image("heavenly potion potion selector button.png", True, False))
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
        # Initialize Config
        self.initalize_config()
        # Setup  Hotkeys
        self.start_button.clicked.connect(self.start_macro)
        self.stop_button.clicked.connect(self.stop_macro)
        self.setup_hotkeys()
        
    def initalize_config(self):
        global config

        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        else:
            config = {
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
                        "craft button": [573, 618]
                    },
                    "item_presets": {
                        "bound": {
                            "name to search": "bound",
                            "buttons to check": ["add button 1", "add button 2"],
                            "additional buttons to click": ["add button 4",],
                            "crafting slots": 4,
                            "instant craft": False
                        },
                        "heavenly": {
                            "name to search": "heavenly",
                            "buttons to check": ["add button 2", "add button 3"],
                            "additional buttons to click" : ["add button 1",],
                            "crafting slots": 5,
                            "instant craft": False
                        },
                        "zeus": {
                            "name to search": "zeus",
                            "buttons to check": ["add button 3",],
                            "additional buttons to click": ["add button 1", "add button 2"],
                            "crafting slots": 5,
                            "instant craft": False
                        },
                        "poseidon": {
                            "name to search": "poseidon",
                            "buttons to check": ["add button 2",],
                            "additional buttons to click": ["add button 1",],
                            "crafting slots": 4,
                            "instant craft": False
                        },
                        "hades": {
                            "name to search": "hades",
                            "buttons to check": ["add button 2",],
                            "additional buttons to click": ["add button 1",],
                            "crafting slots": 4,
                            "instant craft": False
                        },
                        "warp": {
                            "name to search": "warp",
                            "buttons to check": ["add button 4", "add button 5", "add button 6"],
                            "additional buttons to click": ["add button 1", "add button 2"],
                            "crafting slots": 6,
                            "instant craft": False
                        }
                    }
                }
            
    def save_config(self, config, ind=4):
        S = (str, int, float, bool, type(None))

        def d(o, l=0):
            p = " " * (ind * l)
            np = " " * (ind * (l + 1))
            if isinstance(o, dict):
                if not o:
                    return "{}"
                it = list(o.items())
                if len(it) <= 2 and all(isinstance(k, str) for k, _ in it) and all(
                    isinstance(v, S)
                    or (isinstance(v, (list, tuple)) and len(v) <= 6 and all(isinstance(x, S) for x in v))
                    for _, v in it
                ):
                    return "{" + ", ".join(
                        f"{json.dumps(k)}: {json.dumps(list(v) if isinstance(v, tuple) else v)}" for k, v in it
                    ) + "}"
                return "{\n" + "\n".join(
                    f"{np}{json.dumps(k)}: {d(v, l + 1)}{',' if i < len(it) - 1 else ''}" for i, (k, v) in enumerate(it)
                ) + f"\n{p}}}"
            if isinstance(o, (list, tuple)):
                a = list(o)
                if len(a) <= 6 and all(isinstance(x, S) for x in a):
                    return json.dumps(a)
                if not a:
                    return "[]"
                return "[\n" + "\n".join(
                    f"{np}{d(v, l + 1)}{',' if i < len(a) - 1 else ''}" for i, v in enumerate(a)
                ) + f"\n{p}]"
            return json.dumps(o)

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            f.write(d(config) + "\n")
    
    def update_config(self, key, new_value):
        config[key] = new_value
        self.save_config(config)

    def show_add_button_coordinates_selector(self, show=True):
        self.add_button_coordinates_selector.setVisible(show)
    
    def show_amount_box_coordinates_selector(self, show=True):
        self.amount_box_coordinates_selector.setVisible(show)

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
                self.move_and_click(config["positions"][button_to_add_to]["center"], False)
                self.log("Moved to", button_to_add_to, "center")
                time.sleep(slowdown)
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                mkey.left_click()
            elif int(button_to_add_to[-1]) >= 4:
                self.move_and_click(config["positions"]["add button 4"]["center"], False)
                self.log("Moved to add button ((4)) center")
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
                self.log(f"{button_to_add_to} clicked")

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
            
        def macro_loop_iteration(item):
            if item not in self.auto_add_waitlist and self.current_auto_add_potion != item:
                self.move_and_click(config["positions"]["search bar"])
                self.log("Search bar clicked")
                time.sleep(slowdown)
                keyboard.Controller().type(config["item_presets"][item]["name to search"])
                self.log("Item searched:", config["item_presets"][item]["name to search"].capitalize())
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

                for button_to_add_to in config["item_presets"][item]["buttons to check"]:
                    add_to_button(button_to_add_to)
                    time.sleep(slowdown)

                item_ready = True
                self.log(f"{item} set to ready")
                time.sleep(slowdown)
                
                for button_to_check in config["item_presets"][item]["buttons to check"]:
                    item_ready = check_button(button_to_check)
                    time.sleep(slowdown)
                    if not item_ready:
                        break

                time.sleep(slowdown)
                if item_ready:
                    self.log(f"Clicking additional buttons for {item}")
                    time.sleep(slowdown)
                    for button_to_click in config["item_presets"][item]["additional buttons to click"]:
                        add_to_button(button_to_click)
                        time.sleep(slowdown)

                    if not config["item_presets"][item]["instant craft"]:
                        if self.current_auto_add_potion == None:
                            self.move_and_click(config["positions"]["auto add button"])
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
                self.move_and_click(config["positions"]["search bar"])
                self.log("Search bar clicked")
                time.sleep(slowdown)
                keyboard.Controller().type(config["item_presets"][item]["name to search"])
                self.log("Item searched:", config["item_presets"][item]["name to search"].capitalize())
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

                item_ready = True
                self.log(f"{item.capitalize()} set to ready")
                time.sleep(slowdown)
                self.log("Checking All Buttons")
                time.sleep(slowdown)

                for slot in range(1, config["item_presets"][item]["crafting slots"] + 1):  # ignore manual click slots
                    if not check_button("add button " + str(slot)):
                        time.sleep(slowdown)
                        item_ready = False
                        break

                if item_ready:
                    self.move_and_click(config["positions"]["craft button"])
                    self.log("Clicked craft button")
                    time.sleep(slowdown)
                    if len(self.auto_add_waitlist) > 0:
                        self.move_and_click(config["positions"]["search bar"])
                        self.log("Search bar clicked")
                        time.sleep(slowdown)
                        keyboard.Controller().type(config["item_presets"][self.current_auto_add_potion]["name to search"])
                        self.log(f"Item searched: {self.current_auto_add_potion.capitalize()}")
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
                        self.move_and_click(config["positions"]["auto add button"])
                        self.log("Clicked auto add button")
                        time.sleep(slowdown)
                        self.current_auto_add_potion = self.auto_add_waitlist.pop(0)
                           
        for item in config["item_presets"].keys():
            if item != "warp":
                macro_loop_iteration(item)
        
    def auto_find_image(self, template, save=False, multiple=False, bbox_required=False):
        add_start_index = None
        template_path = f"{local_appdata_directory}\\Lib\\Images\\{template}"
        data = {"img_scales": {"add button.png": {"scale": 1.25, "resolution": (1920, 1080), "position_name": ["add button 1", "add button 2", "add button 3", "add button 4"]},
                               "amount box.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": ["amount box 1", "amount box 2", "amount box 3", "amount box 4"]},
                               "auto add button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": "auto add button"},
                               "craft button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": "craft button"},
                               "cauldren search bar.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": "search bar"},
                                "heavenly potion potion selector button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": "potion selection button"},
                                }} 

        def save_position(position_name, center, bbox):
            if not save:
                return
            if QMessageBox.information(self, "Template Found", "Would you like to save the found coordinates", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
                return
            if bbox != None:
                config["positions"][position_name] = {"bbox": bbox, "center": center}
                self.save_config(config)
            else:
                config["positions"][position_name] = center
                self.save_config(config)

        def rescale_template(template):
            base_scale = data["img_scales"][template]["scale"]   
            base_resolution = data["img_scales"][template]["resolution"]

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
                        save_position(data["img_scales"][template]["position_name"], center, bbox if bbox_required else None)
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
                            save_position(data["img_scales"][template]["position_name"][count], center, bbox if bbox_required else None)
                            
                    elif add_start_index != None:
                        for count, match in enumerate(sorted_matches, start=add_start_index[0]):
                            self.log("4th button and up logic")
                            self.log(count)
                            multi_image_template_find(match)
                            if count in add_start_index[1]:
                                single_match_screen.show()
                                save_position(data["img_scales"][template]["position_name"][count], center, bbox if bbox_required else None)
                    
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
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = loading_screen()
    loader.show()
    sys.exit(app.exec())