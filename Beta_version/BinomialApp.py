import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, 
    QLabel, QPushButton, QLineEdit, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from scipy.stats import binom

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

class ProbError3(MyError):
    msg = "*** Probability of zero not allowed ***"

class NegativeError(MyError):
    msg = "*** Values(s) cannot be less than 0 ***"

class NGOneError(MyError):
    msg = "*** n must be greater than 1 ***"

class XGNError(MyError):
    msg = "*** x cannot be greater than n ***"

class IntError(MyError):
    msg = "*** x and n must be whole numbers ***"

errMsg = "*** Input Error ***"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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
    QDialog, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class BinomialGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Binomial Distribution")
        self.show()

    def GUI(self):
        vbox = QVBoxLayout()
        vbox.setSpacing(20)
        form1 = QFormLayout()
        form1.setSpacing(20)
        form2 = QFormLayout()
        gbox = QGroupBox("Data")
        btn_hbox = QHBoxLayout()
        fm2_hbox = QHBoxLayout()



        # input box
        self.n = QLineEdit()
        self.p = QLineEdit()
        self.x = QLineEdit()
        self.n.setFocus()
        form1.addRow("n    ", self.n)
        form1.addRow("p    ", self.p)
        form1.addRow("x    ", self.x)

        # combo box
        self.expr = QComboBox()
        self.expr.addItems(["P(X = x)", "P(X < x)", "P(X \u2264 x)", "P(X > x)", "P(X \u2265 x)"])
        form2.addRow("Select Probability", self.expr)
        fm2_hbox.addLayout(form2)
        fm2_hbox.addStretch()
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")


        self.OK_btn.clicked.connect(self.run_binomial)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)


        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)
        btn_hbox.addStretch()

        # Add widgets
        gbox.setLayout(form1)
        vbox.addWidget(gbox)
        vbox.addLayout(fm2_hbox)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)
    
    def run_binomial(self):

        result = ""

        n_str = self.n.text()
        p_str = self.p.text()
        x_str = self.x.text()

        try:
            lst_str = [n_str, p_str, x_str]

            len_bol = [len(s.strip()) < 1 for s in lst_str]

            if any(len_bol):
                raise ArgError()

            lst_str_bol = [is_number(s.strip()) for s in lst_str]

            if not all(lst_str_bol):
                raise InputError()

            if not is_int([n_str, x_str]):
                raise IntError()

            n = int(n_str)
            p = float(p_str)
            x = int(x_str)

            lst_num = [n, p, x]
            neg_bol = [x < 0 for x in lst_num]

            if any(neg_bol):
                raise NegativeError()

            if n < 2:
                raise NGOneError()

            if x > n:
                raise XGNError()

            if p < 0:
                raise ProbError2()

            if p > 1:
                raise ProbError1()

            if p == 0:
                raise ProbError3()


            label = ""
            res = None
            if self.expr.currentIndex() == 0:
                res = binom.pmf(k = x, n = n, p = p)
                label = f"P(X = {x})"

            elif self.expr.currentIndex() == 1:
                res = binom.cdf(k = (x-1), n = n, p = p)
                label = f"P(X < {x})"

            elif self.expr.currentIndex() == 2:
                res = binom.cdf(k = x, n = n, p = p)
                label = f"P(X \u2264 {x})"

            elif self.expr.currentIndex() == 3:
                res = 1 - binom.cdf(k = x, n = n, p = p)
                label = f"P(X > {x})"

            elif self.expr.currentIndex() == 4:
                res = 1 - binom.cdf(k = (x-1), n = n, p = p)
                label = f"P(X \u2265 {x})"

            result = f"{label} = {res:.5f}"

        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg

        except NegativeError:
            result = NegativeError.msg

        except NGOneError:
            result = NGOneError.msg

        except XGNError:
            result = XGNError.msg

        except ProbError2:
            result = ProbError2.msg

        except ProbError1:
            result = ProbError1.msg

        except ProbError3:
            result = ProbError3.msg

        except IntError:
            result = IntError.msg
            
        except:
            result = errMsg

        finally:
            self.close()

        return result  

    def clearInput(self):

        self.n.setText("")
        self.p.setText("")
        self.x.setText("")
        self.expr.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = BinomialGui()
    sys.exit(app.exec())
    