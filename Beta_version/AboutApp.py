import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QLineEdit, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt




style_sheet = '''
    QDialog, QLabel, QLineEdit, QPushButton, QGroupBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class AboutGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 200, 100)
        self.setWindowTitle("About")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        btn_hbox = QHBoxLayout()

        vbox.setSpacing(20)
        msg = f'''
        IntroStat is an open-source statistical package written in Python and PyQt5.
        
        It is developed and maintained by David Ajayi (dtb.ajayi@gmail.com).
        '''
        abt_lab = QLabel(msg)
        # button
        OK_btn = QPushButton("OK")
        OK_btn.clicked.connect(self.close)
        btn_hbox.addStretch()
        btn_hbox.addWidget(OK_btn)
        # Add widgets
        vbox.addWidget(abt_lab)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = AboutGui()
    sys.exit(app.exec())
    