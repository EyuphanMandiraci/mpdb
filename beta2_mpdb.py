from wget import download
from sys import exit, argv
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QApplication, QGridLayout, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage, QCursor
import webbrowser
from PyQt5 import QtCore
from requests import get
import minecraft_launcher_lib as mll
import subprocess
from os import mkdir, walk, getcwd
import time

class MPDB(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        
        
        
        
    def start_worker(self):
        self.thread = ThreadClass(parent=None,)  
        self.thread.start()
        self.thread.any_signal.connect(self.run_1165)
        self.run_minecraft.setEnabled(False)
        self.run_minecraft_info.setText("Running")
        
    def stop_worker(self):
        self.thread.stop()
        self.run_minecraft.setEnabled(True) 
        self.run_minecraft_info.setText("")       
    
    def initUI(self):
        self.resize(1000,600)
        self.setWindowTitle("TheModpackDatabase")
        #self.graphicsView.setMouseTracking(True)
        
        #Discord Image
        self.image = QImage()
        self.image.loadFromData(get("https://mpdb.xyz/discord.png").content)
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(self.image)
        self.pixmap = self.pixmap.scaled(64,64)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.resize(64,64)
        self.image_label.cursor()
        
        #Run Minecraft Button Beta
        self.run_minecraft = QPushButton("Run 1.16.5",self)
        self.run_minecraft.clicked.connect(self.start_worker)
        
        self.run_minecraft_info = QLabel(self)
        self.run_minecraft_info.setAlignment(QtCore.Qt.AlignRight)
        
        #Download Button Beta
        self.download_button = QPushButton("Download",self)
        self.download_button.move(460,300)
        
        
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
    
    #Mouse click    
    def mousePressEvent(self,event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if 0 <= event.x() <= 64 and 0 <= event.y() <= 64:
                self.discord()
                
    
    #Open discord link 
    def discord(self):
        webbrowser.open("https://discord.gg/w65YFgR6kV",new=0,autoraise=True)
        
        
    #Run Minecraft
    def run_1165(self):
        self.stop_worker()
        
        
            
class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal()
    def __init__(self,parent=None):
        super(ThreadClass,self).__init__(parent)
        self.is_running = True
        self.mpdb = MPDB()
        
    
    def printProgressBar(self,iteration,total,prefix='',suffix='',decimals=1, length=100, fill='█', printEnd="\r"):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
        if iteration == total:
            print()

        
    def maximum(self,max_value,value):
        max_value[0] = value    
    
    def run(self):
        print("Starting...")
        if not "mpdb" in walk(getcwd()):
            mkdir("mpdb")
            
        max_value = [0]
        callback = {
            "setStatus": lambda text: print(text),
            "setProgress": lambda value: self.printProgressBar(value, max_value[0]),
            "setMax": lambda value: self.maximum(max_value, value)
        }
        mll.install.install_minecraft_version("1.16.5","mpdb",callback=callback)
        options = {"username":"TheKralGame"}
        subprocess.call(mll.command.get_minecraft_command("1.16.5","mpdb",options))
        self.any_signal.emit()
        
    def stop(self):
        self.is_running = False
        print("Stopping...")
        self.terminate()
        
        
        
def main():
    app = QApplication(argv)
    mpdb = MPDB()
    mpdb.show()
    exit(app.exec_())
    
if __name__ == "__main__":
    main()
