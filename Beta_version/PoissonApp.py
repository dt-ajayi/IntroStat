import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout,QFormLayout, 
    QLabel, QPushButton, QLineEdit, QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from scipy.stats import poisson

class MyError(Exception):
    pass

class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"

class NegativeError(MyError):
    msg = "*** Values(s) cannot be less than 0 ***"


class IntError2(MyError):
    msg = "*** x must be a whole number ***"

errMsg = "*** Incorrect Input(s) ***"


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

class PoissonGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Poisson Distribution")
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
        self.mu = QLineEdit()
        self.x = QLineEdit()
        self.mu.setFocus()
        form1.addRow("\u03bb    ", self.mu)
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
        btn_hbox.addStretch()
        btn_hbox.addWidget(self.OK_btn)
        btn_hbox.addWidget(self.clear_btn)
        btn_hbox.addWidget(self.cancel_btn)


        self.OK_btn.clicked.connect(self.run_poisson)
        self.clear_btn.clicked.connect(self.clearInput)
        self.cancel_btn.clicked.connect(self.close)

        btn_hbox.addStretch()

        # Add widgets
        gbox.setLayout(form1)
        vbox.addWidget(gbox)
        vbox.addLayout(fm2_hbox)
        vbox.addLayout(btn_hbox)

        self.setLayout(vbox)

    def run_poisson(self):

        result = ""

        mu_str = self.mu.text()
        x_str = self.x.text()

        try:
            lst_str = [mu_str, x_str]

            len_bol = [len(s.strip()) < 1 for s in lst_str]

            if any(len_bol):
                raise ArgError()

            lst_str_bol = [is_number(s.strip()) for s in lst_str]

            if not all(lst_str_bol):
                raise InputError()

            
            if not is_int(x_str):
                raise IntError2()

            
            mu = float(mu_str)
            x = int(x_str)

            lst_num = [mu, x]
            neg_bol = [x < 0 for x in lst_num]

            if any(neg_bol):
                raise NegativeError()

            label = ""
            res = None
            if self.expr.currentIndex() == 0:
                res = poisson.pmf(k = x, mu = mu)
                label = f"P(X = {x})"

            elif self.expr.currentIndex() == 1:
                res = poisson.cdf(k = (x-1), mu = mu)
                label = f"P(X < {x})"

            elif self.expr.currentIndex() == 2:
                res = poisson.cdf(k = x, mu = mu)
                label = f"P(X \u2264 {x})"

            elif self.expr.currentIndex() == 3:
                res = 1 - poisson.cdf(k = x, mu = mu)
                label = f"P(X > {x})"

            elif self.expr.currentIndex() == 4:
                res = 1 - poisson.cdf(k = (x-1), mu = mu)
                label = f"P(X \u2265 {x})"

            result = f"{label} = {res:.5f}"

        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg

        except NegativeError:
            result = NegativeError.msg

        except IntError2:
            result = IntError2.msg

        except:
            result = errMsg

        finally:
            self.close()
            
        return result

    def clearInput(self):

        self.mu.setText("")
        self.x.setText("")
        self.expr.setCurrentIndex(0)
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = PoissonGui()
    sys.exit(app.exec())
    