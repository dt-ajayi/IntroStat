
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, QPushButton, 
    QLineEdit, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
import scipy.stats as stats




class MyError(Exception):
    pass


class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class SizeError(MyError):
    msg = "*** X or Y data points cannot be less than 3 ***"

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
    QDialog, QLineEdit, QLabel, QPushButton, QGroupBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class TwoSampTGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Two-Sample T-Test")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        self.form = QFormLayout()
        self.form.setSpacing(20)
        gbox = QGroupBox("Data")
        btn_hbox = QHBoxLayout()


        

        # input box
        self.X = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.Y = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.form.insertRow(0, "X  ", self.X)
        self.form.insertRow(1, "Y", self.Y)
        gbox.setLayout(self.form)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_twosampttest)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)

        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()

        # Add widgets
        vbox.addWidget(gbox)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
    
        

    def run_twosampttest(self):

        result = ""

        X = self.X.text().split(",")
        Y = self.Y.text().split(",")
        
        
        
        all_str = [X, Y]
                

        try:
            if len(X) < 3 or len(Y) < 3:
                raise SizeError()
            
            if len(X) == 0 or len(Y) == 0:
                raise ArgError()

            bol_num = []    
            for i in all_str:
                bol_num.append(is_number(i))
                
        
            if not all(bol_num):
                raise InputError()
                    
            Xarr = np.array(X)
            Xarr = Xarr.astype(float)
            Yarr = np.array(Y)
            Yarr = Yarr.astype(float)

            Xn = Xarr.shape[0]
            Xbar = f"{Xarr.mean():.4f}"
            Xsd = f"{Xarr.std(ddof=1):.4f}"

            Yn = Yarr.shape[0]
            Ybar = f"{Yarr.mean():.4f}"
            Ysd = f"{Yarr.std(ddof=1):.4f}"

            TS, pvalue = stats.ttest_ind(a = Xarr, b = Yarr)
            TS = round(TS, 4)
            pvalue = round(pvalue, 6)

            
            row1 = [Xn, Xbar, Xsd, TS, pvalue]
            row2 = [Yn, Ybar, Ysd, "", ""]
            col_lst = ["n", "Mean", "SD", "t", "P-value"]
            index_lst = ["X", "Y"]

            stat_df = pd.DataFrame([row1, row2], columns = col_lst, index = index_lst)

            result = stat_df


        except ArgError:
            result = ArgError.msg

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
        self.X.setText("")
        self.Y.setText("")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = TwoSampTGui()
    sys.exit(app.exec())
    