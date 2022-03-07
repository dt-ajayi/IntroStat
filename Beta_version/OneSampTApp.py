
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
    msg = "*** X data points cannot be less than 3 ***"

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

class OneSampTGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("One-Sample T-Test")
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
        self.ref_mean = QLineEdit(placeholderText = "Enter or paste the reference mean")
        self.form.insertRow(0, "X", self.X)
        self.form.insertRow(1, "Mean", self.ref_mean)
        gbox.setLayout(self.form)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_onesampttest)
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
    
        

    def run_onesampttest(self):

        result = ""

        X = self.X.text().split(",")
        ref_mean = self.ref_mean.text().strip()
        
        
        all_str = [X, [ref_mean]]
                

        try:
            if len(X) < 3:
                raise SizeError()
            
            if len(X) == 0 or len(ref_mean) == 0:
                raise ArgError()

            bol_num = []    
            for i in all_str:
                bol_num.append(is_number(i))
                
        
            if not all(bol_num):
                raise InputError()
                    
            Xarr = np.array(X)
            Xarr = Xarr.astype(float)
            ref_mean = float(ref_mean)

            Xn = Xarr.shape[0]
            Xbar = f"{Xarr.mean():.4f}"
            Xsd = f"{Xarr.std(ddof=1):.4f}"


            TS, pvalue = stats.ttest_1samp(Xarr, ref_mean)
            TS = round(TS, 4)
            pvalue = round(pvalue, 6)


            col_lst = ["n", "Mean", "SD", "t", "P-value"]
            index_lst = ["X"]

            stat_df = pd.DataFrame([[Xn, Xbar, Xsd, TS, pvalue]], columns = col_lst, index = index_lst)

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
        self.ref_mean.setText("")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = OneSampTGui()
    sys.exit(app.exec())
    