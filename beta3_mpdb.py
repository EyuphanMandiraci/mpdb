from wget import download
from sys import exit, argv
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QApplication, QGridLayout, QMainWindow, QDesktopWidget, QComboBox, QProgressBar
from PyQt5.QtGui import QIcon, QPixmap, QImage,QCursor
import webbrowser
from PyQt5 import QtCore
from requests import get
import minecraft_launcher_lib as mll
import subprocess
from os import mkdir,remove
import time
from plyer import notification
from pathlib import Path

class MPDB(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def start_worker(self):
        self.thread = ThreadClass(parent=None,version=self.list_widget.currentText(),username=self.username_selector.text(),progress=self.progress,progress_info=self.progress_info)  
        self.thread.start()
        self.thread.any_signal.connect(self.run_1165)
        self.run_minecraft.setEnabled(False)
        self.run_minecraft_info.setText("Running")
        
        
        
    def stop_worker(self):
        self.thread.stop()
        self.run_minecraft.setEnabled(True) 
        self.run_minecraft_info.setText("")
        self.progress.hide()
        self.progress_info.setText("")       
    
    def initUI(self):
        self.minecraft_versions = []
        self.mc_vers = mll.utils.get_version_list()
        for i in self.mc_vers:
            if i["type"] == "release":
                self.minecraft_versions.append(i["id"])
        
        self.resize(1000,600)
        self.setWindowTitle("TheModpackDatabase")
        
        self.setStyleSheet("background:rgba(54,57,63,255)")
        self.setMinimumSize(839,438)
        self.setMouseTracking(True)
        self.center()
        
        self.list_widget = QComboBox(self)
        self.list_widget.addItems(self.minecraft_versions)
        self.list_widget.move(0,70)
        self.list_widget.currentTextChanged.connect(self.change_label)
        self.version = self.list_widget.currentText()
        self.list_widget.setStyleSheet("background:rgba(185,187,190,255)")
        
        self.username_selector = QLineEdit(self)
        self.username_selector.move(900,0)
        self.username_selector.setPlaceholderText("Username")
        self.username_selector.setStyleSheet("background:rgba(185,187,190,255)")
        
        
        self.progress = QProgressBar(self)
        self.progress.move(150,150)
        self.progress.resize(400,25)
        self.progress.hide()
        
        #Discord Image
        self.image = QImage()
        self.image.loadFromData(get("https://mpdb.xyz/discord.png").content)
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(64,64)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(64,64)
        self.image_label.setMouseTracking(True)
        
        #Run Minecraft Button Beta
        self.run_minecraft = QPushButton(f"Run {self.list_widget.currentText()}",self)
        self.run_minecraft.clicked.connect(self.start_worker)
        self.run_minecraft.setStyleSheet("background:rgba(185,187,190,255)")
        
        self.run_minecraft_info = QLabel(self)
        self.run_minecraft_info.setAlignment(QtCore.Qt.AlignRight)
        
        self.progress_info = QLabel(self)
        self.progress_info.resize(400,30)
        
        #Download Button Beta
        self.download_button = QPushButton("Download",self)
        self.download_button.setStyleSheet("background:rgba(185,187,190,255)")
        
        self.theme_selector = QPushButton("White Theme",self)
        self.theme_selector.clicked.connect(self.theme_changer)
        self.theme_selector.setStyleSheet("background:rgba(185,187,190,255)")
        
        
    #Responsive Event
    def resizeEvent(self,event):
        width = self.width() - self.download_button.width()
        height = self.height() - self.download_button.height()
        width = width//2
        height = height//2
        self.download_button.move(width,height)
        width = self.width() - self.run_minecraft.width()
        self.run_minecraft.move(width,0)
        self.run_minecraft_info.move(self.width() - 110, self.run_minecraft.height())
        self.username_selector.move(self.width() - 200, self.run_minecraft.height() - self.run_minecraft_info.height())
        self.theme_selector.move(self.width() - 100,self.height() - 30)
        self.progress_info.move(self.progress.x(),self.progress.y() + self.progress.height())
    
    #Mouse click    
    def mousePressEvent(self,event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if 0 <= event.x() <= 64 and 0 <= event.y() <= 64:
                self.discord()
                
    def mouseMoveEvent(self,event):
        if event.x() <= 64 and event.y() <= 64:
            self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.setCursor(QCursor(QtCore.Qt.ArrowCursor))
    
    #Open discord link 
    def discord(self):
        webbrowser.open("https://discord.gg/frWGTqhFbn",new=0,autoraise=True)
        
    def theme_changer(self):
        get_text = self.theme_selector.text()
        if get_text == "White Theme":
            self.theme_selector.setText("Dark Theme")
            self.setStyleSheet("background:white")
            self.theme_selector.setStyleSheet("background:rgba(54,57,63,255)")
            self.download_button.setStyleSheet("background:rgba(54,57,63,255)")
            self.run_minecraft.setStyleSheet("background:rgba(54,57,63,255)")
            self.list_widget.setStyleSheet("background:rgba(54,57,63,255)")
            self.username_selector.setStyleSheet("background:rgba(54,57,63,255)")
            
            
        else:
            self.theme_selector.setText("White Theme")
            self.setStyleSheet("background:rgba(54,57,63,255)")
            self.theme_selector.setStyleSheet("background:rgba(185,187,190,255)")
            self.download_button.setStyleSheet("background:rgba(185,187,190,255)")
            self.run_minecraft.setStyleSheet("background:rgba(185,187,190,255)")
            self.list_widget.setStyleSheet("background:rgba(185,187,190,255)")
            self.username_selector.setStyleSheet("background:rgba(185,187,190,255)")
            
        
        
    #Run Minecraft
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
        
        
    def change_label(self,value):
        self.run_minecraft.setText(f"Run {value}")
        self.version = value
        
        
            
class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()
    def __init__(self,version,username,progress,progress_info,parent=None):
        super(ThreadClass,self).__init__(parent)
        self.is_running = True
        self.version = version
        self.username = username
        self.progress = progress
        self.progress_info = progress_info
        
    def printProgressBar(self,iteration,total,prefix='',suffix='',decimals=1, length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        
        self.progress.setValue(int(float(percent)))
        if iteration == total:
            print()
            
    def maximum(self,max_value,value):
        max_value[0] = value    
    
    def run(self):
        print("Starting...")
        Path("mpdb").mkdir(parents=True,exist_ok=True)
        if self.username == "": self.username = "MPDB"
        print(self.username)
        max_value = [0]
        self.progress.show()
        callback = {
            "setStatus": lambda text: self.progress_info.setText(text),
            "setProgress": lambda value: self.printProgressBar(value, max_value[0]),
            "setMax": lambda value: self.maximum(max_value, value)
        }
        notification.notify(title="MPDB",message="Minecraft Installing")
        mll.install.install_minecraft_version(self.version,"mpdb",callback=callback)
        options = {"username":self.username}
        notification.notify(title="MPDB",message="Minecraft Running")
        subprocess.call(mll.command.get_minecraft_command(self.version,"mpdb",options))
        self.any_signal.emit()
        
    def stop(self):
        self.is_running = False
        print("Stopping...")
        self.wait()
        
        
        
def main():
    app = QApplication(argv)
    mpdb = MPDB()
    mpdb.show()
    exit(app.exec_())
    
if __name__ == "__main__":
    main()
