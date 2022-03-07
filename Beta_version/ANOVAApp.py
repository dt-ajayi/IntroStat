
import sys, os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, QPushButton, 
    QLineEdit, QGroupBox, QSpinBox)
from PyQt5.QtCore import Qt
import numpy as np
import pandas as pd
from scipy.stats import f_oneway




class MyError(Exception):
    pass


class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class SizeError(MyError):
    msg = "*** Data points cannot be less than 3 ***"

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

def eval_len(nested_lst, n):
    lst = []
    for i in nested_lst:
        lst.append(len(i))

    if min(lst) >= n:
        return True

    else: return False



style_sheet = '''
    QDialog, QLineEdit, QLabel, QPushButton, QGroupBox, QSpinBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class ANOVAGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("One-way ANOVA")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form1 = QFormLayout()
        self.form2 = QFormLayout()
        self.form2.setSpacing(20)
        gbox = QGroupBox("Data")
        btn_hbox = QHBoxLayout()
        fm1_hbox = QHBoxLayout()


        # update widget
        self.nrow = QSpinBox(minimum = 3, maximum = 5, value = 3)
        form1.addRow("Number of groups", self.nrow)
        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_tab)
        fm1_hbox.addLayout(form1)
        fm1_hbox.addWidget(self.update_btn)


        # input box
        self.X1 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.X2 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.X3 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.X4 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.X5 = QLineEdit(placeholderText = "Enter or paste comma separated data")
        self.form2.insertRow(0, "X1 ", self.X1)
        self.form2.insertRow(1, "X2 ", self.X2)
        self.form2.insertRow(2, "X3 ", self.X3)
        gbox.setLayout(self.form2)
        
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_anova)
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

        
        
        if self.row_count == 3:
            self.clear_rows()

            self.form2.insertRow(0, "X1 ", self.X1)
            self.form2.insertRow(1, "X2 ", self.X2)
            self.form2.insertRow(2, "X3 ", self.X3)
            
        elif self.row_count == 4:
            
            self.clear_rows()

            self.form2.insertRow(0, "X1 ", self.X1)
            self.form2.insertRow(1, "X2 ", self.X2)
            self.form2.insertRow(2, "X3 ", self.X3)
            self.form2.insertRow(3, "X4 ", self.X4)
            
        elif self.row_count == 5:

            self.clear_rows()

            self.form2.insertRow(0, "X1 ", self.X1)
            self.form2.insertRow(1, "X2 ", self.X2)
            self.form2.insertRow(2, "X3 ", self.X3)
            self.form2.insertRow(3, "X4 ", self.X4)
            self.form2.insertRow(4, "X5 ", self.X5)
            

    def run_anova(self):
        pass

        result = ""

        slX1 = self.X1.text().split(",")
        slX2 = self.X2.text().split(",")
        slX3 = self.X3.text().split(",")
        slX4 = self.X4.text().split(",")
        slX5 = self.X5.text().split(",")

        
        all_str = [slX1, slX2, slX3, slX4, slX5]
        
        all_str2 = []
        

        try:
            for i in all_str:
                if len(i) == 1:
                    del i
                else:
                    all_str2.append(i)
                
            if len(all_str2) < self.nrow.value():
                raise ArgError()
                    
            num_lst = []    
            for i in all_str2:
                num_lst.extend(i)
                

            if not is_number(num_lst):
                raise InputError()

            if not eval_len(all_str2, 3):
                raise SizeError()
                    
            
            if len(all_str2) == 3:
                aX1 = np.array(slX1, dtype = float)
                aX2 = np.array(slX2, dtype = float)
                aX3 = np.array(slX3, dtype = float)
                
                xbar1, xbar2, xbar3 = aX1.mean(), aX2.mean(), aX3.mean()
                xsd1, xsd2, xsd3 = aX1.std(ddof = 1), aX2.std(ddof = 1), aX3.std(ddof = 1)
                xn1, xn2, xn3 = aX1.shape[0], aX2.shape[0], aX3.shape[0]
                TS, pvalue = f_oneway(aX1, aX2, aX3)

                pvalue = round(pvalue, 6)

                
                axbar = np.array([xbar1, xbar2, xbar3])
                aSD = np.array([xsd1, xsd2, xsd3])
                aVar = aSD**2
                aN = np.array([xn1, xn2, xn3])
                aNm1 = aN - 1
                

                # Sum of squares
                ov_xbar = axbar.mean()
                SSB = (((axbar - ov_xbar)**2) *aN).sum()
                SSW = (aNm1*aVar).sum()
                SST = SSB + SSW
                dfB = 2
                dfW = aNm1.sum()
                dfT = dfB + dfW

                # Mean squares
                MSB = SSB/dfB
                MSW = SSW/dfW
                MST = ""

                Fcal = round(MSB/MSW, 4)

                SSB = round(SSB, 4)
                SSW = round(SSW, 4)
                SST = round(SST, 4)
                MSB = round(MSB, 4)
                MSW = round(MSW, 4)

                anvtab1 = ["Between Group", SSB, dfB, MSB, Fcal, pvalue]
                anvtab2 = ["Within Group", SSW, dfW, MSW, "", ""]
                anvtab3 = ["Total", SST, dfT, MST, "", ""]
                col_names = ["Variance source", "SS", "df", "MS", "F", "P-value"]

                anova_df = pd.DataFrame([anvtab1, anvtab2, anvtab3], columns = col_names)
                
                result = anova_df
                
                
            elif len(all_str2) == 4:
                aX1 = np.array(slX1, dtype = float)
                aX2 = np.array(slX2, dtype = float)
                aX3 = np.array(slX3, dtype = float)
                aX4 = np.array(slX4, dtype = float)
                
                xbar1, xbar2, xbar3, xbar4 = aX1.mean(), aX2.mean(), aX3.mean(), aX4.mean()
                xsd1, xsd2, xsd3, xsd4 = aX1.std(ddof = 1), aX2.std(ddof = 1), aX3.std(ddof = 1), aX4.std(ddof = 1)
                xn1, xn2, xn3, xn4 = aX1.shape[0], aX2.shape[0], aX3.shape[0], aX4.shape[0]
                TS, pvalue = f_oneway(aX1, aX2, aX3, aX4)

                pvalue = round(pvalue, 6)

                axbar = np.array([xbar1, xbar2, xbar3, xbar4])
                aSD = np.array([xsd1, xsd2, xsd3, xsd4])
                aVar = aSD**2
                aN = np.array([xn1, xn2, xn3, xn4])
                aNm1 = aN - 1
                

                # Sum of squares
                ov_xbar = axbar.mean()
                SSB = (((axbar - ov_xbar)**2) *aN).sum()
                SSW = (aNm1*aVar).sum()
                SST = SSB + SSW
                dfB = 3
                dfW = aNm1.sum()
                dfT = dfB + dfW

                # Mean squares
                MSB = SSB/dfB
                MSW = SSW/dfW
                MST = ""

                Fcal = round(MSB/MSW, 4)

                SSB = round(SSB, 4)
                SSW = round(SSW, 4)
                SST = round(SST, 4)
                MSB = round(MSB, 4)
                MSW = round(MSW, 4)

                anvtab1 = ["Between Group", SSB, dfB, MSB, Fcal, pvalue]
                anvtab2 = ["Within Group", SSW, dfW, MSW, "", ""]
                anvtab3 = ["Total", SST, dfT, MST, "", ""]
                col_names = ["Variance source", "SS", "df", "MS", "F", "P-value"]

                anova_df = pd.DataFrame([anvtab1, anvtab2, anvtab3], columns = col_names)
                
                result = anova_df
                

            elif len(all_str2) == 5:
                aX1 = np.array(slX1, dtype = float)
                aX2 = np.array(slX2, dtype = float)
                aX3 = np.array(slX3, dtype = float)
                aX4 = np.array(slX4, dtype = float)
                aX5 = np.array(slX5, dtype = float)
                
                xbar1, xbar2, xbar3, xbar4, xbar5  = aX1.mean(), aX2.mean(), aX3.mean(), aX4.mean(), aX5.mean()
                xsd1, xsd2, xsd3, xsd4, xsd5  = aX1.std(ddof = 1), aX2.std(ddof = 1), aX3.std(ddof = 1), aX4.std(ddof = 1), aX5.std(ddof = 1)
                xn1, xn2, xn3, xn4, xn5 = aX1.shape[0], aX2.shape[0], aX3.shape[0], aX4.shape[0], aX5.shape[0]
                TS, pvalue = f_oneway(aX1, aX2, aX3, aX4, aX5)

                pvalue = round(pvalue, 6)

                axbar = np.array([xbar1, xbar2, xbar3, xbar4, xbar5])
                aSD = np.array([xsd1, xsd2, xsd3, xsd4, xsd5])
                aVar = aSD**2
                aN = np.array([xn1, xn2, xn3, xn4, xn5])
                aNm1 = aN - 1
                

                # Sum of squares
                ov_xbar = axbar.mean()
                SSB = (((axbar - ov_xbar)**2) *aN).sum()
                SSW = (aNm1*aVar).sum()
                SST = SSB + SSW
                dfB = 4
                dfW = aNm1.sum()
                dfT = dfB + dfW

                # Mean squares
                MSB = SSB/dfB
                MSW = SSW/dfW
                MST = ""

                Fcal = round(MSB/MSW, 4)

                SSB = round(SSB, 4)
                SSW = round(SSW, 4)
                SST = round(SST, 4)
                MSB = round(MSB, 4)
                MSW = round(MSW, 4)

                anvtab1 = ["Between Group", SSB, dfB, MSB, Fcal, pvalue]
                anvtab2 = ["Within Group", SSW, dfW, MSW, "", ""]
                anvtab3 = ["Total", SST, dfT, MST, "", ""]
                col_names = ["Variance source", "SS", "df", "MS", "F", "P-value"]

                anova_df = pd.DataFrame([anvtab1, anvtab2, anvtab3], columns = col_names)
                
                result = anova_df
                
        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg
        
        except SizeError:
            result = SizeError.msg

        except:
            result = errMsg

        finally:
            self.close()
            

        return result


    def clearInput(self):

        self.X1.setText("")
        self.X2.setText("")
        self.X3.setText("")
        self.X4.setText("")
        self.X5.setText("")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = ANOVAGui()
    sys.exit(app.exec())
    