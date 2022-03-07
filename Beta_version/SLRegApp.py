
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, QPushButton, 
    QLineEdit, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf


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

class SLRegGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Simple Linear Regression")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        self.form = QFormLayout()
        self.form.setSpacing(20)
        gbox = QGroupBox("Data (comma separated)")
        btn_hbox = QHBoxLayout()


        # input box
        self.X = QLineEdit(placeholderText = "Enter or paste independent variable data")
        self.Y = QLineEdit(placeholderText = "Enter or paste dependent variable data")
        self.form.insertRow(0, "X  ", self.X)
        self.form.insertRow(1, "Y", self.Y)
        gbox.setLayout(self.form)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_slreg)
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
    
        

    def run_slreg(self):

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

            dat = pd.DataFrame({"X": Xarr, "Y": Yarr})
            
            lr_res = smf.ols('Y ~ X', data = dat).fit()

            aParm = lr_res.params.round(4)
            sParm = pd.Series(aParm, name = "Estimate")

            aPval = lr_res.pvalues.round(6)
            sPval = pd.Series(aPval, name = "P-value")

            rsq = round(lr_res.rsquared, 4)

            aTval = lr_res.tvalues.round(4)
            sTval =  pd.Series(aTval, name = "t value")

            aSE = lr_res.bse.round(4)
            sSE = pd.Series(aSE, name = "Std. error")

            slr_df = pd.concat([sParm, sSE, sTval, sPval], axis = 1)

            rsq, f_val, f_p = lr_res.rsquared, lr_res.fvalue, lr_res.f_pvalue

            result = (slr_df, Xn, rsq, f_val, f_p)


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
    window = SLRegGui()
    sys.exit(app.exec())
    