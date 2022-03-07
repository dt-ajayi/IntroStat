import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout,QHBoxLayout , QFormLayout, 
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

class LengthError(MyError):
    msg = "*** Variables are of unequal lengths ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"


errMsg = "*** Incorrect Input(s) ***"




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

class UgSumGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Summary Statistics (Ungrouped Data)")
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

        # spin box
        self.dps = QSpinBox(minimum = 0, maximum = 10, value = 2)
        form.addRow("Decimal Places", self.dps)
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_descriptive1)
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

    def my_mode(self, data):
        counts = dict()

        for dp in data:
            counts[dp] = counts.get(dp, 0) + 1

        hf = max(counts.values())
        mode_lst = []
        mode = None
        for k,v in counts.items():
            if v == hf:
                mode_lst.append(k)
        
        if len(mode_lst) == 1:
            mode = f"Mode = {mode_lst[0]} (frequency: {hf})"
        else:
            mode = f"Mode = {mode_lst} (frequency: {hf})"

        return mode 

    def run_descriptive1(self):

        dat_str = self.data_box.text()
        dp = self.dps.value()
        var = self.var_name.text()
        data = []
        result = ""
        
        try:
            
            data_lst = dat_str.split(",")

            if len(data_lst) < 3:
                raise SizeError()

            if False in [is_number(s.strip()) for s in data_lst]:
                raise InputError()
            data = [float(x) for x in data_lst]
            
            data_df = pd.Series(data, name = "df")

            des_df = data_df.describe()
    
            _N = int(des_df.iloc[0])
            _mean = round(des_df.iloc[1], dp)
            _std = round(des_df.iloc[2], dp)
            _median = round(des_df.iloc[5], dp)
            _min = round(des_df.iloc[3], dp)
            _max = round(des_df.iloc[7], dp)
            _range = round((_max - _min), dp)
            _IQR = round(des_df.iloc[6] - des_df.iloc[4], dp)

            res_lst = [[_N, _mean, _median, _std, _min, _range, _max, _IQR]]
            df_labs = ["N", "Mean", "Median", "SD", "Min", "Range","Max", "IQR"]

            res_df = pd.DataFrame(res_lst, columns= df_labs)
            if len(var) == 0:
                var = "Variable"

            _mode = self.my_mode(data)

            result = (res_df, _mode, var)

        except SizeError:
            result = SizeError.msg
        
        except InputError:
            result = InputError.msg
        
        except:
            result = errMsg
            
        finally:
            self.close()

        return result
        
    def clearInput(self):

        self.data_box.setText("")
        self.var_name.setText("")
        self.dps.setValue(2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = UgSumGui()
    sys.exit(app.exec())
    