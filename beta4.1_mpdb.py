from wget import download
import sys
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QApplication, QMainWindow, QDesktopWidget, \
    QComboBox
from PyQt5.QtGui import QPixmap, QImage, QCursor
import webbrowser
from PyQt5 import QtCore
from requests import get
from minecraft_launcher_lib import command, forge
import subprocess
from os import rename, path, remove, listdir
from pathlib import Path
from psutil import virtual_memory
from json import loads, dump
import time
from zipfile import ZipFile
from shutil import move, rmtree
from datetime import datetime


class MPDB(QMainWindow):
    try:
        # def __init__(self):
        #     super().__init__()
        #     self.initUI()


        def start_worker(self):
            self.thread = ThreadClass(parent=None, version=self.list_widget.currentText(),
                                      username=self.username_selector.text(), ram=str(self.selected_ram))
            self.thread.start()
            self.thread.any_signal.connect(self.run_1165)
            self.run_minecraft.setEnabled(False)
            self.list_widget.setEnabled(False)
            self.ram_selector.setEnabled(False)
            self.username_selector.setEnabled(False)
            for i in self.buttons:
                w = self.findChild(QPushButton, i)
                w.setEnabled(False)
            self.run_minecraft_info.setText("Running")

        def start_download_worker(self):
            self.thread = DownloadThread(parent=None, mp_name=self.sender().objectName(), download_list=self.downloaded)
            self.thread.start()
            for i in self.buttons:
                w = self.findChild(QPushButton, i)
                w.setEnabled(False)
            self.run_minecraft.setEnabled(False)
            self.thread.any_signal.connect(self.down)
            self.downloading = self.sender().objectName()

        def stop_worker(self):
            self.thread.stop()
            self.run_minecraft.setEnabled(True)
            self.list_widget.setEnabled(True)
            self.ram_selector.setEnabled(True)
            self.username_selector.setEnabled(True)
            self.run_minecraft_info.setText("")
            for i in self.buttons:
                w = self.findChild(QPushButton, i)
                w.setEnabled(True)

        def stop_download_worker(self):
            self.thread.stop()
            for i in self.buttons:
                w = self.findChild(QPushButton, i)
                w.setEnabled(True)
            self.run_minecraft.setEnabled(True)
            self.list_widget.addItem(self.downloaded["downloaded"][-1])
            self.list_widget.adjustSize()
            b = self.findChild(QPushButton, self.downloading)
            b.hide()

        def initUI(self):
            start = time.perf_counter()
            self.downloaded = {}
            self.downloaded["downloaded"] = []
            if not path.exists("data.txt"):
                dosya = open("data.txt", "w", encoding="utf-8")
                dump(self.downloaded, dosya, ensure_ascii=False, indent=4, sort_keys=True)
                dosya.close()
            else:
                dosya = open("data.txt", "r", encoding="utf-8")
                self.downloaded = loads(str(dosya.read()))
                if len(self.downloaded["downloaded"]) != 0:
                    self.run_minecraft.setEnabled(True)
                dosya.close()

            max_ram = virtual_memory().total
            max_ram //= 1024
            max_ram //= 1024
            max_ram //= 1024

            self.rams = []
            for i in range(1, max_ram):
                self.rams.append(str(i) + " GB")

            self.r = get("https://mpdb.xyz/get_data.php")
            self.r = self.r.text
            self.r = loads(self.r)

            self.resize(1000, 600)
            self.setWindowTitle("TheModpackDatabase")

            self.setStyleSheet("background:rgba(54,57,63,255)")
            self.setMinimumSize(839, 438)
            self.setMouseTracking(True)
            self.center()

            self.list_widget = QComboBox(self)
            self.list_widget.addItems(self.downloaded["downloaded"])
            self.list_widget.move(0, 70)
            self.list_widget.currentTextChanged.connect(self.change_label)
            self.version = self.list_widget.currentText()
            self.list_widget.setStyleSheet("background:rgba(185,187,190,255)")
            self.list_widget.resize(len(self.list_widget.currentText()) * 11, self.list_widget.height())
            self.list_widget.adjustSize()

            self.ram_selector = QComboBox(self)
            self.ram_selector.addItems(self.rams)
            self.ram_selector.move(0, 100)
            self.ram_selector.currentTextChanged.connect(self.change_ram)
            self.ram_selector.setStyleSheet("background:rgba(185,187,190,255)")

            self.selected_ram = self.ram_selector.currentText().replace(" GB", "")

            self.username_selector = QLineEdit(self)
            self.username_selector.move(900, 0)
            self.username_selector.setPlaceholderText("Username")
            self.username_selector.setStyleSheet("background:rgba(185,187,190,255)")

            # Discord Image
            self.image = QImage()
            self.image.loadFromData(get("https://mpdb.xyz/discord.png").content)
            self.image_label = QLabel(self)
            self.pixmap = QPixmap(self.image)
            self.pixmap = self.pixmap.scaled(64, 64)
            self.image_label.setPixmap(self.pixmap)
            self.image_label.resize(64, 64)
            self.image_label.setMouseTracking(True)

            # Run Minecraft Button Beta
            self.run_minecraft = QPushButton(f"Run {self.list_widget.currentText()}", self)
            self.run_minecraft.clicked.connect(self.start_worker)
            self.run_minecraft.setStyleSheet("background:rgba(185,187,190,255)")
            self.run_minecraft.setEnabled(False)

            self.run_minecraft_info = QLabel(self)
            self.run_minecraft_info.setAlignment(QtCore.Qt.AlignRight)

            pos = 130
            self.buttons = []
            for i in self.r:
                self.buttons.append(str(i))
            for i in self.buttons:
                self.mp_name = QLabel(i, self)
                self.mp_name.move(0, pos)
                self.mp_name.resize(len(self.mp_name.text()) * 8, self.mp_name.height())
                pos += 30
            self.link = QLabel("<a href='https://mpdb.xyz'>https://mpdb.xyz</a>", self)
            self.link.move(0, pos + 30)
            self.link.resize(len(self.link.text()) * 8, self.link.height())
            self.link.setOpenExternalLinks(True)

            pos = 130
            for i in self.buttons:
                self.down_button = QPushButton("Download", self)
                self.down_button.setObjectName(i)
                self.down_button.move(len(max(self.buttons, key=len)) * 8, pos)
                self.down_button.setStyleSheet("background:rgba(185,187,190,255)")
                self.down_button.clicked.connect(self.start_download_worker)
                pos += 30

            for i in self.downloaded["downloaded"]:
                pbutton = self.findChild(QPushButton, i)
                if pbutton != None:
                    pbutton.hide()
                elif pbutton == None:
                    self.downloaded["downloaded"].remove(i)
            start = time.perf_counter() - start
            print(start)

        def down(self):
            self.stop_download_worker()

        # Responsive Event
        def resizeEvent(self, event):
            width = self.width() - self.run_minecraft.width()
            self.run_minecraft.move(width, 0)
            self.run_minecraft_info.move(self.width() - 110, self.run_minecraft.height())
            self.username_selector.move(self.width() - 200,
                                        self.run_minecraft.height() - self.run_minecraft_info.height())

        # Mouse click
        def mousePressEvent(self, event):
            if event.buttons() == QtCore.Qt.LeftButton:
                if 0 <= event.x() <= 64 and 0 <= event.y() <= 64:
                    self.discord()

        def mouseMoveEvent(self, event):
            if event.x() <= 64 and event.y() <= 64:
                self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            else:
                self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

        # Open discord link
        def discord(self):
            webbrowser.open("https://discord.gg/frWGTqhFbn", new=0, autoraise=True)

        def change_ram(self):
            self.selected_ram = int(self.ram_selector.currentText().replace(" GB", ""))

        # Run Minecraft
        def run_1165(self):
            self.stop_worker()

        def center(self):
            # geometry of the main window
            qr = self.frameGeometry()

            # center point of screen
            cp = QDesktopWidget().availableGeometry().center()

            # move rectangle's center point to screen's center point
            qr.moveCenter(cp)

            # top left of rectangle becomes top left of window centering it
            self.move(qr.topLeft())

        def change_label(self, value):
            self.run_minecraft.setText(f"Run {value}")
            self.version = value
            self.list_widget.adjustSize()




    except Exception as e:
        now = datetime.now()
        date_time = now.strftime("%Y_%m_%d-%H_%M_%S")
        log = open(f"{date_time}.txt", "a")
        log.write(f"{e}\n")
        log.close()


