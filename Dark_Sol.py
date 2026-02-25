"""
# Tasks (For Mr. Bored)

# Necessary for First Release:
- Calibrations
1. Fix manual scroll calibration
2. Improve calibration gui / fix it to support new systems
3. Make it so that macro cant start until calibrations are complete
4. Make it so that you can close auto calibrate and then resume where you left off
5. Add verifications before runnning certain calibrations
6. Rename calibration buttons
7. Make manual calibration have a single position thing instead of a box for some calibrations
8. Make a list of features that show if the repo cannot be reached

- Logs
9. Add debug log file
10. Make config creation be added to log after it is created due to the fact config is made before log is created

- Random
11. Add auto updater
12. Make manual scroll calibration slightly automatic using pixel detection for new item detection (need to make position selection thing first)
13. Make it so that overlays can show individual pixels instead of an area
14. Add paths for auto rejoin (non vip and add settings to choose path) and auto calibrations
15. Check if roblox is open and if sols is open before starting macro and add a msg box if not also add settings for these
16. Add crafted potion detection / stats
17. Make ps join button check for valid ps link and save private server link button
18. Add collection buttons to calibrations (exit button may not be added)
19. Add play button to calibrations
20. Add logs where needed (idk check)
21. When macro starts check if roblox is open by checking for a window id if it is then check logs to see if the latest log is a join of "place 15532962292" or a disconnect of any kind also if at any point the log shows roblox was closed or the user was disconnected (kill the macro thread) and rejoin the private server if enabled and add to log
22. Add potion gui entered check
23. Add config corrupted check and fix config
25. Add complete macro exception handling with message box and logging
26. Add msgbox for when something is being downloaded from the repo
27. Make requirements file and check what its file type should be 
28. Improve logging by adding log type, log file, and better wrapping
29. Add current auto add potion enabled check (after pause / unpause)
30. Add stuff for potions that have only requires manual crafting
31. Make potion menu item button be clicked with search for potion function
32. Add macro pause and unpause auto add button check
33. Check roblox logs for disconnect if sols rng is detected to be open before looking for play button
34. Add manual checkmark calibration failsafe (if calibration was not done to not contine)
35. Make remove overlay possible for specific overlays instead of just all overlays
36. Standerized create_msg_box returns and make it skip the ok one unless a parameter is enabled
37. Add a function to do specific points instead of a entire area for a position also allow the user to choose which one they want to do
38. Make requirements downloader check lib folder in github instead of manual list of files and folders to check    

- Mini Status Label
39. Make Mini Status Label movable (when moving make it show largest size)
40. Make mini status label wrapable

- Final Checks
41. Remove excess delays / slowdowns (ensure reliability)
42. Check print statements and remove unnecessary ones
43. Verify macro can handle everything after entering potion craft gui

# Might be added for First Release:
1. Add multi template for single calibration
2. Advanced auto updater (with progress bar)
3. Add settings tab functionality
4. Add tooltips to all buttons (if necessary)
5. Add function to check multiple coordinates and seach each one below (mainly for godly's)
6. Ability to slow down macro if it is going too fast and missing things (mainly for lower end pcs)
7. Always on top setting
8. Make calibration checks not need manual scrolling to verify calibrations
9. Add the ability to reset templates to default by pulling from the repo
10. Add the ability to craft a specfic amount of potions and then stop crafting that potion and if all have been crafted then stop
11. Highest donatator list with messages

# Planned for the future:
1. Make dpi, resolution, scale and etc global
1. Make all hardcoded resolutions dynamic (aka figure out how scaling works)(just praying current code scales atp)
2. Add main and auto updater reinstall arguements
3. Fix multi monitor awareness
4. Fix other widgets not closing properly
6. Make plugins system
7. Add theme tab functionality (Requires style sheet overhaul and compression to allow for user friendly adjustments)
8. Able to handle corrupt config
9. Add config backups
10. Add importing / exporting presets
11. Add importing / exporting themes
12. Add ability to change hotkeys
14. Make it so that it can add in 1's instead of just the amount numbers
16. Add custom log messages (ability for certain logs to not show)
17. Add complete calibration (paths needed)
18. Add private server reconnects (paths needed)
19. Make macro full screen compatible (only needs template rescaling adjustment(i think))
21. Complete overhall and  usage of multi classes
21. Auto Quest Plugin (Depending on what cresqnt and noteab say)
22. Make auto rare biome popping plugin (Depending on what cresqnt and noteab say)
23. Make it so that you can adjust wait time after reset in settings
24. Make it so that rescaled templates are saved so the function doesnt have to be called every time
32. Add ability to craft Limbo potions (aka enter limbo for easier aura gathering)
- Mini Status Label
21. Make mini status label show auto add waitlist and add setting for it 

--- IGNORE ---
# Start Arguments
--reset_config: Resets config to default settings

# Completed (To write commit messages):
"""
# Logs Backlog
log_backlog = []
def add_to_backlog(*args):
    message = " ".join(str(arg) for arg in args)
    print(message)
    log_backlog.append(message)

# Dev Tools
use_built_in_config = False
skip_loading = True
create_debug_test_buttons = True
add_to_backlog("Dev Tools Loaded")

# DPI Setup
import ctypes
ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
hdc = user32.GetDC(0)
LOGPIXELSX = 88
dpi = gdi32.GetDeviceCaps(hdc, LOGPIXELSX)
scale = dpi / 96.0
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
add_to_backlog("DPI Tools Loaded")

# Imports
import os, sys, threading, pyautogui, time, ctypes, pathlib, json, win32gui, win32con, re, requests, io, zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout,
QHBoxLayout, QTabWidget, QMessageBox, QProgressBar, QStackedWidget, QComboBox, QLineEdit, QDialog,
    QDialogButtonBox, QScrollArea, QCheckBox, QFrame, QSlider, QRubberBand, QPlainTextEdit, QLineEdit)
from PyQt6.QtGui import QIcon, QGuiApplication, QColor, QPainter, QDesktopServices
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QSize, QRect, QPoint, QEventLoop, QUrl
from pyscreeze import ImageNotFoundException as pyscreeze_ImageNotFoundException
from PIL import Image, ImageGrab
from pynput import keyboard, mouse
from mousekey import MouseKey
from copy import deepcopy
import numpy as np
add_to_backlog("Imports Loaded")
                   
# Setup Imports
mkey = MouseKey()
local_appdata_directory = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Dark Sol"
config_path = local_appdata_directory / "Dark Sol config.json"
os.makedirs(local_appdata_directory, exist_ok=True)
add_to_backlog("Imports Initalized")

# Constants
current_version = "0.0.0.0"
folders_to_check = ("Icons", "Images")
icons_to_check = ("up chevron.svg", "down chevron.svg", "up chevron disabled.svg")
images_to_check = ("add button.png", "amount box.png", "auto add button.png", "craft button.png", "potion search bar.png", "open recipe button.png",
                    "potion menu item button.png", "zeus potion selection button.png",
                    "poseidon potion selection button.png","hades potion selection button.png",
                    "add completed checkmark.png","play button.png")
add_to_backlog("Constants Loaded")

# File Verification
def download_from_repo(file, output_directory, tag=f"v{current_version}", folder=False, inner_folder_location=None):
    if inner_folder_location == None:
        add_to_backlog(f"Downloading {file} from repo...")
        add_to_backlog(f"URL: https://github.com/Mr-Bored-Bored/Dark-Sol/releases/download/{tag}/{str(file).replace(' ', '%20')}{".zip" if folder else ""}")
        github_file = requests.get(f"https://github.com/Mr-Bored-Bored/Dark-Sol/releases/download/{tag}/{str(file).replace(' ', '%20')}{".zip" if folder else ""}", timeout=20)
        add_to_backlog(f"Finished downloading {file} from repo")
        file_content = github_file.content
        add_to_backlog("Get file content")
        add_to_backlog(file_content)
        add_to_backlog("File Response Code:", github_file.status_code)
        if github_file.status_code != 200:
            raise Exception(f"Failed to download {file} from repo, status code: {github_file.status_code}")
        output_directory.mkdir(parents=True, exist_ok=True)
        add_to_backlog("Created output directory if it did not exist")
        if folder:
            add_to_backlog(f"Extracting {file} to {output_directory}...")
            with zipfile.ZipFile(io.BytesIO(file_content)) as zip_extractor:
                zip_extractor.extractall(output_directory)
            add_to_backlog(f"Finished extracting {file} to {output_directory}")
        else:
            add_to_backlog(f"Saving {file} to {output_directory}...")
            out_path = output_directory / str(file)
            with open(out_path, "wb") as f:
                f.write(file_content)
            add_to_backlog(f"Finished saving {file} to {out_path}")
    else:
        add_to_backlog(f"Downloading {inner_folder_location[0]} from repo...")
        add_to_backlog(f"URL: https://github.com/Mr-Bored-Bored/Dark-Sol/releases/download/{tag}/{str(inner_folder_location[0]).replace(' ', '%20')}{".zip" if folder else ""}")
        github_file = requests.get(f"https://github.com/Mr-Bored-Bored/Dark-Sol/releases/download/{tag}/{str(inner_folder_location[0]).replace(' ', '%20')}{".zip" if folder else ""}", timeout=20)
        add_to_backlog(f"Finished downloading {inner_folder_location[0]} from repo")
        file_content = github_file.content
        add_to_backlog("File Response Code:", github_file.status_code)
        if github_file.status_code != 200:
            raise Exception(f"Failed to download {inner_folder_location[0]} from repo, status code: {github_file.status_code}")
        output_directory.mkdir(parents=True, exist_ok=True)
        add_to_backlog("Created output directory if it did not exist")
        add_to_backlog(f"Extracting {file} to {output_directory}...")
        with zipfile.ZipFile(io.BytesIO(file_content)) as zip_extractor:
            add_to_backlog(zip_extractor.namelist()[:20])
            for name in zip_extractor.namelist():
                if not name.startswith(inner_folder_location[1]) or name.endswith("/"):
                    continue

                rel = name[len(inner_folder_location[1]):]
                out_path = output_directory / rel
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(zip_extractor.read(name))

def verify_folders(folder, path, tag=f"v{current_version}"):
    folder_location = path / folder
    if not folder_location.exists():
        add_to_backlog(f"{folder} does not exist, downloading...")
        inner_prefix = "Lib/" if folder == "Lib" else f"Lib/{folder}/"
        download_from_repo(folder, folder_location, tag=tag, folder=True, inner_folder_location=("Lib", inner_prefix))
    else:
        add_to_backlog(f"{folder} already exists, skipping download")

def verify_files(file, path, tag=f"v{current_version}"):
    file_location = path / file
    if not file_location.exists():
        add_to_backlog(f"{file} does not exist, downloading...")
        if path.name in ("Images", "Icons") and path.parent.name == "Lib":
            download_from_repo(file, path, tag=tag, folder=True, inner_folder_location=("Lib", f"Lib/{path.name}/"))
        else:
            download_from_repo(file, path, tag=tag)
    else:
        add_to_backlog(f"{file} already exists, skipping download")

verify_folders("Lib", local_appdata_directory)

for folder_to_check in folders_to_check:
    verify_folders(folder_to_check, local_appdata_directory / "Lib")

for image_file in images_to_check:
    verify_files(image_file, local_appdata_directory / "Lib" / "Images")

for icon_file in icons_to_check:
    verify_files(icon_file, local_appdata_directory / "Lib" / "Icons")

add_to_backlog("File Verification Completed")

# Config and Data
def nice_config_save(ind=4):
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
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(text)

