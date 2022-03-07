
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QFormLayout, QPushButton, QLineEdit, QGroupBox)
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

class LengthError(MyError):
    msg = "*** X and Y must have the same sample size ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"


errMsg = "*** Input Error ***"


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

class CorrelGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Correlation")
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

        self.OK_btn.clicked.connect(self.run_correlation)
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
    
        

    def run_correlation(self):

        result = ""

        X = self.X.text().split(",")
        Y = self.Y.text().split(",")
        X = [s.strip() for s in X]
        Y = [s.strip() for s in Y]
        
        all_str = [X, Y]
                

        try:
            
            if len(X) == 1 or len(Y) == 1:
                raise ArgError()

            bol_num = []    
            for i in all_str:
                bol_num.append(is_number(i))
                
        
            if not all(bol_num):
                raise InputError()

            if len(X) < 3 or len(Y) < 3:
                raise SizeError()
            

            if len(X) != len(Y):
                raise LengthError()
            
                    
            Xarr = np.array(X)
            Xarr = Xarr.astype(float)
            Yarr = np.array(Y)
            Yarr = Yarr.astype(float)

            Xn = Xarr.shape[0]
            
            r1, pvalue1 = stats.pearsonr(Xarr, Yarr)
            r1 = round(r1, 4)
            pvalue1 = round(pvalue1, 6)

            r2, pvalue2 = stats.spearmanr(Xarr, Yarr)
            r2 = round(r2, 4)
            pvalue2 = round(pvalue2, 6)

            
            r3, pvalue3 = stats.kendalltau(Xarr, Yarr)
            r3 = round(r3, 4)
            pvalue3 = round(pvalue3, 6)

            row1 = [r1, pvalue1]
            row2 = [r2, pvalue2]
            row3 = [r3, pvalue3]
            col_lst = ["Coefficient", "P-value"]
            index_lst = ["Pearson (r)", "Spearman (\u03C1)", "Kendall (\u03C4)"]

            stat_df = pd.DataFrame([row1, row2, row3], columns = col_lst, index = index_lst)

            result = (stat_df, Xn)


        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg

        except SizeError:
            result = SizeError.msg

        except LengthError:
            result = LengthError.msg
        
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
    window = CorrelGui()
    sys.exit(app.exec())
    