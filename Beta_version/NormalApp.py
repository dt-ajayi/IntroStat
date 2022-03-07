import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QPushButton, QLineEdit,
    QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from scipy.stats import norm

class MyError(Exception):
    pass

class InputError(MyError):
    msg = "*** Non-numeric value(s) encountered ***"

class ArgError(MyError):
    msg = "*** Input(s) missing ***"

errMsg = "*** Incorrect Input(s) ***"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

style_sheet = '''
    QDialog, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox{
        font-family: "Calibri";
        font-size: 20px
    }
'''

class NormalGui(QDialog):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.GUI()

    def initializeUI(self):
        self.setGeometry(630, 100, 500, 400)
        self.setWindowTitle("Normal Distribution")
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
        self.x = QLineEdit()
        self.x.setFocus()

        self.mu = QLineEdit()
        self.mu.setText("0")
        self.sigma = QLineEdit()
        self.sigma.setText("1")


        form1.addRow("x    ", self.x)
        form1.addRow("\u03bc    ", self.mu)
        form1.addRow("\u03c3    ", self.sigma)

        # combo box
        self.expr = QComboBox()
        self.expr.addItems(["P(X < x)", "P(X \u2264 x)", "P(X > x)", "P(X \u2265 x)"])
        form2.addRow("Select Probability", self.expr)
        fm2_hbox.addLayout(form2)
        fm2_hbox.addStretch()
        
        # button
        self.OK_btn = QPushButton("OK")
        self.clear_btn = QPushButton("Clear")
        self.cancel_btn = QPushButton("Cancel")

        self.OK_btn.clicked.connect(self.run_normal)
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
    

    def run_normal(self):

        result = ""
        x_str = self.x.text()
        mu_str = self.mu.text()
        sigma_str = self.sigma.text()


        try:
            lst_str = [x_str, mu_str, sigma_str]

            len_bol = [len(s.strip()) < 1 for s in lst_str]

            if any(len_bol):
                raise ArgError()

            lst_str_bol = [is_number(s.strip()) for s in lst_str]

            if not all(lst_str_bol):
                raise InputError()

            
            x = float(x_str)
            mu = float(mu_str)
            sigma = float(sigma_str)

            label = ""
            res = None
            
            if self.expr.currentIndex() == 0:
                res = norm.cdf(x = x, loc = mu, scale = sigma)
                label = f"P(X < {x})"

            elif self.expr.currentIndex() == 1:
                res = norm.cdf(x = x, loc = mu, scale = sigma)
                label = f"P(X \u2264 {x})"

            elif self.expr.currentIndex() == 2:
                res = 1 - norm.cdf(x = x, loc = mu, scale = sigma)
                label = f"P(X > {x})"

            elif self.expr.currentIndex() == 3:
                res = 1 - norm.cdf(x = x, loc = mu, scale = sigma)
                label = f"P(X \u2265 {x})"

            
            result = f"{label} = {res:.5f}"

        except ArgError:
            result = ArgError.msg

        except InputError:
            result = InputError.msg
                    
        except:
            result = errMsg

        finally:
            self.close()
            
        return result

    def clearInput(self):

        self.x.setText("")
        self.mu.setText("0")
        self.sigma.setText("1")
        self.expr.setCurrentIndex(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = NormalGui()
    sys.exit(app.exec())
    