from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QLabel
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import sys

#pocetni interfejs
class UI_login(QMainWindow):
    def __init__(self):
        super(UI_login, self).__init__()

        #ucitavanje UI
        loadUi("Interfejs/login.ui", self)

        self.dugmePocetniDoktor.clicked.connect(self.open_doktor_login)
        self.dugmePocetniPacijent.clicked.connect(self.open_pacijent_login)
 
        #prikazivanje intefejsa
        self.show()
        
    def open_doktor_login(self):
        self.window = UI_doktor_login()
        self.close()
        
    def open_pacijent_login(self):
        self.window = UI_pacijent_login()
        self.close()
        
        
 #klasa za ulogovanje doktora       
class UI_doktor_login(QMainWindow):
    
    def __init__(self):  
        super(UI_doktor_login, self).__init__()
        
        loadUi("Interfejs/dokLogin.ui", self)
        
        self.doktor_login.clicked.connect(self.doktor_ulogovan)
        self.doktor_registruj.clicked.connect(self.doktor_registrovanje)


        self.show()
        
 
    def doktor_ulogovan(self):
        
        
        doktor_id = self.id_doktor_login.text()
        doktor_sifra = self.sifra_doktor_login.text()
        
        doktor = open("doktori.txt", "r")
        
        for line in doktor:
            ID, ime, sifra, pacijent  = line.split(":", 3)
            if doktor_id == ID and doktor_sifra == sifra:                      
                self.window = UI_doktor()
                self.window.ime_doktora.setText(ime)
                print(self.window.ime_doktora.text() + "ime u petlji")
                doktor.close()
                self.close()
                break
                
            
        
        print(doktor_id, doktor_sifra, ID, sifra, ime, pacijent)
        self.greska_doktor_log.setText("Niste registrovani")
                
 
        
    def doktor_registrovanje(self):
        self.window = UI_doktor_registracija()
        self.close()
        
#klasa za registrovanje doktora
class UI_doktor_registracija(QMainWindow):
    
    def __init__(self):
        super(UI_doktor_registracija, self).__init__()
    
        loadUi("Interfejs/dokRegistracija.ui", self)
        
        self.doktor_registruj_reg.clicked.connect(self.doktor_registracija)
        #self.sifra_doktor_reg.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.show()
        
        
    def doktor_registracija(self):
        
        doktor_id = self.id_doktor_reg.text()
        doktor_ime = self.ime_doktor_reg.text()
        doktor_sifra = self.sifra_doktor_reg.text()
        
        if len(doktor_id) == 0 or len(doktor_ime) == 0 or len(doktor_sifra) == 0:
            self.greska_doktor_reg.setText("Popunite sva polja")

        else:
            
            doktor = open("doktori.txt", "r")
            doktor_sadrzaj = doktor.read()
            
            
            if doktor_id in doktor_sadrzaj:  
                self.greska_doktor_reg.setText("Ovaj ID je zauzet")
                    
                
            else:
                #podesiti promenu imena doktora
                doktor.close()
                doktor = open("doktori.txt", "a")
                doktor.write(doktor_id +":" + doktor_ime +":"+ doktor_sifra + "\n")
                doktor.close()

                self.window = UI_doktor()
                self.close()
        
#doktorov interfejs
class UI_doktor(QMainWindow):
    
    def __init__(self):
        super(UI_doktor, self).__init__()
        
        loadUi("Interfejs/doktor.ui", self)
        
        self.doktor_pocetni.clicked.connect(self.povratak_doktor)
        self.ime_doktora = self.findChild(QLabel, "imeDoktora")

        self.show()
        
    def povratak_doktor(self): 
        self.window = UI_login()
        self.close()
    
#klasa za pacijentovo ulogovanje
class UI_pacijent_login(QMainWindow):
    
    def __init__(self):
        super(UI_pacijent_login, self).__init__()
        
        loadUi("Interfejs/pacLogin.ui", self)
        
        self.pacijent_login.clicked.connect(self.pacijent_ulogovan)
        self.pacijent_registruj.clicked.connect(self.pacijent_registrovanje)
        
        
        self.show()
        
        
    def pacijent_ulogovan(self):
        
        #logovanje try i except kao i za doktora
        self.window = UI_pacijent()
        self.close()
        
    
    def pacijent_registrovanje(self):
        self.window = UI_pacijent_registracija()
        self.close()
    
#pacijentovo registrovanje
class UI_pacijent_registracija(QMainWindow):
    
    def __init__(self):
        super(UI_pacijent_registracija, self).__init__()
    
        loadUi("Interfejs/pacRegistracija.ui", self)
    
        self.pacijent_registruj.clicked.connect(self.pacijent_registrovan)
        self.show()
    
    def pacijent_registrovan(self):
        
        pacijent_ime = self.ime_pacijent_reg.text()
        pacijent_sifra = self.sifra_pacijent_reg.text()
        pacijent_id = self.id_pacijent_reg.text()
            
        if len(pacijent_ime) == 0 or len(pacijent_sifra) == 0 or len(pacijent_id) == 0:
            self.pacijent_greska_reg.setText("Popunite sva polja")
                
        else:
            pacijent = open("pacijenti.txt", "r")
            pacijent_podaci = pacijent.read()
        
            if pacijent_id in pacijent_podaci:
                self.pacijent_greska_reg.setText("Ovaj ID je već registrovan")
                
            else:
                pacijent.close()
                pacijent = open("pacijenti.txt", "a")
                pacijent.write(pacijent_id +":" + pacijent_ime + ":" + pacijent_sifra + "\n")
                pacijent.close()
                self.window = UI_pacijent()
                self.window.ime_pacijenta.setText(pacijent_ime)
                self.close()
        
#pacijentov interfejs
class UI_pacijent(QMainWindow):
    
    def __init__(self):
        super(UI_pacijent, self).__init__()
        
        loadUi("Interfejs/pacijent.ui", self)
              
        print(self.ime_pacijenta.text())
       
        self.pacijent_pocetni.clicked.connect(self.povratak_pacijent)
        
        self.show()
        
    def povratak_pacijent(self):
        self.window = UI_login()
        self.close()


#inicijalizacija aplikacije
app = QApplication(sys.argv)
UIWindow = UI_login()
app.exec_()