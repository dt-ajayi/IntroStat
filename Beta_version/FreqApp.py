import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
        QLabel, QPushButton, QLineEdit, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd



class MyError(Exception):
    pass

class SizeError(MyError):
    msg = "*** Data points cannot be less than 3 ***"

class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"


class ArgError(MyError):
    msg = "*** Input(s) missing ***"


errMsg = "*** Incorrect Input(s) ***"


def is_int(data):
    if isinstance(data, list):
        str_lst = [str(x) for x in data]
        bol = ["." in x for x in str_lst]
        if any(bol): return False
        else: return True
    else:
        s = str(data)
        if "." in s: return False
        else: return True



def is_number(data):

    bol = True
    if isinstance(data, list):
        try:
            [float(x) for x in data]
        except ValueError:
            bol = False
    else:
        try:
            float(data)
        except ValueError:
            bol = False

    return bol 

style_sheet = '''

    QDialog, QLabel, QLineEdit, QPushButton, QSpinBox, QGroupBox{
        font-family: "Calibri";
        font-size: 18px
    }
'''

class FreqGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Frequency Distribution")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form = QFormLayout()
        gbox = QGroupBox("Data")
        gbox_layout = QVBoxLayout()
        btn_hbox = QHBoxLayout()

        # input box
        self.data_box = QLineEdit()
        self.data_box.setFixedHeight(50)
        self.data_box.setFocus()
        self.data_box.setPlaceholderText("Enter or paste comma separated data")
        gbox_layout.addWidget(self.data_box)
        gbox.setLayout(gbox_layout)

        # var name
        self.var_name = QLineEdit()
        form.addRow("Variable Name", self.var_name)

        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_freq)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)


        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()



        # Add widgets
        vbox.addWidget(gbox)
        vbox.addLayout(form)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

    def run_freq(self):
        dat_str = self.data_box.text()
        data = []
        result = ""
        
        try:
            
            data = dat_str.split(",")

            if len(data) < 3:
                raise SizeError()
            
            data = [s.strip() for s in data]
            df = pd.DataFrame(data, columns = ["var"])
            counts = pd.crosstab(index= df["var"], columns= "Frequency (n)")
            counts.columns.name = ""
            counts.index.name = ""
            counts["Percent (%)"] = (counts["Frequency (n)"]*100/counts["Frequency (n)"].sum()).round(2)
            total = counts["Frequency (n)"].sum()

            var = self.var_name.text()

            if len(var) == 0:
                var = "Variable"

            var = f"{var} (N = {total})"
            counts[var] = counts.index
            counts2 = counts.iloc[:, [2, 0, 1]]
            result = counts2

        except SizeError:
            result = SizeError.msg
        
        except:
            result = errMsg
            
        finally:
            self.close()


        return result


    def clearInput(self):

        self.data_box.setText("")
        self.var_name.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = FreqGui()
    sys.exit(app.exec())
    