class ThreadClass(QtCore.QThread):
    try:
        any_signal = QtCore.pyqtSignal()

        def __init__(self, version="", username="", ram="", parent=None):
            super(ThreadClass, self).__init__(parent)
            self.is_running = True
            self.version = version
            self.username = username
            self.ram = ram

        def printProgressBar(self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
            percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
            filledLength = int(length * iteration // total)
            bar = fill * filledLength + '-' * (length - filledLength)

            print(percent, end="\n")
            if iteration == total:
                print()

        def maximum(self, max_value, value):
            max_value[0] = value

        def run(self):
            print("Starting...")
            r = get("https://mpdb.xyz/get_data.php?from=name&data=true&name=" + self.version).text
            r = loads(r)
            if self.username == "": self.username = "MPDB"
            if " " in self.username: self.username = self.username.replace(" ", "_")
            print("Get Username OK!")
            print(self.username)
            max_value = [0]
            print("Progress Bar OK!")
            callback = {
                "setProgress": lambda value: self.printProgressBar(value, max_value[0]),
                "setMax": lambda value: self.maximum(max_value, value)
            }
            print(r)
            print(forge.find_forge_version(r["version"]))
            forge.install_forge_version(forge.find_forge_version(r["version"]), r["name"], callback=callback)
            print("Install Version OK!")
            options = {
                "username": self.username,
                "jvmArguments": [f"-Xmx{self.ram}G"]}
            version = forge.find_forge_version(r["version"]).split("-")
            version = version[0] + "-forge-" + version[1]
            print(version)
            subprocess.call(command.get_minecraft_command(version, r["name"], options))
            print("Run Minecraft OK!")
            self.any_signal.emit()

        def stop(self):
            self.is_running = False
            print("Stopping...")
            self.wait()
    except Exception as e:
        now = datetime.now()
        date_time = now.strftime("%Y_%m_%d-%H_%M_%S")
        log = open(f"{date_time}.txt", "a")
        log.write(f"{e}\n")
        log.close()

class DownloadThread(QtCore.QThread):
    try:
        any_signal = QtCore.pyqtSignal()

        def __init__(self, parent, mp_name, download_list):
            super(DownloadThread, self).__init__(parent)
            self.mp_name = mp_name
            self.downloaded = download_list
            self.mainwindow = MPDB()

        def run(self):
            print("Downloading")
            r = get("https://mpdb.xyz/get_data.php?from=name&data=true&name=" + self.mp_name)
            r = r.text
            r = loads(r)
            self.author = r["author"]
            self.name = r["name"]
            self.version = r["version"]

            Path(self.name).mkdir(parents=True, exist_ok=True)
            print(f"Downloading {self.name} by  {self.author}")
            download("https://mpdb.xyz/modpacks/" + self.author + "_" + self.name + ".zip")


            rename(self.author + "_" + self.name + ".zip", self.name + "/" + self.author + "_" + self.name + ".zip")
            zip_path = self.name + "/" + self.author + "_" + self.name + ".zip"
            if self.name not in self.downloaded["downloaded"]:
                self.downloaded["downloaded"].append(self.name)
                dosya = open("data.txt", "w", encoding="utf-8")
                dump(self.downloaded, dosya, ensure_ascii=False, indent=4, sort_keys=True)
                dosya.close()
            print(self.downloaded)
            zip = ZipFile(zip_path, "r")
            all_files = zip.namelist()
            if "modlist.html" in all_files:
                for i in all_files:
                    if "overrides" in i:
                        zip.extract(i, f"{self.name}")
                for i in listdir(f"{self.name}/overrides"):
                    move(f"{self.name}/overrides/{i}", f"{self.name}")
                manifest = zip.read("manifest.json")
                manifest = loads(manifest)
                Path(f"{self.name}/mods").mkdir(parents=True, exist_ok=True)
                for id in manifest["files"]:
                    pid = id["projectID"]
                    fid = id["fileID"]
                    r = loads(get(f"https://cursemeta.dries007.net/{pid}/{fid}.json").text)
                    print(f"Downloading {r['FileNameOnDisk']}")
                    download(r["DownloadURL"], out=f"{self.name}/mods")

                rmtree(f"{self.name}/overrides")
                zip.close()
                remove(f"{self.name}/{self.author}_{self.name}.zip")



            else:
                zip.extractall(f"{self.name}")
                zip.close()
                remove(f"{self.name}/{self.author}_{self.name}.zip")


            zip.close()
            self.any_signal.emit()

        def stop(self):
            print("Stopping")
            self.wait()
    except Exception as e:
        now = datetime.now()
        date_time = now.strftime("%Y_%m_%d-%H_%M_%S")
        log = open(f"{date_time}.txt", "a")
        log.write(f"{e}\n")
        log.close()

try:

    def main():
        app = QApplication(sys.argv)
        mpdb = MPDB()
        mpdb.initUI()
        mpdb.show()
        sys.exit(app.exec_())


    if __name__ == "__main__":
        main()
except Exception as e:
    now = datetime.now()
    date_time = now.strftime("%Y_%m_%d-%H_%M_%S")
    log = open(f"{date_time}.txt", "a")
    log.write(f"{e}\n")
    log.close()
