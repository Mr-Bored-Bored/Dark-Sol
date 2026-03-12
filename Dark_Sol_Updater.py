# Logging
from asyncio import subprocess
import logging, pathlib, os, json
from logging.handlers import RotatingFileHandler
local_appdata_directory = pathlib.Path(os.environ["LOCALAPPDATA"]) / "Dark Sol"

logger = logging.getLogger("DarkSol")
logger.setLevel(logging.DEBUG)
logger.propagate = False
file_handler = RotatingFileHandler(local_appdata_directory / "Dark Sol Updater Log.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
logging_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
logging_formatter.default_msec_format = "%s.%03d"
file_handler.setFormatter(logging_formatter)
logger.addHandler(file_handler)

class log():
    @staticmethod
    def debug(*args):
        logger.debug(" ".join(str(a) for a in args))
        print(" ".join(str(a) for a in args))
    @staticmethod
    def info(*args):
        logger.info(" ".join(str(a) for a in args))
        print(" ".join(str(a) for a in args))
    @staticmethod
    def warning(*args):
        logger.warning(" ".join(str(a) for a in args))
        print(" ".join(str(a) for a in args))
    @staticmethod
    def error(*args):
        logger.error(" ".join(str(a) for a in args))
        print(" ".join(str(a) for a in args))
    @staticmethod
    def exception(*args):
        logger.exception(" ".join(str(a) for a in args))
        print(" ".join(str(a) for a in args))

log.info("Starting Dark Sol Updater")
log.debug("Logging Initalized")

import requests, socket, subprocess, shutil

def get_update_signal():
    global path, parent_path, version_to_download
    continue_update = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5296))
        with client:
            signal = json.loads(b"".join(iter(lambda: client.recv(4096), b"")).decode("utf-8"))
            signal_message = signal["command"]
            version_to_download = signal["version"]
            path = pathlib.Path(signal["path"])
            parent_path = path.parent
            log.debug(f"Received: {signal_message}, Version: {version_to_download}, Path: {path}")
            if signal_message == "Update Dark Sol":
                client.send(b"Dark Sol Update Signal Received")
                continue_update = True
    if continue_update:
        shutil.move(path, local_appdata_directory)
        update_macro(version_to_download)

def update_macro(version):
    log.info("Starting auto update...")
    try:
        log.info(f"Downloading Dark Sol from repo...")
        github_file = requests.get(f"https://github.com/Mr-Bored-Bored/Dark-Sol/releases/download/v{version}/Dark_Sol.exe", timeout=20)
        log.info(f"Finished downloading Dark Sol from repo")
        file_content = github_file.content
        if github_file.status_code != 200:
            raise Exception(f"Failed to download Dark Sol from repo, status code: {github_file.status_code}")
        parent_path.mkdir(parents=True, exist_ok=True)
        log.debug("Created output directory if it did not exist")
        log.info(f"Saving Dark Sol to {parent_path}...")
        with open(path, "wb") as f:
            f.write(file_content)
        log.info(f"Finished saving Dark Sol to {path}")

        pathlib.Path(local_appdata_directory / "Dark_Sol.exe").unlink(missing_ok=True)
        log.info("Finished auto update, exiting updater...")
        subprocess.Popen([str(path), "--updated"])
    except Exception as e:
        log.error("Failed to auto update:", e)
        shutil.move(local_appdata_directory / "Dark_Sol.exe", parent_path)
        subprocess.Popen([str(path), "--update_failed"])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind(("localhost", 5295))
            server.listen(1)
            conn, addr = server.accept()
            log.debug(f"Connected by {addr}")
            with conn:
                conn.send(str(e).encode())

if __name__ == "__main__":
    get_update_signal()