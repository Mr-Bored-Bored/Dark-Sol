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
current_directory = pathlib.Path(__file__).resolve().parent
local_appdata_directory = pathlib.Path(os.environ["LOCALAPPDATA"])
os.makedirs(local_appdata_directory, exist_ok=True)

# Tasks 
# 1. Add amount button logic
# 2. Add potion selection
# 3. Add item selection for each potion
# 4. Add additional buttons to click check to prevent softlock 
# 5. Add auto add logic (
# 1. new auto add button checking logic
# 2. additional items to add check failure logic)
# 6. Make auto add checks ignore manual click slots (lucky potions)


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
        self.setWindowTitle("Loading Auto Crafter")
        self.setStyleSheet(""" QProgressBar {background-color: black; color: white; border-radius: 5px; border: 1px solid black; font-size: 20px; height: 40px;} QProgressBar::chunk {background-color: lime; }""")
        self.setGeometry(0, 0, 500, 100)
        self.loading_bar.setGeometry(0, 0, 500, 100)
        self.loading_bar.setRange(0, parts_to_load)
        self.loading_bar.setValue(0)
        self.loading_bar.setFormat("Loading Auto Crafter (You should not see this)")
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
        main_window = Auto_Crafter()
        main_window.show()

# Main Auto Crafter
class Auto_Crafter(QMainWindow):
    start_macro_signal = pyqtSignal()
    stop_macro_signal = pyqtSignal()

    def __init__(self):
        # Create main window
        super().__init__()
        self.setWindowTitle("Auto Crafter")
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
        self.find_add_button = QPushButton("Find Add Button")
        self.find_auto_add_button = QPushButton("Find Auto Add Button")
        self.find_craft_button = QPushButton("Find Craft Button")
        self.find_search_bar = QPushButton("Find Search Bar")
        self.find_potion_selection_button = QPushButton("Find Potion Selection Button")
        # Semi Auto Calibration mode
        self.set_add_button_template = QPushButton("Set Add Button Template")
        # Manual Calibration mode
        self.set_add_button_1_coordinates = QPushButton("Set Add Button 1 Coordinates")
        self.set_add_button_2_coordinates = QPushButton("Set Add Button 2 Coordinates")
        self.set_add_button_3_coordinates = QPushButton("Set Add Button 3 Coordinates")
        self.set_add_button_4_coordinates = QPushButton("Set Add Button 4 Coordinates")
        self.set_auto_add_button_coordinates = QPushButton("Set Auto Add Button Coordinates")
        self.set_craft_button_coordinates = QPushButton("Set Craft Button Coordinates")
        self.set_search_bar_coordinates = QPushButton("Set Search Bar Coordinates")
        self.set_potion_selection_button_coordinates = QPushButton("Set Potion Selection Button Coordinates")
        # Create Running Variables
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
        # Auto Calibration Page
        auto_calibration_page = QWidget()
        auto_layout = QVBoxLayout(auto_calibration_page)
        auto_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        auto_layout.addWidget(self.find_add_button)
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
        manual_layout.addWidget(self.set_add_button_1_coordinates)
        manual_layout.addWidget(self.set_add_button_2_coordinates)
        manual_layout.addWidget(self.set_add_button_3_coordinates)
        manual_layout.addWidget(self.set_add_button_4_coordinates)
        manual_layout.addWidget(self.set_auto_add_button_coordinates)
        manual_layout.addWidget(self.set_craft_button_coordinates)
        manual_layout.addWidget(self.set_search_bar_coordinates)
        manual_layout.addWidget(self.set_potion_selection_button_coordinates)
        # Add comments
        self.calibrations_stack.addWidget(auto_calibration_page)       # index 0
        self.calibrations_stack.addWidget(semi_auto_calibration_page)  # index 1
        self.calibrations_stack.addWidget(manual_calibration_page)     # index 2

        self.calibrations_tab_main_vbox.addWidget(self.calibration_mode_button)
        self.calibrations_tab_main_vbox.addWidget(self.calibrations_stack)
        self.calibrations_stack.setCurrentIndex(0)
        self.calibrations_tab.setLayout(self.calibrations_tab_main_vbox)

        # Calibrations Tab Setup
        self.calibration_mode_button.setToolTip("Switch between automatic and manual calibration mode.")
        
        # Button Connectors
        self.calibration_mode_button.clicked.connect(lambda: self.switch_calibaration_mode())
        self.find_add_button.clicked.connect(lambda: self.auto_find_image("add button.png", True, True))
        self.find_auto_add_button.clicked.connect(lambda: self.auto_find_image("auto add button.png", True, False))
        self.find_craft_button.clicked.connect(lambda: self.auto_find_image("craft button.png", True, False))
        self.find_search_bar.clicked.connect(lambda: self.auto_find_image("cauldren search bar.png", True, False))
        self.find_potion_selection_button.clicked.connect(lambda: self.auto_find_image("heavenly potion potion selector button.png", True, False))

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
        

    def switch_calibaration_mode(self):

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

    def setup_hotkeys(self):
        self.start_macro_signal.connect(self.start_macro)
        self.stop_macro_signal.connect(self.stop_macro)
        threading.Thread(target=self.hotkey_listener, daemon=True).start()

    def hotkey_listener(self):
        def on_press(key):
            if key == keyboard.Key.f1:
                self.start_macro_signal.emit()
            elif key == keyboard.Key.f2:
                self.stop_macro_signal.emit()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        listener.join()

    def start_macro(self):
        if self.worker is not None and self.worker.is_alive():
            return
        self.status_label.setText("Status: Running")
        self.run_event.set()
        self.worker = threading.Thread(target=self._macro_worker, daemon=True)
        self.worker.start()

    def stop_macro(self):
        self.status_label.setText("Status: Stopped")
        self.run_event.clear()

    def _macro_worker(self):
        while self.run_event.is_set():
            self.main_macro_loop()
            if not self.run_event.wait(0.1):
                break

    def initalize_config(self):
        global config

        if os.path.exists(f"{current_directory}\\Dark Sol config.json"):
            with open(f"{current_directory}\\Dark Sol config.json", "r") as f:
                config = json.load(f)
        else:
            config = {"positions": {
                                "add button 1": {"bbox": (757, 602, 837, 631), "center": (797, 616)},
                                "add button 2": {"bbox": (757, 656, 837, 685), "center": (797, 670)}, 
                                "add button 3": {"bbox": (757, 710, 837, 739), "center": (797, 724)}, 
                                "add button 4": {"bbox": (757, 739, 837, 768), "center": (797, 753)},
                                "amount box 1": (717, 616),
                                "amount box 2": (717, 670),
                                "amount box 3": (717, 724),
                                "amount box 4": (717, 753),
                                "potion selection button": (1140, 400),
                                "search bar": (909, 322),
                                "auto add button": (713, 560),
                                "craft button": (580, 560),
                                },
                    "item_presets": {
                                "bound": {
                                        "name to search": "bound",
                                        "buttons to check": ["add button 1", "add button 2"],
                                        "additional buttons to click": ["add button 4"],
                                        "crafting slots": 4,
                                        "instant craft": False
                                            },
                                "zeus godly": {
                                        "name to search": "zeus",
                                        "buttons to check": ["add button 3", "add button 4"],
                                        "additional buttons to click": ["add button 1", "add button 2"],
                                        "crafting slots": 5,
                                        "instant craft": False
                                            },
                                "warp": {
                                        "name to search": "warp",
                                        "buttons to check": ["add button 4", "add button 5", "add button 6"],
                                        "additional buttons to click": ["add button 1", "add button 2"],
                                        "crafting slots": 6,
                                        "instant craft": False      
                                            },
                                        }}
        
        json.dump(config, open(f"{current_directory}\\auto_crafter_config.json", "w"), indent=4)

    def update_config(self, key, new_value):
        config[key] = new_value
        json.dump(config, open(f"{current_directory}\\auto_crafter_config.json", "w"), indent=4)

    def main_macro_loop(self, slowdown=0.1):
        global auto_add_waitlist
        auto_add_waitlist = []
        global current_auto_add_potion
        current_auto_add_potion = None

        def add_to_button(button_to_add_to):
                    print("Adding to:", button_to_add_to)
                    if int(button_to_add_to[-1]) < 4:
                        print("Button is less than 4:")
                        mkey.move_to_natural(*config["positions"][button_to_add_to]["center"])
                        print("Moved to button center:")
                        pyautogui.scroll(2000)
                        print("Scrolled up:")
                        time.sleep(slowdown)
                        mkey.left_click()
                        print("Add button clicked")
                    elif int(button_to_add_to[-1]) >= 4:
                        print("Button is 4 or greater:")
                        mkey.move_to_natural(*config["positions"]["add button 4"]["center"])
                        print("Moved to add button 4 center:")
                        pyautogui.scroll(2000)
                        print("Scrolled up:")
                        time.sleep(slowdown)
                        pyautogui.scroll(-22)
                        print("Scrolled down to button 4")
                        for x in range(4, int(button_to_add_to[-1])):
                            pyautogui.scroll(-46)
                            time.sleep(slowdown)
                            print("Scrolled down to button:", x+1)
                        time.sleep(slowdown)
                        mkey.left_click()
                        print("Add button clicked")

        def check_button(button_to_check):
            print("Checking:", button_to_check)
            if int(button_to_check[-1]) < 4:
                print("Button is less than 4:")
                mkey.move_to_natural(*config["positions"][button_to_check]["amount box"])
                pyautogui.scroll(2000)
                print("Scrolled up:")
                time.sleep(0.01)
                img = ImageGrab.grab(config["positions"][button_to_check]["bbox"])
                print("Button image captured")
            elif int(button_to_check[-1]) >= 4:
                print("Button is 4 or greater:")
                mkey.move_to_natural(*config["positions"]["add button 4"]["amount box"])
                pyautogui.scroll(2000)
                print("Scrolled up:")
                time.sleep(0.01)
                pyautogui.scroll(-22)
                print("Scrolled down to button 4:")
                for x in range(4, int(button_to_check[-1])):
                    time.sleep(0.01)
                    pyautogui.scroll(-46)
                    print("Scrolled down to button: ", x + 1)
                time.sleep(0.01)
                img = ImageGrab.grab(config["positions"]["add button 4"]["bbox"])
                print(button_to_check, "image captured")
            for t in reader.readtext(np.array(img), detail=0):
                print(f"Detected text for {button_to_check}:", t)
                if not t == "":
                    print("Item not ready, 'Add' detected.")
                    return False
            return True
        
        def macro_loop_iteration(item):
            global current_auto_add_potion
            global auto_add_waitlist

            if item not in auto_add_waitlist and current_auto_add_potion != item:
                mkey.left_click_xy_natural(*config["positions"]["search bar"])
                print("Search bar clicked")
                keyboard.Controller().type(config["item_presets"][item]["name to search"])
                print("Item searched:", config["item_presets"][item]["name to search"])
                mkey.move_to_natural(*config["positions"]["potion selection button"])
                pyautogui.scroll(2000)
                time.sleep(slowdown)
                mkey.left_click()
                print("Selection button clicked")
                for button_to_add_to in config["item_presets"][item]["buttons to check"]:
                    add_to_button(button_to_add_to)
                item_ready = True
                print("Item set to ready")
                for button_to_check in config["item_presets"][item]["buttons to check"]:
                    item_ready = check_button(button_to_check)
                    if not item_ready:
                        break
                    print("Item is ready, proceeding to craft.")
                    for button_to_click in config["item_presets"][item]["additional buttons to click"]:
                        mkey.move_to_natural(*config["positions"][button_to_click]["center"])
                        pyautogui.scroll(2000)
                        time.sleep(slowdown)
                        mkey.left_click()
                        print("Clicked additional button:", button_to_click)
                    if not config["item_presets"][item]["instant craft"]:
                        if current_auto_add_potion == None and item not in auto_add_waitlist:
                            mkey.left_click_xy_natural(*config["positions"]["auto add button"])
                            print("Clicked auto add button")
                        elif not current_auto_add_potion == None and item not in auto_add_waitlist:
                            auto_add_waitlist.append(item)
                            print(f"{item} added to auto add waitlist")
                    elif config["item_presets"][item]["instant craft"]:
                        mkey.left_click_xy_natural(*config["positions"]["craft button"])
                        print("Clicked craft button")
            elif item == current_auto_add_potion:
                item_ready = True
                for slot in range(1, config["item_presets"][item]["crafting slots"] + 1): # Make it ignore manual click slots aka lucky potions 
                    if not check_button("add button " + str(slot)):
                        item_ready = False
                        break
                if item_ready:
                    mkey.left_click_xy_natural(*config["positions"]["craft button"])
                    if len(auto_add_waitlist) > 0:
                        item = auto_add_waitlist[0]
                        mkey.left_click_xy_natural(*config["positions"][config["item_presets"][item]["name to search"]])
                        mkey.move_to_natural(*config["positions"]["potion selection button"])
                        pyautogui.scroll(2000)
                        time.sleep(slowdown)
                        mkey.left_click()
                        mkey.left_click_xy_natural(*config["positions"]["auto add button"])
                        print("Clicked auto add button for next potion")
                        current_auto_add_potion = auto_add_waitlist.pop(0)
                        print("Next potion from waitlist:", current_auto_add_potion)

        macro_loop_iteration("bound")
        macro_loop_iteration("zeus godly")
        macro_loop_iteration("warp")
        
    def auto_find_image(self, template, save=False, multiple=False):
        template_path = f"{current_directory}\\{template}"
        data = {"img_scales": {"add button.png": {"scale": 1.25, "resolution": (1920, 1080), "position_name": ["add button 1", "add button 2", "add button 3", "add button 4"]},
                               "auto add button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": ["auto add button"]},
                               "craft button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": ["craft button"]},
                               "cauldren search bar.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": ["search bar"]},
                                "heavenly potion potion selector button.png": {"scale": 1.25, "resolution": (1920, 1200), "position_name": ["potion selection button"]},
                                }} 
        
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
            print(f"Total Scale X: {total_scale_x}, Total Scale Y: {total_scale_y}")
            print(f"Screen Resolution: {px_width}x{px_height}, DPI Scale: {current_scale*100:.2f}%")
            print(f"Base Scale: {base_scale}, Base Resolution: {base_resolution}")
            print(f"Scale Ratio: {scale_ratio}, Resolution Ratio X: {res_ratio_x}, Resolution Ratio Y: {res_ratio_y}")

            template_img = Image.open(template_path)
            template_scaled = template_img.resize((int(template_img.width * total_scale_x), int(template_img.height * total_scale_y)), Image.Resampling.LANCZOS)
            template_scaled.show()
            return template_scaled

        def save_position(position_name, bbox, center):
            if not save:
                return
            if QMessageBox.information(self, "Template Found", "Would you like to save the found coordinates", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
                return
            print(position_name)
            config["positions"][position_name] = {"bbox": bbox, "center": center}
            json.dump(config, open(f"{current_directory}\\auto_crafter_config.json", "w"), indent=4)

        def find_template():
            nonlocal add_start_index
            count = 0
            screen = ImageGrab.grab()
            single_match_screen = screen.copy()
            all_matches_screen = screen.copy()
            bbox, center = None, None

            print("Finding all matches of template...")
        
            try:
                if not multiple:
                    match = pyautogui.locateOnScreen(template_scaled, confidence=.70)
                    if match:
                        bbox = (int(match.left), int(match.top), int(match.left + match.width), int(match.top + match.height))
                        center = (int(match.left + match.width // 2), int(match.top + match.height // 2))
                        print(f"  bbox : {bbox}, center: {center}")
                        ImageDraw.Draw(all_matches_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                        all_matches_screen.show()
                        save_position(template, bbox, center)
                    else:
                        print(f"No match found for template: {template_path}")

                elif multiple:
                    print ("Searching for multiple matches...")
                    matches = list(pyautogui.locateAllOnScreen(template_scaled, confidence=.75))
                    sorted_matches = sorted(matches, key=lambda box: (box.top))

                    def multi_image_template_find(match):
                        nonlocal single_match_screen, bbox, center
                        bbox = (int(match.left), int(match.top), int(match.left + match.width), int(match.top + match.height))
                        center = (int(match.left + match.width // 2), int(match.top + match.height // 2))
                        print(f"  bbox : {bbox}, center: {center}")
                        single_match_screen = screen.copy()
                        ImageDraw.Draw(all_matches_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                        ImageDraw.Draw(single_match_screen).rectangle(((match.left, match.top), (match.left + match.width, match.top + match.height)), outline='lime')
                        
                    if add_start_index == None:
                        for count, match in enumerate(sorted_matches):
                            print("1st to 3rd button logic")
                            print(count)
                            multi_image_template_find(match)
                            single_match_screen.show()
                            save_position(data["img_scales"][template]["position_name"][count], bbox, center)
                            
                    elif add_start_index != None:
                        for count, match in enumerate(sorted_matches, start=add_start_index[0]):
                            print("4th button and up logic")
                            print(count)
                            multi_image_template_find(match)
                            if count in add_start_index[1]:
                                single_match_screen.show()
                                save_position(data["img_scales"][template]["position_name"][count], bbox, center)
                    
            except (pyscreeze_ImageNotFoundException, pyautogui.ImageNotFoundException):
                print(f"No matches found for template: {template_path}")
                screen.show()

            except Exception as e:
                print(f"Error finding matches: {e}")
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
        template_scaled = rescale_template(template)
        find_template()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    loader = loading_screen()
    loader.show()
    sys.exit(app.exec())