hidden_config = {
    "data": {
        "scroll amounts": {"to_5": 17, "past_5": 51},
        "position data": {
            "add button 1": {"confidence": 0.75},
            "add button 2": {"confidence": 0.75},
            "add button 3": {"confidence": 0.75},
            "add button 4": {"confidence": 0.75},
            "add button 5": {"confidence": 0.75, "scroll check confidence": 0.75},
            "amount box 1": {"confidence": 0.75},
            "amount box 2": {"confidence": 0.75},
            "amount box 3": {"confidence": 0.75},
            "amount box 4": {"confidence": 0.75},
            "amount box 5": {"confidence": 0.75},
            "auto add button": {"confidence": 0.75},
            "craft button": {"confidence": 0.75},
            "potion search bar": {"confidence": 0.75},
            "open recipe button": {"confidence": 0.75},
            "potion menu item button": {"confidence": 0.75},
            "potion selection button 1": {"confidence": 0.75},
            "potion selection button 2": {"confidence": 0.9},
            "potion selection button 3": {"confidence": 0.9},
            "add completed checkmark 1": {"confidence": 0.8}
        }
    },
    "positions": {
        "add button 1": {"bbox": [1080, 460, 1185, 487], "center": [1132, 473]},
        "add button 2": {"bbox": [1081, 514, 1186, 541], "center": [1133, 527]},
        "add button 3": {"bbox": [1081, 568, 1186, 595], "center": [1133, 581]},
        "add button 4": {"bbox": [1081, 622, 1186, 649], "center": [1133, 635]},
        "add button 5": {"bbox": [1081, 659, 1186, 686], "center": [1133, 672]},
        "amount box 1": {"bbox": [969, 458, 1076, 488], "center": [1022, 473]},
        "amount box 2": {"bbox": [969, 512, 1076, 542], "center": [1022, 527]},
        "amount box 3": {"bbox": [969, 566, 1076, 596], "center": [1022, 581]},
        "amount box 4": {"bbox": [969, 620, 1076, 650], "center": [1022, 635]},
        "amount box 5": {"bbox": [969, 657, 1076, 687], "center": [1022, 672]},
        "potion menu item button": {"bbox": [1393, 250, 1630, 285], "center": [1511, 267]},
        "potion selection button 1": {"bbox": [1407, 337, 1857, 465], "center": [1632, 401]},
        "potion selection button 2": {"bbox": [1408, 473, 1855, 600], "center": [1631, 536]},
        "potion selection button 3": {"bbox": [1407, 605, 1855, 735], "center": [1631, 670]},
        "auto add button": {"bbox": [371, 848, 508, 893], "center": [439, 870]},
        "craft button": {"bbox": [959, 716, 1207, 749], "center": [1083, 732]},
        "potion search bar": {"bbox": [1405, 293, 1857, 325], "center": [1631, 309]},
        "open recipe button": {"bbox": [68, 842, 366, 897], "center": [217, 869]},
        "add completed checkmark 1": {"bbox": [942, 458, 978, 488], "center": [960, 480]},
        "add completed checkmark 2": {"bbox": [942, 512, 978, 542], "center": [960, 480]},
        "add completed checkmark 3": {"bbox": [942, 566, 978, 596], "center": [960, 480]},
        "add completed checkmark 4": {"bbox": [942, 620, 978, 650], "center": [960, 480]},
        "add completed checkmark 5": {"bbox": [942, 657, 978, 687], "center": [960, 480]}
    },
    "item presets": {
        "Main": {
            "bound": {
                "buttons to check": ["add button 1"],
                "additional buttons to click": ["add button 4"],
                "crafting slots": 4,
                "instant craft": True,
                "enabled": False,
                "collapsed": False
            },
            "heavenly": {
                "buttons to check": ["add button 2", "add button 3"],
                "additional buttons to click": ["add button 1"],
                "crafting slots": 5,
                "instant craft": False,
                "enabled": True,
                "collapsed": False
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
            }
        }
    },
    "current preset": "Main",
    "private server link": ""
}
if config_path.exists() and not use_built_in_config:
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
else:
    config = hidden_config
    nice_config_save()

data = {
            "position data": {
                    "add button": {
                        "sub positions": ["add button 1", "add button 2", "add button 3", "add button 4", "add button 5"],
                        "image path": "add button.png"
                        },
                    "amount box": {
                        "sub positions": ["amount box 1", "amount box 2", "amount box 3", "amount box 4", "amount box 5"],
                        "image path": "amount box.png"
                        },
                    "auto add button": {
                        "image path": "auto add button.png"
                        },
                    "craft button": {
                        "image path": "craft button.png"
                        },
                    "potion search bar": {
                        "image path": "potion search bar.png"
                        },
                    "open recipe button": {
                        "image path": "open recipe button.png"
                        },
                    "potion menu item button": {
                        "image path": "potion menu item button.png"
                        },
                    "potion selection button 1": {
                        "image path": "zeus potion selection button.png"
                        },
                    "potion selection button 2": {
                        "image path": "poseidon potion selection button.png"
                        },
                    "potion selection button 3": {
                        "image path": "hades potion selection button.png"
                        },
                    "add completed checkmark": {
                        "sub positions": ["add completed checkmark 1", "add completed checkmark 2", "add completed checkmark 3", "add completed checkmark 4", "add completed checkmark 5"],
                        "image path": "add completed checkmark.png"
                        },
                    "play button": {
                        "image path": "play button.png"
                        }
                    },
                "template data": {
                    "add button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "amount box.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "auto add button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "craft button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "potion search bar.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "open recipe button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "potion menu item button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "zeus potion selection button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "poseidon potion selection button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "hades potion selection button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "add completed checkmark.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        },
                    "play button.png": {
                        "scale": 1.25,
                        "resolution": (1920, 1200)
                        }
                    },

            "item data": {
                    "bound": {
                        "name to search": "bound",
                        "button names": {
                            "add button 1": "Bounded",
                            "add button 2": "Permafrost",
                            "add button 3": "Lost Soul",
                            "add button 4": "Lucky Potion"
                        },
                        "amounts to add": {"add button 2": 3, "add button 4": 100},
                        "crafting slots": 4
                    },
                    "heavenly": {
                        "name to search": "heavenly",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Celestial",
                            "add button 3": "Exotic",
                            "add button 4": "Powered",
                            "add button 5": "Quartz"
                        },
                        "amounts to add": {"add button 1": 250, "add button 2": 2},
                        "crafting slots": 5
                    },
                    "zeus": {
                        "name to search": "godly",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Speed Potion",
                            "add button 3": "Zeus",
                            "add button 4": "Stormal",
                            "add button 5": "Wind"
                        },
                        "amounts to add": {"add button 1": 25, "add button 2": 25},
                        "crafting slots": 5,
                        "potion selection button": "1"
                    },
                    "poseidon": {
                        "name to search": "godly",
                        "button names": {
                            "add button 1": "Speed Potion",
                            "add button 2": "Poseidon",
                            "add button 3": "Nautilus",
                            "add button 4": "Aquatic"
                        },
                        "amounts to add": {"add button 1": 50},
                        "crafting slots": 4,
                        "potion selection button": "2"
                    },
                    "hades": {
                        "name to search": "godly",
                        "button names": {
                            "add button 1": "Lucky Potion",
                            "add button 2": "Hades",
                            "add button 3": "Diaboli",
                            "add button 4": "Bleeding"
                        },
                        "amounts to add": {"add button 1": 50},
                        "crafting slots": 4,
                        "potion selection button": "3"
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
                        "amounts to add": {},
                        "crafting slots": 6
                    },
                }
            }

# Loading Screen
class loading_thread(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str, int)
    def run(self):
        if not skip_loading:
            self.progress.emit("Placeholder Load", 0)
            self.progress.emit("Finished Placeholder Load", 1)
            self.finished.emit()
        else:
            self.finished.emit()
