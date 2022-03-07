
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, QPushButton, 
    QLineEdit, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar




class MyError(Exception):
    pass


class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class LengthError(MyError):
    msg = "*** Rows length unequal ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"


class NegativeError(MyError):
    msg = "*** Values(s) cannot be less than 0 ***"


class IntError(MyError):
    msg = "*** Data must be whole numbers ***"


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

def len_equal(nested_lst):
    lst = []
    for i in nested_lst:
        lst.append(len(i))

    if (max(lst) - min(lst)) == 0:
        return True

    else: return False



style_sheet = '''
    QDialog, QLineEdit, QLabel, QPushButton, QGroupBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class McNemarGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("McNemar Test")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        self.form = QFormLayout()
        self.form.setSpacing(20)
        gbox = QGroupBox("Contingency Table")
        btn_hbox = QHBoxLayout()


        

        # input box
        self.row1 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.row2 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.form.insertRow(0, "Row 1", self.row1)
        self.form.insertRow(1, "Row 2", self.row2)
        gbox.setLayout(self.form)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_mcnemar)
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
    
        

    def run_mcnemar(self):

        result = ""

        slr1 = self.row1.text().split(",")
        slr2 = self.row2.text().split(",")
        
        
        all_str = [slr1, slr2]
        
        all_str2 = []
        

        try:
            for i in all_str:
                if len(i) == 1:
                    del i
                else:
                    all_str2.append(i)
                
            if len(all_str2) < 2:
                raise ArgError()
                    
            bol_num = []    
            for i in all_str2:
                bol_num.append(is_number(i))
                
        
            if not all(bol_num):
                raise InputError()

            bol_int = []

            for i in all_str2:
                bol_int.append(is_int(i))
                
        
            if not all(bol_int):
                raise IntError()


            if not len_equal(all_str2):
                raise LengthError()

                    
            obs = np.array(all_str2)
            obs = obs.astype(int)

            res1 = mcnemar(obs, exact=False, correction=False)
            res2 = mcnemar(obs, exact=False, correction=True)
            mcn1, pval1 = res1.statistic, res1.pvalue
            mcn2, pval2 = res2.statistic, res2.pvalue          

            mcn1 = round(mcn1, 4)
            pval1 = round(pval1, 6)
            mcn2 = round(mcn2, 4)
            pval2 = round(pval2, 6)
            

            mcn_lst = [mcn1, pval1]
            yates_lst = [mcn2, pval2]
            col_lst = ["Value", "P-value"]
            index_lst = ["McNemar", "Yates' Correction"]

            stat_df = pd.DataFrame([mcn_lst, yates_lst], columns = col_lst, index = index_lst)

            result = stat_df


        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg
        
        except IntError:
            result = IntError.msg

        except LengthError:
            result = LengthError.msg
        
        except:
            result = errMsg

        finally:
            self.close()

        return result


    def clearInput(self):

        self.row1.setText("")
        self.row2.setText("")
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = McNemarGui()
    sys.exit(app.exec())
    