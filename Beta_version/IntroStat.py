
import sys, os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, QWidget, 
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QFileDialog)
from PyQt5.QtGui import QFont, QIcon
import pandas
from tabulate import tabulate



from FreqApp import FreqGui
from UgSumApp import UgSumGui
from GSumApp import GSumGui
from BayesApp import BayesGui
from BinomialApp import BinomialGui
from PoissonApp import PoissonGui
from NormalApp import NormalGui
from ChisqApp import ChisqGui
from McNemarApp import McNemarGui
from OneSampTApp import OneSampTGui
from TwoSampTApp import TwoSampTGui
from PairedTApp import PairedTGui
from ANOVAApp import ANOVAGui
from CorrelApp import CorrelGui
from SLRegApp import SLRegGui
from AboutApp import AboutGui





style_sheet = '''

    QMenuBar{
        font-family: "Calibri";
        font-size: 19px;
        background-color: #F6F1F9;
        border: 1px solid blue;
        spacing: 5px; 
        padding: 5px
    }

    QMenu{
        font-family: "Helvetica";
        font-size: 15px;
        background-color: #B0C4DE; 
        border: 1px solid black; 
        
    }

    
    QTextEdit{
        font-size: 18px;
        margin: 10px;
        padding: 10px
    }


    QDialog, QLabel, QLineEdit, QPushButton, QGroupBox, QComboBox, QSpinBox, QCheckBox{
        font-family: "Verdana";
        font-size: 15px
    }

'''

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initializeUI()
        self.createMenu()
        

    def initializeUI(self):
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("IntroStat (Beta version)")        

        
        # Widgets
        self.doc = QTextEdit(acceptRichText = True, readOnly = True)
        font = QFont("Monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.doc.setFont(font)
        self.setCentralWidget(self.doc)
        self.show()

    def createMenu(self):
        # create actions for file menu
        self.clear_act = QAction("Clear Output", self)
        self.clear_act.triggered.connect(self.clear)

        self.quit_act = QAction("Quit Program", self)
        self.quit_act.triggered.connect(self.quit)


        # create actions for descriptives menu
        self.freq_act = QAction("Frequencies", self)
        self.freq_act.triggered.connect(self.frequency)

        self.ungroupedData_act = QAction("Ungrouped Data", self)
        self.ungroupedData_act.triggered.connect(self.ungroupedSumStat)

        self.groupedData_act = QAction("Grouped Data", self)
        self.groupedData_act.triggered.connect(self.grouped)


        # create actions for probability menu
        self.bayes_act = QAction("Bayes' Rule", self)
        self.bayes_act.triggered.connect(self.bayesian)

        self.binomial_act = QAction("Binomial Distribution", self)
        self.binomial_act.triggered.connect(self._binomial)

        self.poisson_act = QAction("Poisson Distribution", self)
        self.poisson_act.triggered.connect(self._poisson)

        self.normal_act = QAction("Normal Distribution", self)
        self.normal_act.triggered.connect(self._normal)


        # create actions for bivariate menu
        self.correl_act = QAction("Correlation", self)
        self.correl_act.triggered.connect(self.correlation)

        self.chisq_act = QAction("Chi-square Test", self)
        self.chisq_act.triggered.connect(self.chiSquare)

        self.mcn_act = QAction("McNemar Test", self)
        self.mcn_act.triggered.connect(self._mcnemar)


        self.onesample_act = QAction("One-sample", self)
        self.onesample_act.triggered.connect(self.oneSample)

        self.twosample_act = QAction("Two-sample", self)
        self.twosample_act.triggered.connect(self.twoSample)

        self.paired_act = QAction("Paired", self)
        self.paired_act.triggered.connect(self.paired)

        self.anova_act = QAction("One-way ANOVA", self)
        self.anova_act.triggered.connect(self.anova)

        self.slreg_act = QAction("Simple Linear Regression", self)
        self.slreg_act.triggered.connect(self.slreg)

        # Create action for about menu
        self.about_act = QAction('About', self)
        self.about_act.triggered.connect(self.aboutInfo)

        # Create menubar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(self.clear_act)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)

        # Create descriptives menu and add actions
        des_menu = menu_bar.addMenu("Descriptives")
        des_menu.addAction(self.freq_act)
        des_menu.addSeparator()
        des_submenu = des_menu.addMenu("Summary Statistics")
        des_submenu.addActions([self.ungroupedData_act, self.groupedData_act])
        
        # Create probability menu and add actions
        prob_menu = menu_bar.addMenu("Probability")
        prob_menu.addAction(self.bayes_act)
        prob_menu.addSeparator()
        prob_menu.addAction(self.binomial_act)
        prob_menu.addSeparator()
        prob_menu.addAction(self.poisson_act)
        prob_menu.addSeparator()
        prob_menu.addAction(self.normal_act)
        

        # Create bivariate menu and add actions
        bvr_menu = menu_bar.addMenu("Statistical Tests")
        bvr_menu.addAction(self.chisq_act)
        bvr_menu.addSeparator()
        bvr_menu.addAction(self.mcn_act)
        bvr_menu.addSeparator()
        t_test = bvr_menu.addMenu("T-test")
        t_test.addActions([self.onesample_act, self.twosample_act, self.paired_act])
        bvr_menu.addSeparator()
        bvr_menu.addAction(self.anova_act)
        bvr_menu.addSeparator()
        bvr_menu.addAction(self.correl_act)
        bvr_menu.addSeparator()
        bvr_menu.addAction(self.slreg_act)

        # Create about menu and add action
        abt_menu = menu_bar.addMenu("About")
        abt_menu.addAction(self.about_act)


        

    def clear(self):
        answer = QMessageBox.question(self, "Clear Output", 
            "Do you want to clear the output?", QMessageBox.No | QMessageBox.Yes,
            QMessageBox.Yes)
        if answer == QMessageBox.Yes:
            self.doc.clear()
        else:
            pass

    

    def quit(self):
        self.close()

    
    def frequency(self):
        self.freqgui = FreqGui()
        self.freqgui.show()
        OK_btn = self.freqgui.OK_btn
        self.run_freq = self.freqgui.run_freq
        OK_btn.clicked.connect(self.display_freq)
        

    def display_freq(self):
        self.doc.setText("")
        res = self.run_freq()

        if isinstance(res, pandas.core.frame.DataFrame):
            result = tabulate(res, headers = "keys", tablefmt= "psql", showindex= False, 
                floatfmt = ("", "", ".2f"))
            self.doc.setText(result)

        else:
            warning = res
            self.doc.setText(warning)
        
       

    def ungroupedSumStat(self):
        self.ugsumgui = UgSumGui()
        self.ugsumgui.show()
        self.run_descriptive1 = self.ugsumgui.run_descriptive1
        OK_btn = self.ugsumgui.OK_btn
        OK_btn.clicked.connect(self.display_descriptive1)
        

    
    def display_descriptive1(self):
        self.doc.setText("")
        res = self.run_descriptive1()

        if isinstance(res, tuple):
            df, _mode, var = res
            table = tabulate(df, headers = "keys", tablefmt= "psql", showindex= False)
            header = f"Summary statistics for {var}:\n"
            self.doc.setText(header)
            self.doc.append(table)
            self.doc.append(_mode)

        else:
            warning = res
            self.doc.setText(warning)
         
        
    def grouped(self):
        self.gsumgui = GSumGui()
        self.gsumgui.show()
        self.run_descriptive2 = self.gsumgui.run_descriptive2
        OK_btn = self.gsumgui.OK_btn
        OK_btn.clicked.connect(self.display_descriptive2)
        

    def display_descriptive2(self):
        self.doc.setText("")
        res = self.run_descriptive2()

        if isinstance(res, tuple):
            df, _mode, var = res
            table = tabulate(df, headers = "keys", tablefmt= "psql", showindex= False)
            header = f"Summary statistics for {var}:\n"
            self.doc.setText(header)
            self.doc.append(table)
            self.doc.append(_mode)

        else:
            warning = res
            self.doc.setText(warning)
        
        
        
    def bayesian(self):
        self.bayesgui = BayesGui()
        self.bayesgui.show()
        self.run_bayes = self.bayesgui.run_bayes
        OK_btn = self.bayesgui.OK_btn
        OK_btn.clicked.connect(self.display_bayes)
        


    def display_bayes(self):
        self.doc.setText("")
        result = self.run_bayes()
        self.doc.setText(result)

    def _binomial(self):
        self.binomialgui = BinomialGui()
        self.binomialgui.show()
        self.run_binomial = self.binomialgui.run_binomial
        OK_btn = self.binomialgui.OK_btn
        OK_btn.clicked.connect(self.display_binomial)
        

    def display_binomial(self):
        self.doc.setText("")
        result = self.run_binomial()
        self.doc.setText(result)

    def _poisson(self):
        self.poissongui = PoissonGui()
        self.poissongui.show()
        self.run_poisson = self.poissongui.run_poisson
        OK_btn = self.poissongui.OK_btn
        OK_btn.clicked.connect(self.display_poisson)
        

    def display_poisson(self):
        self.doc.setText("")
        result = self.run_poisson()
        self.doc.setText(result)

        
    
    def _normal(self):
        self.normalgui = NormalGui()
        self.normalgui.show()
        self.run_normal = self.normalgui.run_normal
        OK_btn = self.normalgui.OK_btn
        OK_btn.clicked.connect(self.display_normal)
        

    def display_normal(self):
        self.doc.setText("")
        result = self.run_normal()
        self.doc.setText(result)

        

    def chiSquare(self):
        self.chisqgui = ChisqGui()
        self.chisqgui.show()
        OK_btn = self.chisqgui.OK_btn
        self.run_chisq = self.chisqgui.run_chisq
        OK_btn.clicked.connect(self.display_chisq)

    def display_chisq(self):
        self.doc.setText("")
        result = self.run_chisq()
        
        if isinstance(result, tuple):
            ex_df, ex_b5, prop_ex_b5, stat_df = result

            ex_tab = tabulate(ex_df, headers = "keys", tablefmt= "psql", showindex= True)
            header1 = "Expected frequencies:\n"

            stat_tab = tabulate(stat_df, headers = "keys", tablefmt= "psql", showindex= True)
            header2 = "Chi-Square Tests:\n"
            footer = "\u03B1 = 0.05"

            self.doc.setText(header1)
            self.doc.append(ex_tab)
            self.doc.append(f"Number of cells with expected frequency below 5: {ex_b5}({prop_ex_b5}%)\n\n")

            self.doc.append(header2)
            self.doc.append(stat_tab)
            self.doc.append(footer)


        else: 
            warning = result
            self.doc.setText(warning)

    def _mcnemar(self):
        self.mcnemargui = McNemarGui()
        self.mcnemargui.show()
        self.run_mcnemar = self.mcnemargui.run_mcnemar
        OK_btn = self.mcnemargui.OK_btn

        OK_btn.clicked.connect(self.display_mcnemar)


    def display_mcnemar(self):
        self.doc.setText("")
        res = self.run_mcnemar()

        if isinstance(res, pandas.core.frame.DataFrame):
            result = tabulate(res, headers = "keys", tablefmt= "psql", showindex= True)
            header = "McNemar Test:\n"
            footer = "\u03B1 = 0.05"
            self.doc.setText(header)
            self.doc.append(result)
            self.doc.append(footer)

        else:
            warning = res
            self.doc.setText(warning)

    def oneSample(self):
        self.onesampletgui = OneSampTGui()
        self.onesampletgui.show()
        self.run_onesampttest = self.onesampletgui.run_onesampttest
        OK_btn = self.onesampletgui.OK_btn
        OK_btn.clicked.connect(self.display_onesampttest)


    def display_onesampttest(self):
        self.doc.setText("")
        res = self.run_onesampttest()

        if isinstance(res, pandas.core.frame.DataFrame):
            result = tabulate(res, headers = "keys", tablefmt= "psql", showindex= True)
            header = "One-Sample T-Test:\n"
            footer = "\u03B1 = 0.05 (two-sided)"
            self.doc.setText(header)
            self.doc.append(result)
            self.doc.append(footer)
        else:
            warning = res
            self.doc.setText(warning)




    def twoSample(self):
        self.twosampletgui = TwoSampTGui()
        self.twosampletgui.show()
        self.run_twosampttest = self.twosampletgui.run_twosampttest
        OK_btn = self.twosampletgui.OK_btn
        OK_btn.clicked.connect(self.display_twosampttest)


    def display_twosampttest(self):
        self.doc.setText("")
        res = self.run_twosampttest()

        if isinstance(res, pandas.core.frame.DataFrame):
            result = tabulate(res, headers = "keys", tablefmt= "psql", showindex= True)
            header = "Two-Sample T-Test:\n"
            footer1 = "\u03B1 = 0.05 (two-sided)"
            footer2 = "Equality of variance assummed"
            self.doc.setText(header)
            self.doc.append(result)
            self.doc.append(footer1)
            self.doc.append(footer2)

        else:
            warning = res
            self.doc.setText(warning)


    
    def paired(self):
        self.pairedttestgui = PairedTGui()
        self.pairedttestgui.show()
        self.run_pairedttest = self.pairedttestgui.run_pairedttest
        OK_btn = self.pairedttestgui.OK_btn
        OK_btn.clicked.connect(self.display_pairedttest)

    def display_pairedttest(self):
        self.doc.setText("")
        res = self.run_pairedttest()

        if isinstance(res, pandas.core.frame.DataFrame):
            result = tabulate(res, headers = "keys", tablefmt= "psql", showindex= True)
            header = "Paired T-Test:\n"
            footer1 = "\u03B1 = 0.05 (two-sided)"
            self.doc.setText(header)
            self.doc.append(result)
            self.doc.append(footer1)
        else:
            warning = res
            self.doc.setText(warning)


    def anova(self):
        self.anovagui = ANOVAGui()
        self.anovagui.show()
        self.run_anova = self.anovagui.run_anova
        OK_btn = self.anovagui.OK_btn
        OK_btn.clicked.connect(self.display_anova)

    def display_anova(self):
        self.doc.setText("")
        res = self.run_anova()

        if isinstance(res, pandas.core.frame.DataFrame):
            anova_df = res
            anova_tab = tabulate(anova_df, headers = "keys", tablefmt= "psql", showindex= False)
            header = "One-way Analysis of Variance:\n"
            footer1 = "\u03B1 = 0.05"
            footer2 = "Equality of variance assummed"
            self.doc.setText(header)
            self.doc.append(anova_tab)
            self.doc.append(footer1)
            self.doc.append(footer2)
        else:
            warning = res
            self.doc.setText(warning)


    
    def correlation(self):
        self.correlgui = CorrelGui()
        self.correlgui.show()
        self.run_correlation = self.correlgui.run_correlation
        OK_btn = self.correlgui.OK_btn
        OK_btn.clicked.connect(self.display_correlation)

    
    def display_correlation(self):
        self.doc.setText("")
        res = self.run_correlation()

        if isinstance(res, tuple):    
            df, N_samp = res
            correl_tab = tabulate(df, headers = "keys", tablefmt= "psql", showindex= True, floatfmt = ".4f")
            header = "Correlation:\n"

            footer1 = f"N = {N_samp}"
            footer2 = "\u03B1 = 0.05 (two-sided)"

            self.doc.setText(header)
            self.doc.append(correl_tab)
            self.doc.append(footer1)
            self.doc.append(footer2)
        else: 
            warning = res
            self.doc.setText(warning)


    
    def slreg(self):
        self.slreggui = SLRegGui()
        self.slreggui.show()
        self.run_slreg= self.slreggui.run_slreg
        OK_btn = self.slreggui.OK_btn
        OK_btn.clicked.connect(self.display_slreg)

    def display_slreg(self):
        self.doc.setText("")
        res = self.run_slreg()

        if isinstance(res, tuple):            
            slr_df, Xn, rsq, f_val, f_p = res
            coef_tab = tabulate(slr_df, headers = "keys", tablefmt= "psql", showindex= True, 
                floatfmt = (".4f", ".4f", ".4f",".4f" ,".6f"))
            header = "Simple Linear Regression:\n"

            footer1 = f"N = {Xn}; R-squared = {rsq:.4f}"
            footer2 = f"F-statistic = {f_val:.4f} on 1 & {Xn-2} df; P-value = {f_p:.6f}"

            self.doc.setText(header)
            self.doc.append(coef_tab)
            self.doc.append(footer1)
            self.doc.append(footer2)
        else: 
            warning = res
            self.doc.setText(warning)


    def aboutInfo(self):
        self.aboutgui = AboutGui()
        self.aboutgui.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = App()
    sys.exit(app.exec())
    