
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, QPushButton, 
    QLineEdit, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import fisher_exact




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


def gen_header(n, name):
    name_lst = [name]*n
    num = list((range(1, (n+1))))
    num_lst = [str(x) for x in num]

    name_num = list(zip(name_lst, num_lst))

    header = []

    for i in name_num:
        x = "".join(i)
        header.append(x)
        
    return header


style_sheet = '''
    QDialog, QLineEdit, QLabel, QPushButton, QGroupBox, QSpinBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class ChisqGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Chi-Square Test")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form1 = QFormLayout()
        self.form2 = QFormLayout()
        self.form2.setSpacing(20)
        gbox = QGroupBox("Contingency Table")
        btn_hbox = QHBoxLayout()
        fm1_hbox = QHBoxLayout()


        # update widget
        self.nrow = QSpinBox(minimum = 2, maximum = 5, value = 2)
        form1.addRow("Number of rows", self.nrow)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_tab)
        fm1_hbox.addLayout(form1)
        fm1_hbox.addWidget(self.update_btn)


        # input box
        self.row1 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.row2 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.row3 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.row4 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.row5 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.form2.insertRow(0, "Row 1", self.row1)
        self.form2.insertRow(1, "Row 2", self.row2)
        gbox.setLayout(self.form2)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_chisq)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)

        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()

        # Add widgets
        vbox.addLayout(fm1_hbox)
        vbox.addWidget(gbox)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
    

    def clear_rows(self):
        for i in reversed(range(self.form2.count())): 
            self.form2.itemAt(i).widget().setParent(None)   


    def update_tab(self):
        self.row_count = self.nrow.value()
        self.clear_rows()

        
        if self.row_count == 2:
            self.clear_rows()

            self.form2.insertRow(0, "Row 1", self.row1)
            self.form2.insertRow(1, "Row 2", self.row2)

        elif self.row_count == 3:
            self.clear_rows()

            self.form2.insertRow(0, "Row 1", self.row1)
            self.form2.insertRow(1, "Row 2", self.row2)
            self.form2.insertRow(2, "Row 3", self.row3)
            
        elif self.row_count == 4:
            
            self.clear_rows()

            self.form2.insertRow(0, "Row 1", self.row1)
            self.form2.insertRow(1, "Row 2", self.row2)
            self.form2.insertRow(2, "Row 3", self.row3)
            self.form2.insertRow(3, "Row 4", self.row4)
            
        elif self.row_count == 5:

            self.clear_rows()

            self.form2.insertRow(0, "Row 1", self.row1)
            self.form2.insertRow(1, "Row 2", self.row2)
            self.form2.insertRow(2, "Row 3", self.row3)
            self.form2.insertRow(3, "Row 4", self.row4)
            self.form2.insertRow(4, "Row 5", self.row5)
        

    def run_chisq(self):

        result = ""

        slr1 = self.row1.text().split(",")
        slr2 = self.row2.text().split(",")
        slr3 = self.row3.text().split(",")
        slr4 = self.row4.text().split(",")
        slr5 = self.row5.text().split(",")

        
        all_str = [slr1, slr2, slr3, slr4, slr5]
        
        all_str2 = []
        

        try:
            for i in all_str:
                if len(i) == 1:
                    del i
                else:
                    all_str2.append(i)
                
            if len(all_str2) < self.nrow.value():
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

            if obs.shape == (2, 2):
                chi2, pchsq, dof, ex = chi2_contingency(obs, correction = False)
                
                yates, pyates, dof, ex = chi2_contingency(obs, correction = True)

                oddsr, pfet = fisher_exact(obs, alternative='two-sided')

                chi2 = round(chi2, 4)
                pchsq = round(pchsq, 6)
                yates = round(yates, 4)
                pyates = round(pyates, 6)
                pfet = round(pfet, 6)

                nrow, ncol = ex.shape
                col_lab = gen_header(ncol, "Col ")
                row_lab = gen_header(nrow, "Row ")

                ex_df = pd.DataFrame(ex, columns = col_lab, index = row_lab)
                ex_df = ex_df.round(2)
                num = ex_df.where(ex_df < 5).notna().sum().sum()
                denom = ex_df.shape[0]*ex_df.shape[1]
                ex_b5 = num
                prop_ex_b5 = round((num/denom*100), 1)

                
                chi_lst = [chi2, dof, pchsq]
                yates_lst = [yates, dof, pyates]
                fet_lst = ["", "", pfet]
                col_lst = ["Value", "df", "P-value"]
                index_lst = ["Pearson Chi-square", "Yates' Correction" ,"Fisher's Exact Test"]

                stat_df = pd.DataFrame([chi_lst, yates_lst, fet_lst], columns = col_lst, index = index_lst)

                result = (ex_df, ex_b5, prop_ex_b5, stat_df)

            else:
                chi2, pchsq, dof, ex = chi2_contingency(obs, correction = False)
                
                yates, pyates, dof, ex = chi2_contingency(obs, correction = True)

                chi2 = round(chi2, 4)
                pchsq = round(pchsq, 6)
                yates = round(yates, 4)
                pyates = round(pyates, 6)

                nrow, ncol = ex.shape
                col_lab = gen_header(ncol, "Col ")
                row_lab = gen_header(nrow, "Row ")

                ex_df = pd.DataFrame(ex, columns = col_lab, index = row_lab)
                ex_df = ex_df.round(2)
                num = ex_df.where(ex_df < 5).notna().sum().sum()
                denom = ex_df.shape[0]*ex_df.shape[1]
                ex_b5 = num
                prop_ex_b5 = round((num/denom*100), 1)

                
                chi_lst = [chi2, dof, pchsq]
                yates_lst = [yates, dof, pyates]
                col_lst = ["Value", "df", "P-value"]
                index_lst = ["Pearson Chi-square", "Yates' Correction"]

                stat_df = pd.DataFrame([chi_lst, yates_lst], columns = col_lst, index = index_lst)

                result = (ex_df, ex_b5, prop_ex_b5, stat_df)

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
        self.row3.setText("")
        self.row4.setText("")
        self.row5.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = ChisqGui()
    sys.exit(app.exec())
    