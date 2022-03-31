import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QPushButton, QLineEdit, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap

import numpy as np
import pandas as pd
import math


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

class IntError2(MyError):
    msg = "*** Frequency must be a whole number ***"


class ClassWidthError(MyError):
    msg = "*** Class width not constant ***"


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


style_sheet = '''


    QDialog, QLabel, QLineEdit, QPushButton, QSpinBox, QGroupBox{
        font-family: "Calibri";
        font-size: 18px
    }
'''

class GSumGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Summary Statistics (Grouped Data)")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form1 = QFormLayout()
        form2 = QFormLayout()
        gbox = QGroupBox("Data (comma separated)")
        btn_hbox = QHBoxLayout()



        # input box
        self.grp_box = QLineEdit()
        self.freq_box = QLineEdit()
        self.grp_box.setFixedHeight(50)
        self.freq_box.setFixedHeight(50)
        self.grp_box.setFocus()

        self.grp_box.setPlaceholderText("Enter or paste groups")
        self.freq_box.setPlaceholderText("Enter or paste frequencies")
        
        form1.addRow("", self.grp_box)
        form1.addRow("", self.freq_box)

        gbox.setLayout(form1)
    
        
        # var name
        self.var_name = QLineEdit()
        form2.addRow("Variable Name", self.var_name)

        # spin box
        self.dps = QSpinBox(minimum = 0, maximum = 10, value = 2)
        form2.addRow("Decimal Places", self.dps)
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_descriptive2)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)

        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()

        # Add widgets
        
        vbox.addWidget(gbox)
        vbox.addLayout(form2)
        vbox.addLayout(btn_hbox)
        self.setLayout(vbox)


    def run_descriptive2(self):

        dat_str = self.grp_box.text()
        freq_str = self.freq_box.text()
        dp = self.dps.value()
        var = self.var_name.text()
        result = ""
        
        try:
            
            data_lst = dat_str.split(",")
            freq_lst = freq_str.split(",")

            if len(data_lst) < 3 or len(freq_lst) < 3:
                raise SizeError()
            
            limits = []

            for s in data_lst:
                y = s.split("-")
                limits.extend(y)

            ll_str = [x for i,x in enumerate(limits) if (i == 0 or i%2 == 0)]
            ul_str = [x for i,x in enumerate(limits) if (i == 1 or i%2 == 1)]
            
            ll_bol = False in [is_number(s.strip()) for s in ll_str]
            ul_bol = False in [is_number(s.strip()) for s in ul_str]
            f_bol = False in [is_number(s.strip()) for s in freq_lst]

            if ll_bol or ul_bol or f_bol:
                raise InputError()

            f_int_bol = False in [is_int(s.strip()) for s in freq_lst]

            if f_int_bol:
                raise IntError2()

            ll = [float(x) for x in ll_str]
            ul = [float(x) for x in ul_str]
            freq = [float(x) for x in freq_lst]

            if len(ll) != len(freq):
                raise LengthError()

            df = pd.DataFrame({
                "class":data_lst,
                "LL": ll,
                "UL": ul,
                "f": freq
            })

            
            df["x"] = (df["LL"] + df["UL"])*0.5
            df["F"] = df["f"].cumsum()
            df["lcb"] = df["LL"] - 0.5
            df["ucb"] = df["UL"] + 0.5
            df["fx"] = df["f"]*df["x"]
            df["wc"] = df["ucb"] - df["lcb"]

            if len(pd.unique(df["wc"]).tolist()) > 1:
                raise ClassWidthError()

            sum_fx = df["fx"].sum()
            sum_f = df["f"].sum()
            _mean = round(sum_fx/sum_f, dp)
            df["xmms"] = (df["x"] - _mean)**2
            df["fxmms"] = df["f"]*df["xmms"]
            _std = round((df["fxmms"].sum()/(sum_f-1))**0.5, dp)

            cond = df["f"] == df["f"].max() 

            dfmo = df.where(cond)
            mod_df = dfmo[dfmo["f"].notna()]

            _mode = None

            if mod_df.shape[0] == 1:
                m_i = mod_df.index.tolist()[0]
                x_i = m_i - 1
                y_i = m_i + 1

                if m_i == 0:
                    lmo = df.loc[m_i, "lcb"]
                    w = df.loc[m_i, "ucb"] - df.loc[m_i, "lcb"]
                    fmo = df.loc[m_i, "f"]
                    fx = 0
                    fy = df.loc[y_i, "f"]
                    _mode = round(lmo + (w*(fmo - fx)/((fmo - fx) + (fmo - fy))), dp)
                
                elif m_i == (df.shape[0]-1):
                    lmo = df.loc[m_i, "lcb"]
                    w = df.loc[m_i, "ucb"] - df.loc[m_i, "lcb"]
                    fmo = df.loc[m_i, "f"]
                    fx = df.loc[x_i, "f"]
                    fy = 0
                    _mode = round(lmo + (w*(fmo - fx)/((fmo - fx) + (fmo - fy))), dp)

                else:
                    
                    lmo = df.loc[m_i, "lcb"]
                    w = df.loc[m_i, "ucb"] - df.loc[m_i, "lcb"]
                    fmo = df.loc[m_i, "f"]
                    fx = df.loc[x_i, "f"]
                    fy = df.loc[y_i, "f"]
                    _mode = round(lmo + (w*(fmo - fx)/((fmo - fx) + (fmo - fy))), dp)

            else:
                _mode = "More than one mode"

            _mode = f"Mode: {_mode}"

            cond2 = df["F"] >= math.ceil(df["f"].sum()/2)  
            dfmd = df.where(cond2)
            md_df = dfmd[dfmd["F"] == dfmd["F"].min()]

            md_i = md_df.index.tolist()[0]
            md_x_i = md_i - 1

            _median = None

            if md_i == 0:
                lmd = df.loc[md_i, "lcb"] 
                Nover2 = df["f"].sum()*0.5
                Fb = 0
                fmd = df.loc[md_i, "f"]
                wmd = df.loc[md_i, "ucb"] - df.loc[md_i, "lcb"] 
                _median = round(lmd + (((Nover2 - Fb)*wmd)/fmd), dp)

            else:
                lmd = df.loc[md_i, "lcb"] 
                Nover2 = df["f"].sum()*0.5
                Fb = df.loc[md_x_i, "F"]
                fmd = df.loc[md_i, "f"]
                wmd = df.loc[md_i, "ucb"] - df.loc[md_i, "lcb"] 

                _median = round(lmd + (((Nover2 - Fb)*wmd)/fmd), dp)

            _N = int(df["f"].sum())
            res_lst = [[_N, _mean, _median, _std]]
            df_labs = ["N", "Mean", "Median", "SD"]

            res_df = pd.DataFrame(res_lst, columns= df_labs)
    
            if len(var) == 0:
                var = "Variable"

            result = (res_df, _mode, var)
            
        except SizeError:
            result = SizeError.msg

        except InputError:
            result = InputError.msg

        except IntError2:
            result = IntError2.msg

        except LengthError:
            result = LengthError.msg

        except ClassWidthError:
            result = ClassWidthError.msg
            
        except:
            result = errMsg

        finally:
            self.close()


        return result

    
    def clearInput(self):

        self.grp_box.setText("")
        self.freq_box.setText("")
        self.var_name.setText("")
        self.dps.setValue(2)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = GSumGui()
    sys.exit(app.exec())
    