class loading_screen(QWidget):
    def __init__(self):
        super().__init__()
        parts_to_load = 1
        self.loading_bar = QProgressBar(self)
        self.setWindowTitle("Loading Dark Sol")
        self.setStyleSheet(""" QProgressBar {background-color: black; color: white; border-radius: 5px; border: 1px solid black; font-size: 15pt; height: 40px;} QProgressBar::chunk {background-color: lime; }""")
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
    status_signal = pyqtSignal(str, str)
    macro_stopped_signal = pyqtSignal()
    log_signal = pyqtSignal(str)

    def __init__(self):
        # Create main window
        super().__init__()
        self.setWindowTitle("Dark Sol")
        self.setGeometry(int(((screen_width / 2) / scale) - (self.width() / 2)), int(((screen_height / 2) / scale) - (self.height() / 2 )), 0, 0) # Make gui as small as possible and appear in the center of the screen
        # Create Main Gui Elements
        self.central_widget = QWidget()
        self.central_widget_vbox = QVBoxLayout(self.central_widget)
        # Create Tabs
        self.tabs_widget = QTabWidget()
        self.main_tab = QWidget()
        self.presets_tab = QWidget()
        self.calibrations_tab = QWidget()
        self.theme_tab = QWidget()
        self.settings_tab = QWidget()
        # Create Main Tab Elements
        self.status_label = QLabel("Status: Stopped")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.rejoin_and_path_to_potion_gui_button = QPushButton("Rejoin and Path to Potion GUI")
        self.log_area = QPlainTextEdit()
        # Create Presets Tab Elements
        self.current_preset = config["current preset"]
        self.preset_selector = QComboBox()
        self.rename_preset_button = QPushButton("Rename")
        self.delete_preset_button = QPushButton("Delete")
        self.presets_tab_scroller = QScrollArea()
        self.presets_tab_content = QWidget()
        self.up_chevron_svg = str(local_appdata_directory / "Lib" / "Icons" / "up chevron.svg")
        self.down_chevron_svg = str(local_appdata_directory / "Lib" / "Icons" / "down chevron.svg")
        self.up_chevron_disabled_svg = str(local_appdata_directory / "Lib" / "Icons" / "up chevron disabled.svg")
        # Create Calibration Tab Elements
        self.completed_calibrations = []
        self.calibration_mode = "auto"
        self.calibration_mode_button = QPushButton("Current Mode: Automatic Calibration")
        self.show_calibration_overlays_button = QPushButton("Show Calibration Overlays")
        self.calibrations_overlay_active = False
        # Auto Calibration Mode
        self.auto_calibrate_button = QPushButton("Auto Calibrate")
        self.find_add_button = QPushButton("Find Add Buttons")
        self.find_amount_box = QPushButton("Find Amount Boxes")
        self.find_auto_add_button = QPushButton("Find Auto Add Button")
        self.find_craft_button = QPushButton("Find Craft Button")
        self.find_search_bar = QPushButton("Find Search Bar")
        self.find_potion_selection_button = QPushButton("Find Potion Selection Button")
        self.auto_calibrate_add_completed_checkmarks_button = QPushButton("Calibrate Add Completed Checkmarks")
        self.auto_calibrate_scrolling_button = QPushButton("Calibrate Scroll Amounts")
        # Semi Auto Calibration Mode
        self.set_add_button_template = QPushButton("Set Add Button Template")
        self.set_amount_box_template = QPushButton("Set Amount Box Template")
        # Manual Calibration Mode
        self.add_button_coordinates_selector = QWidget()
        self.add_button_coordinates_selector.setWindowTitle("Set Add Button Coordinates")
        self.add_button_coordinates_selector_layout = QVBoxLayout(self.add_button_coordinates_selector)
        self.set_add_button_coordinates = QPushButton("Set Add Button Coordinates", self)
        self.set_add_button_1_coordinates = QPushButton("Set Add Button 1 Coordinates")
        self.set_add_button_2_coordinates = QPushButton("Set Add Button 2 Coordinates")
        self.set_add_button_3_coordinates = QPushButton("Set Add Button 3 Coordinates")
        self.set_add_button_4_coordinates = QPushButton("Set Add Button 4 Coordinates")
        self.set_add_button_5_coordinates = QPushButton("Set Add Button 5 Coordinates")
        self.amount_box_coordinates_selector = QWidget()
        self.amount_box_coordinates_selector.setWindowTitle("Set Amount Box Coordinates")
        self.amount_box_coordinates_selector_layout = QVBoxLayout(self.amount_box_coordinates_selector)
        self.set_amount_box_coordinates = QPushButton("Set Amount Box Coordinates", self)
        self.set_amount_box_1_coordinates = QPushButton("Set Amount Box 1 Coordinates")
        self.set_amount_box_2_coordinates = QPushButton("Set Amount Box 2 Coordinates")
        self.set_amount_box_3_coordinates = QPushButton("Set Amount Box 3 Coordinates")
        self.set_amount_box_4_coordinates = QPushButton("Set Amount Box 4 Coordinates")
        self.set_amount_box_5_coordinates = QPushButton("Set Amount Box 5 Coordinates")
        self.set_auto_add_button_coordinates = QPushButton("Set Auto Add Button Coordinates")
        self.set_amount_box_coordinates = QPushButton("Set Amount Box Coordinates")
        self.set_craft_button_coordinates = QPushButton("Set Craft Button Coordinates")
        self.set_search_bar_coordinates = QPushButton("Set Search Bar Coordinates")
        self.set_potion_selection_button_coordinates = QPushButton("Set Potion Selection Button Coordinates")
        self.calibrate_add_completed_checkmarks_button = QPushButton("Manually Calibrate Add Completed Checkmarks")
        self.manually_calibrate_scrolling_button = QPushButton("Manually Calibrate Scroll Amounts")
        # Settings Tab
        self.ps_link_label = QLabel("Private Server Link:")
        self.ps_link_line = QLineEdit()
        self.ps_link_save_button = QPushButton("Save Private Server Link")
        self.ps_link_join_button = QPushButton("Join Private Server")
        self.reset_add_button_template_button = QPushButton("Reset Add Button Template")
        self.reset_amount_box_template_button = QPushButton("Reset Amount Box Template")
        # Create Donations Stuff
        self.donate_label = QLabel("Donate")
        # Mini Status Label 
        self.mini_status_widget = QWidget()
        self.general_mini_status_label = QLabel("Stopped")
        self.mini_status_label = QLabel()
        # Create Running Variables
        self.scroll_calibration_safety_check = True
        self.auto_add_waitlist = []
        self.current_auto_add_potion = None
        self.macro_timer = QTimer(self)
        self.run_event = threading.Event()
        self.worker = None
        self.macro_stopped_signal.connect(self.on_macro_stopped)
        self.status_signal.connect(self.inner_update_status)
        self.log_signal.connect(self.inner_log)
        self.init_ui()
        self.setup_hotkeys()
        self.catch_up_log()

        if create_debug_test_buttons:
            self.debug_tab = QWidget()
            self.tabs_widget.addTab(self.debug_tab, "Debug")
            self.debug_tab_qv_layout = QVBoxLayout()
            self.debug_test_button_1 = QPushButton("Test Button 1", self)
            self.debug_test_button_2 = QPushButton("Test Button 2", self)
            self.debug_test_button_3 = QPushButton("Test Button 3", self)
            self.debug_test_button_4 = QPushButton("Test Button 4", self)
            self.debug_test_button_5 = QPushButton("Test Button 5", self)
            self.debug_tab_qv_layout.addWidget(self.debug_test_button_1)
            self.debug_tab_qv_layout.addWidget(self.debug_test_button_2)
            self.debug_tab_qv_layout.addWidget(self.debug_test_button_3)
            self.debug_tab_qv_layout.addWidget(self.debug_test_button_4)
            self.debug_tab_qv_layout.addWidget(self.debug_test_button_5)
            self.debug_tab.setStyleSheet("QPushButton {font-size: 22pt;}")
            self.debug_tab_qv_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.debug_tab.setLayout(self.debug_tab_qv_layout)

            self.debug_test_button_1.clicked.connect(lambda: self.log("Test Button 1 Pressed"))
            self.debug_test_button_2.clicked.connect(lambda: self.log("Test Button 2 Pressed"))
            self.debug_test_button_3.clicked.connect(lambda: self.log("Test Button 3 Pressed"))
            self.debug_test_button_4.clicked.connect(lambda: self.log("Test Button 4 Pressed"))
            self.debug_test_button_5.clicked.connect(lambda: self.log("Test Button 5 Pressed"))

    def init_ui(self):
        # Initalize Main Gui
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.central_widget_vbox)
        self.central_widget_vbox.addWidget(self.tabs_widget)
        self.central_widget_vbox.setContentsMargins(0,0,0,0)
        # Initialize Tabs
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
        main_tab_vbox.addWidget(self.rejoin_and_path_to_potion_gui_button)
        main_tab_vbox.addWidget(self.log_area)
        self.log_area.setReadOnly(True)
        self.main_tab.setLayout(main_tab_vbox)
        self.log_area.setStyleSheet("background-color: #0f0f0f; color: white; font-size: 11pt; padding: 1px;")
        #Set Presets Tab Layout
        self.preset_selector.addItems(list(config["item presets"].keys()) + ["Create New Preset"])
        self.preset_selector.setStyleSheet("color: cyan; background: #111; font-size: 18pt; padding: 6px;")
        self.preset_selector.setMinimumHeight(52)
        self.preset_selector.blockSignals(True)
        self.preset_selector.setCurrentText(self.current_preset)
        self.preset_selector.blockSignals(False)
        self.rename_preset_button.setStyleSheet("color: cyan; background: #111; font-size: 18pt; padding: 6px;")
        self.delete_preset_button.setStyleSheet("color: red; background: #111; font-size: 18pt; padding: 6px; border: 1px solid red;")
        presets_header = QWidget()
        presets_header_layout = QHBoxLayout(presets_header)
        presets_header_layout.setContentsMargins(0, 0, 0, 0)
        presets_header_layout.setSpacing(10)
        presets_header_layout.addWidget(self.preset_selector, 1)
        presets_header_layout.addWidget(self.rename_preset_button)
        presets_header_layout.addWidget(self.delete_preset_button)
        self.presets_tab_scroller.setWidget(self.presets_tab_content)
        self.presets_tab_scroller.setFrameShape(QFrame.Shape.NoFrame)
        self.presets_tab_scroller.setWidgetResizable(True)
        self.presets_tab_scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.presets_tab_scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.presets_tab_content_layout = QVBoxLayout(self.presets_tab_content)
        self.presets_tab_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.presets_tab_main_vbox = QVBoxLayout()
        self.presets_tab_main_vbox.addWidget(presets_header)
        self.presets_tab_main_vbox.addWidget(self.presets_tab_scroller)
        self.presets_tab.setStyleSheet("""
                    QWidget { background-color: black; }
                    QLabel { color: cyan; font-size: 14pt; }
                    QCheckBox { color: cyan; font-size: 11pt; }
                    QScrollArea { border: 0px; }
                """)
        self.presets_tab.setLayout(self.presets_tab_main_vbox)
        self.build_potions_ui()
        # Set Calibrations Tab Layout
        self.calibrations_tab_main_vbox = QVBoxLayout()
        self.calibrations_stack = QStackedWidget()
        self.calibration_mode_button.setToolTip("Switch between automatic, semi-automatic, and manual calibration modes.")
        # Auto Calibration Page
        auto_calibration_page = QWidget()
        auto_layout = QVBoxLayout(auto_calibration_page)
        auto_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        auto_layout.addWidget(self.auto_calibrate_button)
        auto_layout.addWidget(self.find_add_button)
        auto_layout.addWidget(self.find_amount_box)
        auto_layout.addWidget(self.find_auto_add_button)
        auto_layout.addWidget(self.find_craft_button)
        auto_layout.addWidget(self.find_search_bar)
        auto_layout.addWidget(self.find_potion_selection_button)
        auto_layout.addWidget(self.auto_calibrate_add_completed_checkmarks_button)
        auto_layout.addWidget(self.auto_calibrate_scrolling_button)
        # Semi Auto Calibration Page
        semi_auto_calibration_page = QWidget()
        semi_auto_layout = QVBoxLayout(semi_auto_calibration_page)
        semi_auto_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        semi_auto_layout.addWidget(self.set_add_button_template)
        semi_auto_layout.addWidget(self.set_amount_box_template)
        # Manual Calibration Page
        manual_calibration_page = QWidget()
        manual_layout = QVBoxLayout(manual_calibration_page)
        manual_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_1_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_2_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_3_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_4_coordinates)
        self.add_button_coordinates_selector_layout.addWidget(self.set_add_button_5_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_1_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_2_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_3_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_4_coordinates)
        self.amount_box_coordinates_selector_layout.addWidget(self.set_amount_box_5_coordinates)
        manual_layout.addWidget(self.set_add_button_coordinates)
        manual_layout.addWidget(self.set_amount_box_coordinates)
        manual_layout.addWidget(self.set_auto_add_button_coordinates)
        manual_layout.addWidget(self.set_craft_button_coordinates)
        manual_layout.addWidget(self.set_search_bar_coordinates)
        manual_layout.addWidget(self.set_potion_selection_button_coordinates)
        manual_layout.addWidget(self.calibrate_add_completed_checkmarks_button)
        manual_layout.addWidget(self.manually_calibrate_scrolling_button)
        self.add_button_coordinates_selector.setStyleSheet("QWidget {background-color: black;} QPushButton {color: cyan;border: 2px solid cyan; border-radius: 6px; font-size: 22pt;}")
        self.amount_box_coordinates_selector.setStyleSheet("QWidget {background-color: black;} QPushButton {color: cyan;border: 2px solid cyan; border-radius: 6px; font-size: 22pt;}")
        self.add_button_coordinates_selector.adjustSize()
        self.amount_box_coordinates_selector.adjustSize()
        # Calibration Pages Setup
        self.calibrations_stack.addWidget(auto_calibration_page)       # index 0
        self.calibrations_stack.addWidget(semi_auto_calibration_page)  # index 1
        self.calibrations_stack.addWidget(manual_calibration_page)     # index 2
        self.calibrations_tab_main_vbox.addWidget(self.calibration_mode_button)
        self.calibrations_tab_main_vbox.addWidget(self.show_calibration_overlays_button)
        self.calibrations_tab_main_vbox.addWidget(self.calibrations_stack)
        self.calibrations_stack.setCurrentIndex(0)
        self.calibrations_tab.setLayout(self.calibrations_tab_main_vbox)
        # Settings Tab Layout
        settings_tab_vbox = QVBoxLayout(self.settings_tab)
        private_server_hbox = QHBoxLayout()
        self.ps_link_line.setPlaceholderText("Enter private server link here")
        if config["private server link"] != "":
            self.ps_link_line.setText(config["private server link"])
        private_server_hbox.addWidget(self.ps_link_label)
        private_server_hbox.addWidget(self.ps_link_line)
        settings_tab_vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        settings_tab_vbox.addLayout(private_server_hbox)
        self.ps_link_save_button
        settings_tab_vbox.addWidget(self.ps_link_save_button)
        self.ps_link_join_button
        self.ps_link_join_button.setToolTip("Must save private server before clicking")
        settings_tab_vbox.addWidget(self.ps_link_join_button)
        settings_tab_vbox.addWidget(self.reset_add_button_template_button)
        settings_tab_vbox.addWidget(self.reset_amount_box_template_button)
        # Donations Layout
        self.donate_row = QWidget()
        donate_row_layout = QHBoxLayout(self.donate_row)
        donate_row_layout.setContentsMargins(0, 0, 0, 0)
        donate_row_layout.addStretch(1)
        donate_row_layout.addWidget(self.donate_label)
        self.central_widget_vbox.addWidget(self.donate_row)
        self.donate_label.setAlignment(Qt.AlignmentFlag.AlignRight)
       
        self.donate_label.setTextFormat(Qt.TextFormat.RichText)
        self.donate_label.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        self.donate_label.setOpenExternalLinks(True)
        self.donate_label.setStyleSheet("padding-right: 12px; padding-bottom: 6px;")
        self.donate_label.setMouseTracking(True)
        self.donate_label.setCursor(Qt.CursorShape.ArrowCursor)
        self.donate_label_color = 0

        def change_donate_label_color():
            hovered = self.donate_label.underMouse()
            self.donate_label.setCursor(
                Qt.CursorShape.PointingHandCursor if hovered
                else Qt.CursorShape.ArrowCursor
            )
            self.donate_label_color = (self.donate_label_color + 2) % 360
            color = QColor.fromHsv(self.donate_label_color, 255, 255).name()
            underline = "underline" if hovered else "none"
            self.donate_label.setText(
                f'<a href="https://www.roblox.com/games/74832430065070/The-Bank#!/store" style="color:{color}; text-decoration:{underline};">Donate</a>')
        # Timer (keep a reference on self so it never gets GC’d)
        self.donate_timer = QTimer(self)
        self.donate_timer.timeout.connect(change_donate_label_color)
        self.donate_timer.start(30)

        change_donate_label_color()
        
        # Button Connectors
        self.calibration_mode_button.clicked.connect(lambda: self.switch_calibration_mode())
        self.show_calibration_overlays_button.clicked.connect(lambda: self.show_calibration_overlays())

        self.auto_calibrate_button.clicked.connect(self.auto_calibrate)
        self.find_add_button.clicked.connect(lambda: self.find_add_buttons())
        self.find_amount_box.clicked.connect(lambda: self.find_amount_boxes())
        self.find_auto_add_button.clicked.connect(lambda: (self.focus_roblox(), time.sleep(0.2), self.safe_image_find("auto add button")))
        self.find_craft_button.clicked.connect(lambda: (self.focus_roblox(), time.sleep(0.2), self.safe_image_find("craft button")))
        self.find_search_bar.clicked.connect(lambda: (self.focus_roblox(), time.sleep(0.2), self.safe_image_find("potion search bar")))
        self.auto_calibrate_add_completed_checkmarks_button.clicked.connect(self.find_and_calibrate_checkmarks)
        self.find_potion_selection_button.clicked.connect(lambda: self.find_potion_selection_buttons())
        self.auto_calibrate_scrolling_button.clicked.connect(lambda: self.auto_calibrate_scrolling())    

        self.set_add_button_coordinates.clicked.connect(lambda: self.add_button_coordinates_selector.show())
        self.set_add_button_1_coordinates.clicked.connect(lambda: self.manual_calibration("add button 1"))
        self.set_add_button_2_coordinates.clicked.connect(lambda: self.manual_calibration("add button 2"))
        self.set_add_button_3_coordinates.clicked.connect(lambda: self.manual_calibration("add button 3"))
        self.set_add_button_4_coordinates.clicked.connect(lambda: self.manual_calibration("add button 4"))
        self.set_add_button_5_coordinates.clicked.connect(lambda: self.manual_calibration("add button 5"))
        self.set_amount_box_coordinates.clicked.connect(lambda: self.amount_box_coordinates_selector.show())
        self.set_amount_box_1_coordinates.clicked.connect(lambda: self.manual_calibration("amount box 1"))
        self.set_amount_box_2_coordinates.clicked.connect(lambda: self.manual_calibration("amount box 2"))
        self.set_amount_box_3_coordinates.clicked.connect(lambda: self.manual_calibration("amount box 3"))
        self.set_amount_box_4_coordinates.clicked.connect(lambda: self.manual_calibration("amount box 4"))
        self.set_amount_box_5_coordinates.clicked.connect(lambda: self.manual_calibration("amount box 5"))
        self.set_auto_add_button_coordinates.clicked.connect(lambda: self.manual_calibration("auto add button"))
        self.set_craft_button_coordinates.clicked.connect(lambda: self.manual_calibration("craft button"))
        self.set_search_bar_coordinates.clicked.connect(lambda: self.manual_calibration("potion search bar"))
        self.set_potion_selection_button_coordinates.clicked.connect(lambda: self.manual_calibration("potion selection button"))
        self.calibrate_add_completed_checkmarks_button.clicked.connect(lambda: self.manual_checkmarks_calibration())
        self.manually_calibrate_scrolling_button.clicked.connect(lambda: self.manual_scroll_calibration())
        self.ps_link_save_button.clicked.connect(lambda: (config.__setitem__("private server link", self.ps_link_line.text()), nice_config_save()))
        self.ps_link_join_button.clicked.connect(lambda: self.open_roblox(config["private server link"]))
        self.set_add_button_template.clicked.connect(lambda: self.replace_template("add button"))
        self.set_amount_box_template.clicked.connect(lambda: self.replace_template("amount box"))
        self.reset_add_button_template_button.clicked.connect(lambda: verify_files("add_button.png", local_appdata_directory / "Lib" / "Images"))
        self.reset_amount_box_template_button.clicked.connect(lambda: verify_files("amount_box.png", local_appdata_directory / "Lib" / "Images"))
        self.rejoin_and_path_to_potion_gui_button.clicked.connect(lambda: self.reload_potion_gui())

        self.preset_selector.currentTextChanged.connect(lambda: self.switch_preset(self.preset_selector.currentText()) if self.preset_selector.currentText() != "Create New Preset" else self.create_new_preset())
        self.rename_preset_button.clicked.connect(self.rename_preset)
        self.delete_preset_button.clicked.connect(self.delete_preset)
        #Status Label Setup
        self.mini_status_widget.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.mini_status_widget.setStyleSheet("background-color: black; border: 2px solid cyan; border-radius: 6px;")
        self.general_mini_status_label.setStyleSheet("color: cyan; font-size: 15pt;")
        self.mini_status_label.setStyleSheet("color: cyan; font-size: 15pt;")
        self.mini_status_qv = QVBoxLayout(self.mini_status_widget)
        self.mini_status_qv.setContentsMargins(0, 0, 0, 0)
        self.mini_status_qv.addWidget(self.general_mini_status_label)
        self.mini_status_qv.addWidget(self.mini_status_label)
        self.mini_status_widget.move(600, 75)
        self.mini_status_qv.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.general_mini_status_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.mini_status_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # Set Ui Theme
        self.status_label.setObjectName("status_label")
        self.start_button.setObjectName("start_button")
        self.stop_button.setObjectName("stop_button")
        self.calibrations_tab.setObjectName("calibrations_tab")
        self.setStyleSheet("""
            QMainWindow {background-color: black; }
            QTabBar::tab { background-color: #222; }
            QTabBar::tab:selected { background-color: black; }
            QTabBar {color: cyan;}
            QWidget {background-color: black;}
            QPushButton {background-color: black; color: cyan; border-radius: 5px; border: 1px solid cyan; font-size: 15pt;}
            QPushButton#start_button {font-size: 22pt;}
            QPushButton#stop_button {font-size: 22pt;}
            QLabel {color: cyan; font-size: 14pt;}
            QLabel#status_label {color: cyan; font-size: 38pt;}
        """)
        # Setup  Hotkeys
        self.start_button.clicked.connect(self.start_macro)
        self.stop_button.clicked.connect(self.stop_macro)
        
    def reset_template(self):
        pass

    def auto_calibrate_scrolling(self):
        if not self.calibrate_scrolling():
            self.adjust_template_settings("add button 5", what_to_save=None, multiple=True, ignore_match_not_found=True, scroll_check=True, region=(0, config["positions"]["add button 4"]["bbox"][3], screen_width, config["positions"]["add button 5"]["bbox"][3] - config["positions"]["add button 4"]["bbox"][3]))

    def catch_up_log(self):
        for log in log_backlog:
            self.log(log)
    
    def replace_template(self, template_name):
        image_location = data["position data"][template_name]["image path"]
        image_path = str(local_appdata_directory / "Lib" / "Images" / image_location)
        if not (new_template_bbox := self.select_region()):
            return
        else:
            ImageGrab.grab(new_template_bbox).save(image_path)

    def open_roblox(self, link):
        def convert_roblox_link(url):
            game_pattern = r"https://www.roblox.com/games/(\d+)/[^?]+\?privateServerLinkCode=(\d+)"
            share_pattern = r"https://www.roblox.com/share\?code=([a-f0-9]+)&type=([A-Za-z]+)"
            match_game = re.match(game_pattern, url)
            if match_game:
                place_id = match_game.group(1)
                link_code = match_game.group(2)
                if place_id != "15532962292":
                    return None
                link_code = "".join(filter(str.isdigit, link_code))
                return f"roblox://placeID={place_id}&linkCode={link_code}"

            match_share = re.match(share_pattern, url)
            if match_share:
                code = match_share.group(1)
                share_type = match_share.group(2)
                if "Server" in share_type:
                    share_type = "Server"
                elif "ExperienceInvite" in share_type:
                    share_type = "ExperienceInvite"
                return f"roblox://navigation/share_links?code={code}&type={share_type}"
            
        main_url = convert_roblox_link(link)
        QDesktopServices.openUrl(QUrl(main_url))

    def reload_potion_gui(self):
        self.open_roblox(config["private server link"])

        while True:
            self.focus_roblox()
            if self.auto_find_image("play button", what_to_save=None, ignore_match_not_found=True):
                self.move_and_click((270,1050))
                break
            time.sleep(1)
        
        time.sleep(2)
        self.path_to_potion_gui()

    def path_to_potion_gui(self):
        self.move_and_click((40,500))
        self.move_and_click((414,163))

        time.sleep(0.2)
        mkey.right_mouse_down()
        time.sleep(0.2)
        mkey.move_relative(0, screen_height*2)
        time.sleep(0.2)
        mkey.right_mouse_up()

        time.sleep(5)
        keyboard.Controller().press('s')
        time.sleep(0.0059)
        keyboard.Controller().press('a')
        time.sleep(3.1014)
        keyboard.Controller().release('a')
        time.sleep(3.0857)
        keyboard.Controller().release('s')
        time.sleep(0.1841)
        keyboard.Controller().press('d')
        time.sleep(0.9020)
        keyboard.Controller().press('s')
        time.sleep(0.3860)
        keyboard.Controller().release('s')
        time.sleep(0.0772)
        keyboard.Controller().release('d')
        time.sleep(0.1619)
        keyboard.Controller().press('w')
        time.sleep(0.1413)
        keyboard.Controller().release('w')
        time.sleep(0.0856)
        keyboard.Controller().press(keyboard.Key.space)
        time.sleep(0.1184)
        keyboard.Controller().press('d')
        time.sleep(0.0255)
        keyboard.Controller().release(keyboard.Key.space)
        time.sleep(0.2294)
        keyboard.Controller().release('d')
        time.sleep(0.2628)
        keyboard.Controller().press('s')
        time.sleep(0.6789)
        keyboard.Controller().press('a')
        time.sleep(0.9100)
        keyboard.Controller().release('a')
        time.sleep(0.9474)
        keyboard.Controller().press('a')
        time.sleep(0.1487)
        keyboard.Controller().release('a')
        time.sleep(3.9572)
        keyboard.Controller().press('a')
        time.sleep(2.2367)
        keyboard.Controller().release('a')
        time.sleep(0.3313)
        keyboard.Controller().press('a')
        time.sleep(0.1747)
        keyboard.Controller().release('a')
        time.sleep(0.7474)
        keyboard.Controller().press('a')
        time.sleep(1.2850)
        keyboard.Controller().release('a')
        time.sleep(0.0758)
        keyboard.Controller().release('s')
        time.sleep(0.2941)
        keyboard.Controller().press('w')
        time.sleep(0.0029)
        keyboard.Controller().press('d')
        time.sleep(0.2300)
        keyboard.Controller().release('d')
        time.sleep(0.0002)
        keyboard.Controller().release('w')
        time.sleep(0.2077)
        keyboard.Controller().press(keyboard.Key.space)
        time.sleep(0.0041)
        keyboard.Controller().press('s')
        time.sleep(0.1679)
        keyboard.Controller().release(keyboard.Key.space)
        time.sleep(0.5104)
        keyboard.Controller().release('s')
        time.sleep(0.0555)
        keyboard.Controller().press('a')
        time.sleep(0.0881)
        keyboard.Controller().press(keyboard.Key.space)
        time.sleep(0.1990)
        keyboard.Controller().release(keyboard.Key.space)
        time.sleep(2.8905)
        keyboard.Controller().release('a')
        time.sleep(0.0732)
        keyboard.Controller().press('s')
        time.sleep(1.8236)
        keyboard.Controller().release('s')
        time.sleep(2.6950)
        keyboard.Controller().press('a')
        time.sleep(0.7439)
        keyboard.Controller().release('a')
        time.sleep(0.2463)
        keyboard.Controller().press('f')
        time.sleep(0.0868)
        keyboard.Controller().release('f')
        keyboard.Controller().press('d')
        time.sleep(1)
        keyboard.Controller().release('d')

    def select_region(self):
        loop = QEventLoop()
        selection_result = None

        widget = QWidget()
        widget.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        widget.setMouseTracking(True)
        widget.setCursor(Qt.CursorShape.CrossCursor)

        selection_band = QRubberBand(QRubberBand.Shape.Rectangle, widget)
        drag_start = QPoint()

        def refresh_screen_metrics() -> None: 
            hwnd = int(widget.winId())

        def paint_event(event):  # type: ignore[no-untyped-def]
            p = QPainter(widget)
            p.fillRect(widget.rect(), QColor(120, 120, 120, 80))
            p.end()

        def key_press_event(event):  # type: ignore[no-untyped-def]
            if event is None:
                return
            if event.key() == Qt.Key.Key_Escape:
                loop.quit()

        def mouse_press_event(event):  # type: ignore[no-untyped-def]
            nonlocal drag_start
            if event is None:
                return
            if event.button() != Qt.MouseButton.LeftButton:
                return
            drag_start = event.pos()
            selection_band.setGeometry(QRect(drag_start, drag_start))
            selection_band.show()

        def mouse_move_event(event):  # type: ignore[no-untyped-def]
            if event is None:
                return
            if not selection_band.isVisible():
                return
            selection_band.setGeometry(QRect(drag_start, event.pos()).normalized())

        def mouse_release_event(event):  # type: ignore[no-untyped-def]
            nonlocal selection_result
            if event is None:
                return
            if event.button() != Qt.MouseButton.LeftButton:
                return
            selection_rect = selection_band.geometry().normalized()
            selection_band.hide()

            top_left_global = widget.mapToGlobal(selection_rect.topLeft())
            bottom_right_global = widget.mapToGlobal(
                QPoint(selection_rect.right() + 1, selection_rect.bottom() + 1)
            )
            tl_x = int(round(top_left_global.x() * scale))
            tl_y = int(round(top_left_global.y() * scale))
            br_x = int(round(bottom_right_global.x() * scale))
            br_y = int(round(bottom_right_global.y() * scale))
            selection_result = (tl_x, tl_y, br_x, br_y)
            loop.quit()

        widget.paintEvent = paint_event  # type: ignore[method-assign]
        widget.keyPressEvent = key_press_event  # type: ignore[method-assign]
        widget.mousePressEvent = mouse_press_event  # type: ignore[method-assign]
        widget.mouseMoveEvent = mouse_move_event  # type: ignore[method-assign]
        widget.mouseReleaseEvent = mouse_release_event  # type: ignore[method-assign]

        widget.showFullScreen()
        QTimer.singleShot(0, refresh_screen_metrics)
        loop.exec()
        selection_band.hide()
        widget.close()
        return selection_result

    def manual_calibration(self, calibration_name, save=True, what_to_save=("bbox", "center")):
        self.focus_roblox()
        time.sleep(0.2)
        result = self.select_region()
        if result == None:
            self.log(f"Manual calibration for {calibration_name} was cancelled.")
        else:
            bbox = result
            center = (int((bbox[0] + bbox[2]) // 2), int((bbox[1] + bbox[3]) // 2))
            self.log(f"Manual calibration for {calibration_name} completed successfully.")
            if save:
                if not isinstance(what_to_save, (tuple)):
                    what_to_save = (what_to_save,)
                config["positions"][calibration_name] = {key: value for key, value in [("bbox", bbox), ("center", center)] if key in what_to_save}
                nice_config_save()
                self.log(f"Manual Calibration Coordinates for {calibration_name} saved to config.")
            return bbox, center

    def create_new_preset(self):
        dlg = QDialog(self)
        layout = QVBoxLayout(dlg)
        dlg.setWindowTitle("Create New Preset")
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
            self.preset_selector.setCurrentText(config["current preset"])
            return

        preset_name = name_edit.text().strip()
        if not preset_name or preset_name == None or "":
            QMessageBox.warning(self, "Invalid Name", "Preset name cannot be empty.")
            self.preset_selector.setCurrentText(config["current preset"])
            return
        if preset_name in config["item presets"].keys():
            QMessageBox.warning(self, "Name Exists", "A preset with that name already exists.")
            self.preset_selector.setCurrentText(config["current preset"])
            return

        source_key = config["current preset"]
        if source_key not in config["item presets"]:
            presets = list(config["item presets"].keys())
            source_key = presets[0] if presets else None

        new_preset_value = deepcopy(config["item presets"][source_key])
        config["item presets"][preset_name] = new_preset_value
        self.switch_preset(preset_name)

    def rename_preset(self):
        old_name = self.preset_selector.currentText()

        while True:
            dialog = QDialog(self)
            dialog.setWindowTitle("Rename Preset")
            layout = QVBoxLayout(dialog)
            layout.addWidget(QLabel(f"Rename preset '{old_name}' to:"))

            name_edit = QLineEdit()
            name_edit.setText(old_name)
            name_edit.setStyleSheet("color: cyan; background: #111;")
            layout.addWidget(name_edit)

            buttons = QDialogButtonBox()
            buttons.addButton(QDialogButtonBox.StandardButton.Ok)
            buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            new_name = name_edit.text().strip()
            if new_name == "" or new_name is None:
                QMessageBox.warning(self, "Invalid Name", "Preset name cannot be empty.")
                continue
            if new_name == old_name:
                return
            if new_name in config["item presets"].keys():
                QMessageBox.warning(self, "Name Exists", "A preset with that name already exists.")
                continue
            break

        config["item presets"][new_name] = config["item presets"].pop(old_name)
        config["current preset"] = new_name
        self.current_preset = new_name

        nice_config_save()
        self.preset_selector.blockSignals(True)
        self.preset_selector.clear()
        self.preset_selector.addItems(list(config["item presets"].keys()) + ["Create New Preset"])
        self.preset_selector.setCurrentText(config["current preset"])
        self.preset_selector.blockSignals(False)
        self.rebuild_potions_ui()

    def delete_preset(self):
        preset_name = self.preset_selector.currentText()

        remaining_presets = [p for p in config["item presets"].keys() if p != preset_name]
        if len(remaining_presets) == 0:
            QMessageBox.warning(self, "Cannot Delete", "You must keep at least one preset.")
            return

        while True:
            dialog = QDialog(self)
            dialog.setWindowTitle("Delete Preset")
            layout = QVBoxLayout(dialog)
            warning_label = QLabel(f'Are you sure you want to delete "{preset_name}" this cannot be undone.')
            warning_label.setStyleSheet("color: red; font-size: 14pt;")
            layout.addWidget(warning_label)
            label = QLabel("Select the preset you want to switch to:")
            label.setStyleSheet("font-size: 14pt;")
            layout.addWidget(label)
            next_selector = QComboBox()
            next_selector.setStyleSheet("color: cyan; background: #111; font-size: 14pt; padding: 6px;")
            next_selector.addItem("-- Select preset --")
            next_selector.addItems(remaining_presets)
            layout.addWidget(next_selector)
            buttons = QDialogButtonBox()
            delete_button = QPushButton("Delete")
            delete_button.setStyleSheet("color: red; border: 1px solid red;")
            buttons.addButton(delete_button, QDialogButtonBox.ButtonRole.AcceptRole)
            buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            next_preset = next_selector.currentText()

            if next_preset == "-- Select preset --":
                self.create_msg_box("Select Preset", "Select the preset you want to switch to first.", QMessageBox.Icon.Warning)
                continue

            config["current preset"] = next_preset
            self.current_preset = next_preset
            config["item presets"].pop(preset_name)
            break

        nice_config_save()
        self.preset_selector.blockSignals(True)
        self.preset_selector.clear()
        self.preset_selector.addItems(list(config["item presets"].keys()) + ["Create New Preset"])
        self.preset_selector.setCurrentText(config["current preset"])
        self.preset_selector.blockSignals(False)
        self.rebuild_potions_ui()

    def switch_preset(self, preset_name):
        if config["current preset"] == preset_name:
            return
        config["current preset"] = preset_name
        self.current_preset = preset_name
        nice_config_save()
        self.preset_selector.blockSignals(True)
        self.preset_selector.clear()
        self.preset_selector.addItems(list(config["item presets"].keys()) + ["Create New Preset"])
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
                QCheckBox { color: cyan; font-size: 12pt; spacing: 8px; }
                QCheckBox::indicator { width: 44px; height: 22px; border-radius: 11px; }
                QCheckBox::indicator:unchecked { background-color: #222; border: 1px solid cyan; }
                QCheckBox::indicator:checked { background-color: #0aa; border: 1px solid cyan; }
            """)

        def change_potion_toggle(checked: bool):
            sender = self.sender()
            if sender is None:
                return
            potion = sender.property("potion")
            config_key = sender.property("config_key")
            config["item presets"][self.current_preset][potion][config_key] = bool(checked)
            nice_config_save()

        def check_collapsed_state(sender, potion_config):
            collapse_button_icon = QIcon(self.down_chevron_svg) if potion_config["enabled"] and not potion_config["collapsed"] else QIcon(self.up_chevron_svg)
            collapse_button_icon.addFile(self.up_chevron_disabled_svg, QSize(), QIcon.Mode.Disabled)
            sender.setIcon(collapse_button_icon)

        def change_potion_list(checked: bool):
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
            nice_config_save()

        def collapse_potion():
            sender = self.sender()

            if sender is None or not isinstance(sender, QPushButton):
                return
            
            potion = sender.property("potion")
            body = sender.property("body")
            instant_craft = sender.property("instant craft")
            cb_enabled = sender.property("cb enabled")
            potion_config = config["item presets"][self.current_preset][potion]
            

            if not cb_enabled.isChecked():
                return

            potion_config["collapsed"] = not potion_config["collapsed"]
            collapsed = potion_config["collapsed"]

            check_collapsed_state(sender, potion_config)
            body.setVisible(not collapsed)
            instant_craft.setVisible(not collapsed)

            nice_config_save()
            self.presets_tab_content.adjustSize()
            self.presets_tab_scroller.adjustSize()

        def potion_enabled(checked: bool):
            sender = self.sender()

            if sender is None or not isinstance(sender, QCheckBox):
                return
            
            potion = sender.property("potion")
            body = sender.property("body")
            instant_craft = sender.property("instant craft")
            collapse_button = sender.property("collapse button")
            potion_config = config["item presets"][self.current_preset][potion]

            collapsed = potion_config["collapsed"]
            body.setVisible(checked and not collapsed)
            instant_craft.setVisible(checked and not collapsed)
            collapse_button.setEnabled(checked)
            check_collapsed_state(collapse_button, potion_config)

            nice_config_save()
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
            title.setStyleSheet("color: cyan; font-size: 18pt;")
            # Instant Craft Checkbox
            instant_craft_checkbox = QCheckBox("Instant Craft")
            instant_craft_checkbox.setChecked(bool(potion_config["instant craft"]))
            checkbox_into_toggler(instant_craft_checkbox)
            instant_craft_checkbox.setProperty("potion", potion)
            instant_craft_checkbox.setProperty("config_key", "instant craft")
            instant_craft_checkbox.toggled.connect(change_potion_toggle)
            # Enabled Checkbox
            enabled_checkbox = QCheckBox("Enabled")
            enabled_checkbox.setChecked(bool(potion_config["enabled"]))
            checkbox_into_toggler(enabled_checkbox)
            enabled_checkbox.setProperty("potion", potion)
            enabled_checkbox.setProperty("config_key", "enabled")
            enabled_checkbox.toggled.connect(change_potion_toggle)
            # Collapse Button
            collapse_button = QPushButton()
            # Header Layout
            QHLayout.addWidget(title)
            QHLayout.addStretch()
            QHLayout.addWidget(instant_craft_checkbox)
            QHLayout.addWidget(enabled_checkbox)
            QHLayout.addWidget(collapse_button)
            QHLayout.setContentsMargins(6, 6, 6, 6)
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
            left_column_QV_Layout.setSpacing(4)
            left_title = QLabel("Buttons To Check")
            left_title.setStyleSheet("color: cyan; font-size: 15pt;")
            left_column_QV_Layout.addWidget(left_title)
            # Additional Buttons To Click Column (Right)
            right_column = QWidget()
            right_column_QV_Layout = QVBoxLayout(right_column)
            right_column_QV_Layout.setSpacing(4)
            right_title = QLabel("Additional Buttons To Click")
            right_title.setStyleSheet("color: cyan; font-size: 15pt;")
            right_column_QV_Layout.addWidget(right_title)
    
            slots = int(potion_config["crafting slots"])
            for i in range(1, slots + 1):
                btn = f"add button {i}"
                label = potion_data["button names"][btn]
                # Fill Buttons To Check Column (Left)
                buttons_to_check_checkbox = QCheckBox(label)
                buttons_to_check_checkbox.setStyleSheet("""QCheckBox { color: cyan; font-size: 11pt; padding-left: 4pt;}""")
                buttons_to_check_checkbox.setChecked(btn in potion_config["buttons to check"])
                buttons_to_check_checkbox.setProperty("potion", potion)
                buttons_to_check_checkbox.setProperty("list_key", "buttons to check")
                buttons_to_check_checkbox.setProperty("btn", btn)
                buttons_to_check_checkbox.toggled.connect(change_potion_list)
                left_column_QV_Layout.addWidget(buttons_to_check_checkbox)
                # Fill Additional Buttons To Click Column (Right)
                addition_buttons_to_click_checkbox = QCheckBox(label)
                addition_buttons_to_click_checkbox.setStyleSheet("""QCheckBox { color: cyan; font-size: 11pt; padding-left: 4pt;}""")
                addition_buttons_to_click_checkbox.setChecked(btn in potion_config["additional buttons to click"])
                addition_buttons_to_click_checkbox.setProperty("potion", potion)
                addition_buttons_to_click_checkbox.setProperty("list_key", "additional buttons to click")
                addition_buttons_to_click_checkbox.setProperty("btn", btn)
                addition_buttons_to_click_checkbox.toggled.connect(change_potion_list)
                right_column_QV_Layout.addWidget(addition_buttons_to_click_checkbox)
            columns_QH_Layout.addWidget(left_column)
            columns_QH_Layout.addStretch(1)
            columns_QH_Layout.addWidget(right_column)
            QVLayout.addWidget(body)
            # Initial Visibility Setup
            collapsed = potion_config["collapsed"]
            body.setVisible(potion_config["enabled"] and not collapsed)
            instant_craft_checkbox.setVisible(potion_config["enabled"] and not collapsed)
            # Collapse Button Setup
            collapse_button.setStyleSheet("color: cyan; background: #111; border: 1px solid cyan; font-size: 16pt;")
            collapse_button.setEnabled(potion_config["enabled"])
            collapse_button.setIconSize(QSize(45, 35))
            collapse_button.setProperty("potion", potion)
            collapse_button.setProperty("body", body)
            collapse_button.setProperty("instant craft", instant_craft_checkbox)
            collapse_button.setProperty("cb enabled", enabled_checkbox)
            check_collapsed_state(collapse_button, potion_config)
            collapse_button.clicked.connect(collapse_potion)
            # Enabled Checkbox 
            enabled_checkbox.setProperty("body", body)
            enabled_checkbox.setProperty("instant craft", instant_craft_checkbox)
            enabled_checkbox.setProperty("collapse button", collapse_button)
            enabled_checkbox.toggled.connect(potion_enabled)

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
        
    def show_calibration_overlays(self):
        for calibration in config["positions"].keys():
            try:
                bbox = config["positions"][calibration]["bbox"]
            except (TypeError, KeyError):
                bbox = None
                continue
            if self.calibrations_overlay_active:
                self.create_overlay(bbox, disabled=True)
            else:
                self.create_overlay(bbox, text=calibration)
        self.calibrations_overlay_active = not self.calibrations_overlay_active

    def create_msg_box(self, title, text, *buttons, msg_box_type=QMessageBox.Icon.Information, internal=True):
        if internal:
            msg_box = QMessageBox(self)
        else:
            msg_box = QMessageBox()
        msg_box.setIcon(msg_box_type)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStyleSheet("""QLabel { color: cyan; font-size: 14pt;} QWidget {background-color: black;} QPushButton {background-color: black; color: cyan; border-radius: 5px; border: 1px solid cyan; font-size: 15pt;}""")
        if buttons:
            for button in buttons:
                if isinstance(button, str):
                    msg_box.addButton(button, QMessageBox.ButtonRole.AcceptRole)
                else:
                    msg_box.addButton(button)
        else:
            msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.show()
        msg_box.raise_()
        msg_box.activateWindow()
        msg_box.exec()
        clicked = msg_box.clickedButton()
        if clicked is None:
            return False
        clicked_text = clicked.text()
        self.log(f"Button clicked: {clicked_text.lower()}")
        return clicked_text

    def adjust_template_settings(self, calibration, what_to_save=("center", "bbox"), multiple=False, ignore_match_not_found=False, region=None, scroll_check=False):
        return_bool2 = False
        self.focus_roblox()

        def check_if_template_found():
            nonlocal return_bool2

            if not scroll_check:
                if self.auto_find_image(calibration, what_to_save=what_to_save, multiple=multiple, ignore_match_not_found=ignore_match_not_found, region=region):
                    adjust_template_widget.close()
                    self.log(f"Template '{calibration}' found with current settings.")
                    return_bool2 = True
                else:
                    re_raise()
            else: 
                if self.calibrate_scrolling():
                    adjust_template_widget.close()
                    self.log(f"Scroll calibration succeeded with current settings.")
                    return_bool2 = True
                else:
                    re_raise()

        def re_raise():
            adjust_template_widget.raise_()
            adjust_template_widget.activateWindow()

        def update_confidence(calibration):

            if scroll_check:
                config["data"]["position data"][calibration]["scroll check confidence"] = slider.value() / 100.0
                confidence_label.setText(f"Adjust scroll confidence: {slider.value()}%")
            else:
                config["data"]["position data"][calibration]["confidence"] = slider.value() / 100.0
                confidence_label.setText(f"Adjust confidence for '{calibration}': {slider.value()}%")
            nice_config_save()

        adjust_template_widget = QDialog()
        adjust_template_widget.setWindowTitle("Save Position")
        adjust_template_widget.setStyleSheet("""QLabel { color: cyan; font-size: 14pt;} QWidget {background-color: black;} 
                     QPushButton {background-color: black; color: cyan; border-radius: 5px; border: 1px solid cyan; font-size: 15pt;}
                     QSlider::groove:horizontal {height: 8px; background-color: #2b2b2b; border-radius: 4px;}
                     QSlider::sub-page:horizontal {background-color: cyan; border-radius: 4px;}
                     QSlider::add-page:horizontal {background-color: #2b2b2b; border-radius: 4px;}
                     QSlider::handle:horizontal {width: 18px; margin: -6px 0px; background-color: cyan; border: 2px solid #2b2b2b; border-radius: 9px;}
                     """)
        
        adjust_template_widget_layout = QVBoxLayout(adjust_template_widget)

        check_for_button = QPushButton()
        check_for_button.setText("Check For Template" if not scroll_check else "Calibrate Scrolling")
        check_for_button.clicked.connect(check_if_template_found)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(int(config["data"]["position data"][calibration]["confidence"] * 100) if not scroll_check else int(config["data"]["position data"][calibration]["scroll check confidence"] * 100))

        confidence_label = QLabel(slider)
        confidence_label.setText(f"Adjust confidence for '{calibration}': {slider.value()}%" if not scroll_check else f"Adjust scroll confidence: {slider.value()}%")
        slider.valueChanged.connect(lambda value, cal=calibration: update_confidence(cal))

        adjust_template_widget_layout.addWidget(confidence_label)
        adjust_template_widget_layout.addWidget(slider)
        adjust_template_widget_layout.addWidget(check_for_button)
        adjust_template_widget.show()
        adjust_template_widget.raise_()
        adjust_template_widget.activateWindow()
        adjust_template_widget.exec()
        return return_bool2

    def safe_image_find(self, calibration, what_to_save=("center", "bbox"), multiple=False, ignore_match_not_found=False, region=None):
        if not self.auto_find_image(calibration, what_to_save=what_to_save, multiple=multiple, ignore_match_not_found=ignore_match_not_found, region=region):
            if not self.adjust_template_settings(calibration, what_to_save=what_to_save, multiple=multiple, ignore_match_not_found=ignore_match_not_found, region=region):
                self.log(f"Auto Calibration failed at calibration: '{calibration}'")
                return False
        self.log(f"Auto Calibration found, calibration: '{calibration}'")
        return True
    
    def auto_calibrate(self):
        if not self.focus_roblox():
            QMessageBox.warning(self, "Roblox Not Found", "Could not find a Roblox window. Please make sure Roblox is running.")
            return
        
        time.sleep(0.2)
        if not self.safe_image_find("potion menu item button"):
            return
        self.move_and_click(config["positions"]["potion menu item button"]["center"])
        if not self.safe_image_find("potion search bar"):
            return
        self.move_and_click(config["positions"]["potion search bar"]["center"])
        mkey.left_click()
        mkey.left_click()
        keyboard.Controller().type(f"godly")
        time.sleep(0.5)
        keyboard.Controller().press(keyboard.Key.enter)
        time.sleep(0.1)
        for count in range(1, 4):
            if not self.safe_image_find("potion selection button " + str(count + 1)):
                return
        self.move_and_click(config["positions"]["potion selection button 1"]["center"])
        self.move_and_click(config["positions"]["potion search bar"]["center"])
        mkey.left_click()
        mkey.left_click()
        keyboard.Controller().type(f"jewelry")
        time.sleep(0.5)
        keyboard.Controller().press(keyboard.Key.enter)
        time.sleep(0.1)
        self.move_and_click(config["positions"]["potion selection button 1"]["center"])
        if not self.safe_image_find("open recipe button"):
            return
        self.move_and_click(config["positions"]["open recipe button"]["center"])
        if not self.safe_image_find("amount box 1"):
            return
        self.move_and_click(config["positions"]["amount box 1"]["center"], False)
        pyautogui.scroll(2000)
        for add_button in config["positions"]["add button"]["sub positions"][:4]:
            if not self.safe_image_find(add_button, multiple=True):
                return
        for amount_box in config["positions"]["amount box"]["sub positions"][:4]:
            if not self.safe_image_find(amount_box, multiple=True):
                return
        self.move_and_click(config["positions"]["add button 1"]["center"], False)
        pyautogui.scroll(-2000)
        time.sleep(0.1)
        if not self.safe_image_find("add button 5", multiple=True):
            return
        time.sleep(0.1)
        if not self.safe_image_find("amount box 5", multiple=True):
            return
        if not self.safe_image_find("craft button"):
            return
        if not self.safe_image_find("auto add button"):
            return
        pyautogui.scroll(2000)
        if not self.calibrate_scrolling():
            if not self.adjust_template_settings("add button 5", scroll_check=True):
                return
        
        self.move_and_click(config["positions"]["amount box 1"]["center"], False)
        pyautogui.scroll(2000)
        mkey.left_click()
        mkey.left_click
        keyboard.Controller().type("20")
        self.move_and_click(config["positions"]["add button 1"]["center"])
        time.sleep(0.1)

        if not self.safe_image_find("add completed checkmark 1"):
            return
        
        self.calibrate_checkmarks()
        self.move_and_click(config["positions"]["search bar"]["center"], True)
        mkey.left_click()
        mkey.left_click()
        keyboard.Controller().type("godly")
        time.sleep(0.5)
        keyboard.Controller().press(keyboard.Key.enter)
        self.show_calibration_overlays()
        self.create_msg_box("Auto Calibration Complete", "Auto calibration is complete. Please verify the positions are correct.", internal=False)
        self.show_calibration_overlays()

    def find_add_buttons(self):
        self.focus_roblox()
        time.sleep(0.2)
        if not self.safe_image_find("amount box 1"):
            return
        self.move_and_click(config["positions"]["amount box 1"]["center"], False)
        pyautogui.scroll(2000)
        for add_button in data["position data"]["add button"]["sub positions"]:
            if not self.safe_image_find(add_button, multiple=True):
                return
        pyautogui.scroll(-2000)
        time.sleep(0.2)
        if not self.safe_image_find("add button 5", multiple=True, region=(0, config["positions"]["add button 4"]["bbox"][3], screen_width, config["positions"]["add button 5"]["bbox"][3] - config["positions"]["add button 4"]["bbox"][3])):
            return
        
    def find_amount_boxes(self):
        self.focus_roblox()
        time.sleep(0.2)
        if not self.safe_image_find("amount box 1"):
            return
        self.move_and_click(config["positions"]["amount box 1"]["center"], False)
        pyautogui.scroll(2000)
        for amount_box in config["positions"]["amount box"]["sub positions"][:4]:
            if not self.safe_image_find(amount_box, multiple=True):
                return
        pyautogui.scroll(-2000)
        time.sleep(0.2)
        if not self.safe_image_find("amount box 5", multiple=True):
            return
    
    def find_potion_selection_buttons(self):
        self.focus_roblox()
        time.sleep(0.2)
        for count in range(3):
            if not self.safe_image_find("potion selection button " + str(count + 1)):
                return
        
    def find_and_calibrate_checkmarks(self):
        self.focus_roblox()
        time.sleep(0.2)
        self.move_and_click(config["positions"]["amount box 1"]["center"], False)
        pyautogui.scroll(2000)
        mkey.left_click()
        mkey.left_click()
        if not self.safe_image_find("add completed checkmark 1"):
            return
        self.calibrate_checkmarks()

    def calibrate_checkmarks(self):
        checkmark_width_1 = config["positions"][f"add completed checkmark 1"]["bbox"][0]
        checkmark_width_2 = config["positions"][f"add completed checkmark 1"]["bbox"][2]
        checkmark_height_difference_top = config["positions"][f"add completed checkmark 1"]["bbox"][1] - config["positions"][f"amount box 1"]["bbox"][1]
        checkmark_height_difference_bottom = config["positions"][f"add completed checkmark 1"]["bbox"][3] - config["positions"][f"amount box 1"]["bbox"][3]

        for count in range(2, 6):
            amount_box_bbox = config["positions"][f"amount box {count}"]["bbox"]
            bbox = (checkmark_width_1, amount_box_bbox[1] + checkmark_height_difference_top, checkmark_width_2, amount_box_bbox[3] + checkmark_height_difference_bottom)
            config["positions"].setdefault(f"add completed checkmark {count}", {})["bbox"] = bbox
        nice_config_save()
        for count in range(5):
            self.create_overlay(bbox=config["positions"][f"add completed checkmark {count + 1}"]["bbox"])
        self.create_msg_box("Checkmark Calibration Complete", "checkmark calibration is complete. Please verify the positions are correct.", internal=False)
        self.create_overlay(disabled=True)

    def manual_scroll_calibration(self):
        def point_clicked(x, y, button, pressed):
            scroll_calibration_mouse_listener.stop()
            self.log(mkey.get_cursor_position())

        self.focus_roblox()
        scroll_calibration_mouse_listener = mouse.Listener(on_click=point_clicked)
        scroll_calibration_mouse_listener.start()
        scroll_calibration_mouse_listener.join()

    def manual_checkmarks_calibration(self):
        calibrated = self.manual_calibration("add completed checkmark 1", save=True, what_to_save=("bbox",))
        if calibrated is None:
            return
        self.calibrate_checkmarks()

    def focus_roblox(self):
        hwnd = win32gui.FindWindow(None, "Roblox")
        if not hwnd:
            self.log("Roblox window not found!")
            return False

        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        if win32gui.GetForegroundWindow() != hwnd:
            try:
                win32gui.BringWindowToTop(hwnd)
                win32gui.SetForegroundWindow(hwnd)
            except Exception:
                self.log("Failed to bring Roblox to the foreground. It may be minimized or not responding.")

        if win32gui.GetWindowPlacement(hwnd)[1] != win32con.SW_SHOWMAXIMIZED:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

        return True

    def close_roblox(self):
        hwnd = ctypes.windll.user32.FindWindowW(None, "Roblox")
        if hwnd:
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
            time.sleep(0.2)
            ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE

    def global_hotkey_listener(self):
        def on_press(key):
            if key == keyboard.Key.f1:
                self.start_macro_signal.emit()
            elif key == keyboard.Key.f2:
                self.stop_macro_signal.emit()
            elif key == keyboard.Key.f3:
                if not self.scroll_calibration_safety_check:
                    self.scroll_calibration_safety_check = True
            elif key == keyboard.Key.f7:
                os._exit(1)
            elif key == keyboard.Key.f4:
                self.log(mkey.get_cursor_position())
        main_hotkey_listener = keyboard.Listener(on_press=on_press)
        main_hotkey_listener.start()
        main_hotkey_listener.join()

    def setup_hotkeys(self):
        self.start_macro_signal.connect(self.start_macro)
        self.stop_macro_signal.connect(self.stop_macro)
        threading.Thread(target=self.global_hotkey_listener, daemon=True).start()

    def create_overlay(self, bbox=None, color=(0,255,0,255), text=None, text_color="#00FF00", font_size=10, thickness=3, disabled=False):
        overlay_windows = getattr(self, "active overlays", None)

        if overlay_windows is None:
            overlay_windows = {}
            setattr(self, "active overlays", overlay_windows)

        if disabled:
            for overlay_window in overlay_windows.values():
                overlay_window.close()
            overlay_windows.clear()
            return
        
        if bbox == None:
            return
        
        overlay_key = tuple(bbox)
        if overlay_key in overlay_windows:
            self.log("Overlay already exists for this region.")
            return

        x, y, x2, y2 = bbox
        w = x2 - x
        h = y2 - y

        # Scale coordinates for logical/physical match
        x_scaled = int(x / scale)
        y_scaled = int(y / scale)
        w_scaled = int(w / scale)
        h_scaled = int(h / scale)

        screen = QGuiApplication.screenAt(QPoint(x_scaled + w_scaled // 2, y_scaled + h_scaled // 2))
        if screen is None:
            QMessageBox.warning(self, "Screen Not Found", "Could not find a screen at the specified coordinates.")
            return

        screen_geo = screen.geometry()

        overlay_window = QWidget()
        overlay_window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool | Qt.WindowType.WindowTransparentForInput)
        overlay_window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        overlay_window.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        overlay_window.setGeometry(screen_geo)
        overlay_window.show()
        overlay_window.raise_()

        local_x = x_scaled - screen_geo.x()
        local_y = y_scaled - screen_geo.y()
        outline_frame = QFrame(overlay_window)
        outline_frame.setGeometry(QRect(local_x, local_y, w_scaled, h_scaled))

        if isinstance(color, tuple):
            outline_frame.setStyleSheet(f"background: transparent; border: {thickness}px solid rgba({color[0]},{color[1]},{color[2]},{color[3] if len(color) == 4 else 255});")
        elif isinstance(color, str):
            outline_frame.setStyleSheet(f"background: transparent; border: {thickness}px solid {color};")

        outline_frame.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        outline_frame.show()
        outline_frame.raise_()

        if text:
            label = QLabel(text, overlay_window)
            
            if isinstance(text_color, tuple):
                label.setStyleSheet(f"color: rgba({text_color[0]},{text_color[1]},{text_color[2]},{text_color[3] if len(text_color) == 4 else 255}); background: transparent; font-size: {font_size}pt;")
            elif isinstance(text_color, str):
                label.setStyleSheet(f"color: {text_color}; background: transparent; font-size: {font_size}pt;")

            label.adjustSize()
            label.move(local_x, local_y - label.height())
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            label.show()
            label.raise_()

        overlay_windows[overlay_key] = overlay_window

    def find_pixels_with_color(self, *targets, bbox=None):
        if bbox == None:
            img = ImageGrab.grab()
        else:
            img = ImageGrab.grab(bbox)

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

    def rescale_template(self, template, template_path):
        image_scale = data["template data"][template]["scale"]   
        image_resolution =data["template data"][template]["resolution"]
        scale_ratio = scale / image_scale
        image_ratio_x = screen_width / image_resolution[0]
        image_ratio_y = screen_height / image_resolution[1]
        total_image_scale_x = scale_ratio * image_ratio_x
        total_image_scale_y = scale_ratio * image_ratio_y
        self.log(f"Total Scale X: {total_image_scale_x}, Total Scale Y: {total_image_scale_y}")

        template_img = Image.open(template_path)
        template_scaled = template_img.resize((int(template_img.width * total_image_scale_x), int(template_img.height * total_image_scale_y)), Image.Resampling.LANCZOS)
        return template_scaled
    
    def auto_find_image(self, calibration,
                        what_to_save=("center", "bbox"),
                        multiple=False,
                        ignore_match_not_found=False,
                        region=None):
        
        template_path = f"{local_appdata_directory}\\Lib\\Images\\{data['position data'][calibration if calibration in data['position data'] else calibration[:-1].strip()]['image path']}"
        return_bool = False
        if what_to_save != None:
            tuple(what_to_save)

        if region == None and multiple and int(calibration[-1]) > 1:
            region = (0, config["positions"][calibration.replace(calibration[-1], str(int(calibration[-1]) - 1))]["bbox"][3], screen_width, screen_height)

        def save_position(position_name, center=None, bbox=None):
            self.log(f"Proposed position for '{position_name}': Center: {center}, bbox: {bbox}")
            if self.create_msg_box("Save Position", f"Save position for '{position_name}'?", "Yes", "No", internal=False) != "Yes":
                return False
            if "bbox" in what_to_save and bbox != None:
                config["positions"][position_name]["bbox"] = bbox
            if "center" in what_to_save and center != None:
                config["positions"][position_name]["center"] = center
            nice_config_save()
            return True
                
        def find_template():
            if not ignore_match_not_found:
                self.focus_roblox()
            time.sleep(0.2)
            bbox, center = None, None
            nonlocal return_bool
            return_bool = True
            try:
                match = pyautogui.locateOnScreen(template_scaled, confidence=config["data"]["position data"][calibration]["confidence"], region=region)
                bbox = (int(match.left), int(match.top), int(match.left + match.width), int(match.top + match.height))  # type: ignore[reportOptionalMemberAccess]
                center = (int(match.left + match.width // 2), int(match.top + match.height // 2))  # type: ignore[reportOptionalMemberAccess]
                self.log(f"  bbox : {bbox}, center: {center}")
                if what_to_save != None:
                    self.create_overlay(bbox, text=calibration)
                    return_bool = save_position(calibration, center, bbox)
                    self.create_overlay(bbox, text=calibration, disabled=True)
                if return_bool == False:
                    return
            except Exception as exception:
                self.create_overlay(disabled=True)

                if isinstance(exception, (pyautogui.ImageNotFoundException, pyscreeze_ImageNotFoundException))and ignore_match_not_found:
                    pass
                elif isinstance(exception, (pyautogui.ImageNotFoundException, pyscreeze_ImageNotFoundException)):
                    self.log(f"No matches found for template: {template_path}")
                    self.create_msg_box("No Matches Found", f"No Matches Found For: {calibration}", internal=False)
                else:
                    self.log(f"Error finding matches: {exception}")
                    self.create_msg_box("Error Finding Matches", f"Error Finding Matches: {exception}")
                return_bool = False

        template_scaled = self.rescale_template(data["position data"][calibration if calibration in data["position data"] else calibration[:-1].strip()]["image path"], template_path)
        find_template()
        return return_bool

    def calibrate_scrolling(self):
        template_path = self.rescale_template("add button.png", f"{local_appdata_directory}\\Lib\\Images\\add button.png")
        def count_scrolls(find=True):
            scrolls = 0
            found = False
            gone = False
            self.scroll_calibration_safety_check = False
            while True:
                if self.scroll_calibration_safety_check:
                    return False
                img =ImageGrab.grab(config["positions"]["add button 5"]["bbox"])
                if find:
                    try:
                        pyautogui.locate(template_path, img, confidence=config["data"]["position data"]["add button 5"]["scroll check confidence"])
                        self.log("'Add' detected saving scroll amount:", scrolls)
                        found = True
                    except pyautogui.ImageNotFoundException:
                        pass
                    except Exception as e:
                        self.log(e)

                    if found:
                        self.scroll_calibration_safety_check = True
                        return scrolls

                    pyautogui.scroll(-1)
                    scrolls += 1
                elif not find:
                    try:
                        pyautogui.locate(template_path, img, confidence=config["data"]["position data"]["add button 5"]["scroll check confidence"])
                    except pyautogui.ImageNotFoundException:
                        self.log("'Moved away from previous add button")
                        gone = True
                    except Exception as e:
                        self.log(e)

                    if gone:
                        self.scroll_calibration_safety_check = True
                        return True
                    pyautogui.scroll(-1)

        self.focus_roblox()
        self.mini_status_widget.show()
        self.update_status("Calibrating", what_to_update="General")
        self.update_status("Calibrating scrolling")
        QApplication.processEvents()
        self.move_and_click(config["positions"]["amount box 5"]["center"], False)
        pyautogui.scroll(2000)
        count1 = count_scrolls()
        if count1 == False:
            return False
        config["data"]["scroll amounts"]["to_5"] = count1
        nice_config_save()
        self.create_msg_box("Scroll Calibration", f"scrolls needed to reach 5th add button: {count1}", internal=False)
        if not count_scrolls(False):
            self.mini_status_widget.hide()
            QApplication.processEvents()
            return False
        self.focus_roblox()
        count2 = count_scrolls()
        if count2 == False:
            return False
        config["data"]["scroll amounts"]["past_5"] = count2
        nice_config_save()
        self.create_msg_box("Scroll Calibration", f"scrolls needed to reach past 5th add button: {count2}", internal=False)
        self.mini_status_widget.hide()
        QApplication.processEvents()
        return True
            
    def start_macro(self):
        if self.worker is not None and self.worker.is_alive():
            return
        self.mini_status_widget.show()
        self.update_status("Running", what_to_update="General")
        self.run_event.set()
        self.worker = threading.Thread(target=self.macro_worker, daemon=True)
        self.worker.start()

    def stop_macro(self):
        self.run_event.clear()

    def macro_worker(self):
        while self.run_event.is_set():
            self.main_macro_loop()
            if not self.run_event.wait(0.1):
                self.macro_stopped_signal.emit()
                break

    def log(self, *args):
        self.log_signal.emit(" ".join(str(a) for a in args))

    def inner_log(self, log_message):
        print(log_message)
        self.log_area.appendPlainText(log_message)
        log_scroll_bar = self.log_area.verticalScrollBar()
        if log_scroll_bar is not None:
            log_scroll_bar.setValue(log_scroll_bar.maximum())

    def update_status(self, *args, what_to_update="Task"):
        status_text = " ".join(str(a) for a in args)
        self.status_signal.emit(status_text, str(what_to_update))
        
    def inner_update_status(self, status_text, what_to_update="Task"):
        if what_to_update in ("General", "Both"):
            self.log("Status:", status_text)
            self.status_label.setText(f"Status: {status_text}")
            if self.general_mini_status_label != None:
                self.general_mini_status_label.setText(f"Status: {status_text}")
                self.general_mini_status_label.adjustSize()

        if what_to_update in ("Task", "Both"):
            self.log("Current Task:", status_text)
            if self.mini_status_label != None:
                self.mini_status_label.setText(f"Current Task: {status_text}")
                self.mini_status_label.adjustSize()

        self.mini_status_widget.adjustSize()

    def on_macro_stopped(self):
        self.update_status("Stopped", what_to_update="General")
        self.update_status("", what_to_update="Task")
        self.mini_status_widget.hide()
        
    def check_auto_add_button(self):
        bbox = config["positions"]["auto add button"]["bbox"]

        def get_green_amount(bbox):
            img = ImageGrab.grab(bbox).convert("RGB")
            if img is None:
                return False
            
            width, height = img.size
            pixels = img.load()

            score_sum = 0.0
            considered = 0
            for yy in range(0, height):
                for xx in range(0, width):
                    r, g, b = pixels[xx, yy] # type: ignore

                    max_rgb = max(r, g, b)
                    delta = g - max(r, b)
                    if delta > 0 and max_rgb > 0:
                        score_sum += (delta / max_rgb)
                    considered += 1

            confidence = (score_sum / considered)
            return confidence
        
        self.move_and_click(config["positions"]["auto add button"]["center"], click=False)
        time.sleep(0.1)
        first = get_green_amount(bbox)
        time.sleep(0.1)
        self.move_and_click(config["positions"]["auto add button"]["center"])
        time.sleep(0.1)
        second = get_green_amount(bbox)
        
        if first > second:
            more_green = "FIRST"
            time.sleep(0.1)
            mkey.left_click()
            self.log("double clicked auto add button as it was already active")
        elif second > first:
            more_green = "SECOND"
            self.log("clicked auto add button")
        elif first == second:
            more_green = "TIE"
        else:
            raise Exception("Unexpected case in auto add button check")
        self.log(f"first_conf={(first*100):.0f} second_conf={(second*100):.0f} more_green={more_green}")
        
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

    def search_for_potion(self, potion):
        self.move_and_click(config["positions"]["potion search bar"]["center"])
        mkey.left_click()
        mkey.left_click()
        self.log("Search bar clicked")
        keyboard.Controller().type(data["item data"][potion]["name to search"])
        self.log("Item searched:", data["item data"][potion]["name to search"].capitalize())
        time.sleep(0.5)
        keyboard.Controller().press(keyboard.Key.enter)
        potion_selection_button = ("potion selection button " + data["item data"][potion].get("potion selection button", "1"))
        self.log(potion_selection_button)
        self.move_and_click(config["positions"][potion_selection_button]["center"])
        self.move_and_click(config["positions"]["open recipe button"]["center"])
        self.log("Clicked to open recipe button")

    def main_macro_loop(self, slowdown=0.01, slowdown2=0.1):
        def add_to_button(button_to_add_to):
            self.log("Adding to:", button_to_add_to)
            if int(button_to_add_to[-1]) < 5:
                self.move_and_click(config["positions"][f"amount box {int(button_to_add_to[-1])}"]["center"], False)
                self.log("Moved to", "amount box", button_to_add_to[-1])
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown)
                mkey.left_click()
                mkey.left_click()
                self.log("Amount box clicked to focus")
                if button_to_add_to in data["item data"][item]["amounts to add"]:
                    keyboard.Controller().type(str(data["item data"][item]["amounts to add"][button_to_add_to]))
                    self.log(f"Typed amount: {data['item data'][item]['amounts to add'][button_to_add_to]}")
                else:
                    keyboard.Controller().type("1")
                    self.log("Typed amount: 1")
                time.sleep(slowdown)
                self.move_and_click(config["positions"][button_to_add_to]["center"])
                self.log(f"{button_to_add_to} clicked")
            elif int(button_to_add_to[-1]) >= 5:
                self.move_and_click(config["positions"]["amount box 5"]["center"], False)
                self.log("Moved to amount box 5 center")
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                pyautogui.scroll(-config["data"]["scroll amounts"]["to_5"])
                self.log("Scrolled down to slot 5")
                time.sleep(slowdown)
                for x in range(4, int(button_to_add_to[-1])):
                    pyautogui.scroll(-config["data"]["scroll amounts"]["past_5"])
                    self.log("Scrolled down to slot", x + 1)
                mkey.left_click()
                mkey.left_click()
                self.log("Amount box clicked to focus")
                if button_to_add_to in data["item data"][item]["amounts to add"]:
                    keyboard.Controller().type(str(data["item data"][item]["amounts to add"][button_to_add_to]))
                    self.log(f"Typed amount: {data['item data'][item]['amounts to add'][button_to_add_to]}")
                else:
                    keyboard.Controller().type("1")
                    self.log("Typed amount: 1")
                self.move_and_click(config["positions"]["add button 5"]["center"])
                self.log(f"{button_to_add_to} clicked")

        def check_button(button_to_check):
            time.sleep(slowdown)
            if int(button_to_check[-1]) < 5:
                self.move_and_click(config["positions"][f"amount box {int(button_to_check[-1])}"]["center"], False)
                self.log(f"Moved to amount box {int(button_to_check[-1])}")
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                time.sleep(slowdown2)
                time.sleep(slowdown2)
                bbox = config["positions"][f"add completed checkmark {button_to_check[-1]}"]["bbox"]
            else:
                self.move_and_click(config["positions"]["amount box 5"]["center"], False)
                self.log("Moved to amount box 5")
                pyautogui.scroll(2000)
                self.log("Scrolled up")
                pyautogui.scroll(-config["data"]["scroll amounts"]["to_5"])
                self.log("Scrolled down to slot 4")
                for x in range(4, int(button_to_check[-1])):
                    pyautogui.scroll(-config["data"]["scroll amounts"]["past_5"])
                    self.log("Scrolled down to slot", x + 1)
                time.sleep(slowdown2)
                time.sleep(slowdown2)
                bbox = config["positions"][f"add completed checkmark 5"]["bbox"]
            pixel_matches =self.find_pixels_with_color("#42FF6E", "#41FA6C", "#3FF369", "#3EEE67", "#41FC6D", "#40F169", bbox=bbox)
            self.log(data["item data"][item]["button names"][button_to_check], "pixel matches:", pixel_matches)
            if pixel_matches > 0:
                self.log(f"{data['item data'][item]['button names'][button_to_check]} is ready")
                return True
            else:
                self.log(f"{data['item data'][item]['button names'][button_to_check]} is not ready")
                return False
            
        def add_additional_buttons_for_item(item):
            self.log(f"Clicking additional buttons for {item}")
            for button_to_click in config["item presets"][self.current_preset][item]["additional buttons to click"]:
                add_to_button(button_to_click)
                if not check_button(button_to_click):
                    self.log(f"Additional button {button_to_click} for {item} failed.")
                    return False
                else:
                    self.log(f"Additional button {button_to_click} for {item} succeeded.")
            return True

        def add_next_item_to_auto_add():
            if len(self.auto_add_waitlist) > 0:
                self.update_status("Setting Auto Add for:", self.auto_add_waitlist[0].capitalize())
                self.search_for_potion(self.auto_add_waitlist[0])
                time.sleep(slowdown2)
                self.check_auto_add_button()
                time.sleep(slowdown)
                self.current_auto_add_potion = self.auto_add_waitlist.pop(0)

        def macro_loop_iteration(item):
            self.focus_roblox()
            if item not in self.auto_add_waitlist and self.current_auto_add_potion != item:
                self.move_and_click(config["positions"]["potion menu item button"]["center"])
                self.update_status("Searching for:", item.capitalize())
                self.search_for_potion(item)
                self.update_status("Adding to buttons for:", item.capitalize())
                for button_to_add_to in config["item presets"][self.current_preset][item]["buttons to check"]:
                    add_to_button(button_to_add_to)
                    time.sleep(slowdown)

                self.log(f"{item} set to ready")
                time.sleep(slowdown2)
                self.update_status("Checking Buttons for:", item.capitalize())
                for button_to_check in config["item presets"][self.current_preset][item]["buttons to check"]:
                    if not check_button(button_to_check):
                        return  
                    
                self.update_status("Adding Additional Buttons for", item.capitalize())
                if add_additional_buttons_for_item(item):
                    if not config["item presets"][self.current_preset][item]["instant craft"]:
                        self.update_status("Setting Auto Add for:", item.capitalize())
                        if self.current_auto_add_potion == None:
                            self.check_auto_add_button()
                            self.current_auto_add_potion = item
                        elif not self.current_auto_add_potion == None and item not in self.auto_add_waitlist:
                            self.auto_add_waitlist.append(item)
                            self.log(f"{item.capitalize()} added to auto add waitlist")
                    else:
                        self.update_status("Crafting:", item.capitalize())
                        self.move_and_click(config["positions"]["craft button"])
                        self.log("Clicked craft button")

            elif item == self.current_auto_add_potion:
                self.move_and_click(config["positions"]["potion menu item button"]["center"])
                self.update_status("Searching for:", item.capitalize())
                self.search_for_potion(item)
                self.log(f"{item.capitalize()} set to ready")
                self.update_status("Checking All Buttons")

                for slot in config["item presets"][self.current_preset][item]["buttons to check"]:
                    add_to_button(slot)
                    if not check_button(slot):
                        self.log(f"{item.capitalize()} false positive detected on completed check button: {data['item data'][item]['button names'][slot]}, skipping craft and moving to next auto add item")
                        self.current_auto_add_potion = None
                        add_next_item_to_auto_add()
                        return
                
                for slot in config["item presets"][self.current_preset][item]["additional buttons to click"]:
                    add_to_button(slot)
                    if not check_button(slot):
                        self.log(f"{item.capitalize()} false positive detected on additional button to click: {data['item data'][item]['button names'][slot]}, skipping craft and moving to next auto add item")
                        self.current_auto_add_potion = None
                        add_next_item_to_auto_add()
                        return
                    
                for slot in range(1, data['item data'][item]['crafting slots'] + 1):
                    slot = "add button " + str(slot)
                    if slot not in (config["item presets"][self.current_preset][item]["buttons to check"] or config["item presets"][self.current_preset][item]["additional buttons to click"]):
                        add_to_button(slot)
                        if not check_button(slot):
                            return

                self.update_status("Crafting:", item.capitalize())
                self.move_and_click(config["positions"]["craft button"]["center"])
                self.log("Clicked craft button")
                time.sleep(slowdown)
                add_next_item_to_auto_add()
                           
        for item in data["item data"].keys():
                if config["item presets"][self.current_preset][item]["enabled"]:
                    macro_loop_iteration(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if skip_loading:
        main_window = Dark_Sol()
        main_window.show()
    else:
        loader = loading_screen()
        loader.show()
    sys.exit(app.exec())