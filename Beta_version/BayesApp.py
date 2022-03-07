import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QLineEdit, QSpinBox, QGroupBox)
from PyQt5.QtCore import Qt



class MyError(Exception):
    pass

class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"


class ProbError1(MyError):
    msg = "*** Probability cannot be greater than 1 ***"

class ProbError2(MyError):
    msg = "*** Probability cannot be less than 0 ***"

class ZeroError(MyError):
    msg = "*** Value(s) must be greater than zero ***"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

errMsg = "*** Incorrect Input(s) ***"


style_sheet = '''
    QDialog, QLabel, QLineEdit, QPushButton, QGroupBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class BayesGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Bayes' Rule (Two Events)")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form = QFormLayout()
        form.setSpacing(20)
        gbox = QGroupBox("Data")
        btn_hbox = QHBoxLayout()

        # input box
        self.pBgA = QLineEdit()
        self.pA = QLineEdit()
        self.pBcgAc = QLineEdit()
        self.pBgA.setFocus()

        form.addRow("P(B|A)", self.pBgA)
        form.addRow("P(B'|A')", self.pBcgAc)
        form.addRow("P(A)", self.pA)
       
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")


        self.OK_btn.clicked.connect(self.run_bayes)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)

        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()

        # Add widgets
        gbox.setLayout(form)
        vbox.addWidget(gbox)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
    

    def run_bayes(self):

        result = ""
        pBgA_str = self.pBgA.text()
        pA_str = self.pA.text()
        pBcgAc_str = self.pBcgAc.text()

        try:
            lst_str = [pBgA_str, pA_str, pBcgAc_str]

            len_bol = [len(s.strip()) < 1 for s in lst_str]

            if any(len_bol):
                raise ArgError()

            lst_str_bol = [is_number(s.strip()) for s in lst_str]

            if all(lst_str_bol) != True:
                raise InputError()

            pBgA = float(pBgA_str)
            pA = float(pA_str)
            pBcgAc = float(pBcgAc_str)

            lst_num = [pBgA, pA, pBcgAc]
            lt0_bol = [x < 0 for x in lst_num]

            if any(lt0_bol):
                raise ProbError2()

            gt1_bol = [x > 1 for x in lst_num]

            if any(gt1_bol):
                raise ProbError1()

            ge0_bol = [x == 0 for x in lst_num]

            if any(ge0_bol):
                raise ZeroError()

            pBgAc = 1 - pBcgAc
            pAc = 1 - pA

            pAgB = pBgA*pA/((pBgA*pA)+(pBgAc*pAc))
            
            result = f"P(A|B) = {pAgB:.5f}"


        except ArgError:
            result = ArgError.msg
        
        except InputError:
            result = InputError.msg

        except ProbError2:
            result = ProbError2.msg

        except ProbError1:
            result = ProbError1.msg

        except ZeroError:
            result = ZeroError.msg

        except:
            result = errMsg

        finally:
            self.close()

        return result

    def clearInput(self):

        self.pBgA.setText("")
        self.pA.setText("")
        self.pBcgAc.setText("")
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = BayesGui()
    sys.exit(app.exec())
    