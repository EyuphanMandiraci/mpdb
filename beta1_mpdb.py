from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import wget

class TestMPDB(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.resize(1000,600)
        #self.center()
        self.setWindowTitle("MPDB")
        self.setStyleSheet("QToolTip{color: #ffffff; background-color: #000000; border: 0px;}")
        hbox = QVBoxLayout()
        self.get_pack_id = QLineEdit(self)
        self.get_pack_id.move(460,270)
        button = QPushButton("Download",self)
        button.setToolTip("Download Button")
        button.move(460,300)
        button.clicked.connect(self.download_button)
        pack_id_label = QLabel("Pack ID: ",self)
        pack_id_label.move(400,274)
        hbox.addWidget(self.get_pack_id)
        hbox.addWidget(pack_id_label)
        
        self.show()
        

    
    def download_button(self):
        pack_id = self.get_pack_id.text()
        if pack_id == "test_pack":
            wget.download("https://mpdb.xyz/test_pack.zip")
        
def main():
    app = QApplication(sys.argv)
    mpdb = TestMPDB()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
