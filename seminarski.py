from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QWindow
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from PyQt5 import uic
import sys

from PyQt5.uic.uiparser import WidgetStack

class UI_login(QMainWindow):
    def __init__(self):
        super(UI_login, self).__init__()

        #ucitavanje UI
        uic.loadUi("./login.ui", self)

        self.labela = self.findChild(QLabel, "loginLabel")
        self.doktorLogin = self.findChild(QPushButton, "dugmePocetniDoktor")


        self.doktorLogin.clicked.connect(self.openDoktorLogin)

        #prikazivanje aplikacije
        self.show()

    def openDoktorLogin(self):
      self.window = QtWidgets.QMainWindow()
      self.window = uic.loadUi("./dokLogin.ui", self)
      self.window.show()


      UI_dokLogin.nekitamo(self)
      UI_dokLogin.moduli(self)


      


class UI_dokLogin(QMainWindow):
    def __init__(self):  
      super(UI_dokLogin, self)

    def moduli(self):
      UI_dokLogin.doktorLabela = self.findChild(QLabel, "doktorLoginLabel")
      UI_dokLogin.doktorLog = self.findChild(QPushButton, "doktorLogin")

      UI_dokLogin.doktorLog.clicked.connect(UI_dokLogin.nekitamo)  

    def nekitamo(self):
      UI_dokLogin.doktorLabela.setText("Brrrrrrrr")



     


   


#inicijalizacija aplikacije
app = QApplication(sys.argv)
UIWindow = UI_login()
app.exec_()