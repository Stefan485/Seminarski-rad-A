from array import array
from ast import Try
from encodings import utf_8
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPlainTextEdit
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
        self.doktorLoginNazad.clicked.connect(self.nazad)
        #sakrivena sifra
        self.sifra_doktor_login.setEchoMode(QtWidgets.QLineEdit.Password)

        self.show()
        
    def nazad(self):
        self.window =UI_login()
        self.close()
 
    def doktor_ulogovan(self):

        slova = ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "š", "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Š", ":"]
        dvotacka = [":"]

        doktor_id = self.id_doktor_login.text()
        doktor_sifra = self.sifra_doktor_login.text()
        termini = open("termini.txt", "r", encoding="utf-8")
        doktor = open("doktori.txt", "r", encoding="utf-8")
        
        if any(element in doktor_id for element in slova):
            self.greska_doktor_log.setText("Uneli ste pogresan karakter u ID.")

        elif any(element in doktor_sifra  for element in dvotacka) or any(element in doktor_id for element in slova):
            self.greska_doktor_log.setText("Uneli ste neodgovarajuce karaktere")

        else:
            test = doktor.read()
            if test !="":
                doktor.seek(0,0)
                for line in doktor:
                    #deljenje linije ucitane iz fajla
                    ID, ime, sifra, prostor  = line.split(":", 3)
                    #provera da li su parametri tacni
                    if doktor_id == ID and doktor_sifra == sifra:                      
                    
                        self.window = UI_doktor()
                        self.window.imeDoktora.setText(doktor_id +":" + ime)
                        pacijenti = open("pacijenti.txt", "r", encoding="utf-8")

                        lista_za_doktora = []
                        for line in termini:
                            pacijent_broj, doktor_broj, ostalo = line.split(":", 2)
                            if doktor_id == doktor_broj:
                                lista_za_doktora.append(pacijent_broj)

                        lista_pacijenata = [] 
                        for line in pacijenti:
                                broj, pacijent, nebitno = line.split(":", 2)
                                if broj in lista_za_doktora:  
                                    self.window.doktorCombo.addItem(broj +":"+ pacijent)
                                    lista_pacijenata.append(broj)

                        if lista_pacijenata == []:
                            self.window.doktorCombo.addItem("Nemate pacijenata.")

                        
                        pacijenti.close()
                        doktor.close()
                        self.close()
                        break
                    
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
        self.doktorRegistracijaNazad.clicked.connect(self.nazad)
        #sakrivena sifra
        self.sifra_doktor_reg.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.show()   

    def nazad(self):
        self.window = UI_doktor_login()
        self.close()
        
    def doktor_registracija(self):

        slova = ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "š", "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Š", ":"]
        dvotacka = [":"]
        brojevi = ["0", "1", "2", "3","4","5","6","7","8","9"]
        doktor_id = self.id_doktor_reg.text()
        doktor_ime = self.ime_doktor_reg.text()
        doktor_sifra = self.sifra_doktor_reg.text()
        
        if len(doktor_id) == 0 or len(doktor_ime) == 0 or len(doktor_sifra) == 0:
            self.greska_doktor_reg.setText("Popunite sva polja")

        elif len(doktor_id) >6:
            self.greska_doktor_reg.setText("Uneli ste previse karaktera za ID (>6)")          

        elif any(element in doktor_id for element in dvotacka) or any(element in doktor_sifra for element in dvotacka) or any(element in doktor_ime for element in dvotacka) :
            self.greska_doktor_reg.setText("Ne mozete upotrebiti:" + " :")

        elif any(element in doktor_id for element in slova):
            self.greska_doktor_reg.setText("Ne mozete upotrebiti:" + " :")  

        elif any(element in doktor_ime for element in brojevi):
            self.greska_doktor_reg.setText("Ne mozete koristiti brojeve u imenu.")  
        
        else:
            termini = open("termini.txt", "r", encoding="utf-8")
            doktor = open("doktori.txt", "r", encoding="utf-8")
            
            doktor_provera_lista = []
            for line in doktor:
                doktor_id_provera, ostalo = line.split(":", 1)
                doktor_provera_lista.append(doktor_id_provera)

            if doktor_id in doktor_provera_lista:  
                self.greska_doktor_reg.setText("Ovaj ID je zauzet")
                    
            else:
                #podesiti promenu imena doktora
                doktor.close()
                doktor = open("doktori.txt", "a", encoding="utf-8")
                doktor.write(doktor_id +":" + doktor_ime +":"+ doktor_sifra + ":" + "\n")
                doktor.close()

                self.window = UI_doktor()
                self.window.imeDoktora.setText(doktor_id +":" + doktor_ime)
                pacijenti = open("pacijenti.txt", "r", encoding="utf-8")

                lista_za_doktora = []
                for line in termini:
                    pacijent_broj, doktor_broj, ostalo = line.split(":", 2)
                    if doktor_id == doktor_broj:
                        lista_za_doktora.append(pacijent_broj)

                lista_pacijenata = []
                for line in pacijenti:
                    pacijent_id, pacijent_ime, pacijent_sifra = line.split(":", 2)
                    if pacijent_id in lista_za_doktora:
                        self.window.doktorCombo.addItem(pacijent_id +":"+ pacijent_ime)
                        lista_pacijenata.append(pacijent_id)

                if lista_pacijenata == []:
                    self.window.doktorCombo.addItem("Nemate pacijenata.")

                termini.close()
                pacijenti.close()
                self.close()
        
#doktorov interfejs
class UI_doktor(QMainWindow):
    
    def __init__(self):
        super(UI_doktor, self).__init__()
        
        loadUi("Interfejs/doktor.ui", self)
        
        self.podaci_pacijenta = self.findChild(QPlainTextEdit, "podaciPacijenata2")
        self.doktor_pocetni.clicked.connect(self.povratak_doktor)
        self.doktorSacuvaj.clicked.connect(self.sacuvaj)
        self.doktorUcitaj.clicked.connect(self.ucitaj)
        
        self.show() 

    def ucitaj(self):

        pacijent = self.doktorCombo.currentText()
        if pacijent != "Nemate pacijenata.":
            id_pacijenta, ime_pacijenta = pacijent.split(":", 1)
            ime_fajla = "pacijent/" + id_pacijenta + ".txt"

            try:
                fajl_pacijent = open(ime_fajla, "r", encoding="utf-8")
                self.podaciPacijenata.setPlainText(fajl_pacijent.read())
        
            except:
                fajl_pacijent = open(ime_fajla, "x", encoding="utf-8")
                fajl_pacijent.close()

    def sacuvaj(self):
        pacijent = self.doktorCombo.currentText()
        if pacijent != "Nemate pacijenata.":
            id_pacijenta, ime_pacijenta = pacijent.split(":", 1)
            ime_fajla = "pacijent/" + id_pacijenta + ".txt"

            fajl_pacijent = open(ime_fajla, "w", encoding="utf-8")
            fajl_pacijent.write(self.podaciPacijenata.toPlainText())
            fajl_pacijent.close()

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
        self.pacijentLoginNazad.clicked.connect(self.nazad)
        #skrivena sifra
        self.sifra_pacijent_login.setEchoMode(QtWidgets.QLineEdit.Password)

        self.show()
            
    def nazad(self):
        self.window = UI_login()
        self.close()

    def pacijent_ulogovan(self):

        slova = ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "š", "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Š", ":"]
        dvotacka = [":"]
    
        pacijent_sifra = self.sifra_pacijent_login.text()
        pacijent_id = self.id_pacijent_login.text()
        pacijent = open("pacijenti.txt", "r", encoding="utf-8")
        fajl_doktori = open("doktori.txt", "r", encoding="utf-8")
        termini = open("termini.txt", "r", encoding="utf-8")

        if len(pacijent_sifra) == 0 or len(pacijent_id) == 0:
            self.pacijent_login_greska.setText("Popunite sva polja")

        elif any(element in pacijent_sifra  for element in dvotacka) or any(element in pacijent_id for element in slova):
            self.pacijent_login_greska.setText("Uneli ste neodgovarajuće karaktere")
                
        else:
            test = termini.read()
            if test != "":
                termini.seek(0,0)
                for line in pacijent:
                    ID, ime, sifra, prostor  = line.split(":", 3)
                        
                    if pacijent_id == ID and pacijent_sifra == sifra:
            
                        lista_doktora = []
                        lista_doktora_sa_imenima = []
                        niz_termina = array("i", [])

                        for line in fajl_doktori:
                            id_doktora, ime_doktora, sifra_doktora, prazan = line.split(":", 3)
                            lista_doktora.append(id_doktora)
                            lista_doktora_sa_imenima.append(id_doktora + "," + ime_doktora)

                        fajl_doktori.seek(0,0)
                        for line in fajl_doktori:
                            niz_termina.append(int(0))       
                    
                        test = termini.read()

                        if test != "":
                            termini.seek(0,0)
                            for line in termini:
                                id_pacijenta, id_dok, mesec, termin = line.split(":", 3)
                                niz_termina[lista_doktora.index(id_dok)] += 1

                        lista_termina = []
                        for i in range(len(niz_termina)):
                            lista_termina.append(str(niz_termina[i]))

                        #self.window.
                        fajl_doktori.seek(0,0)
                        self.window = UI_pacijent()
                        
                        self.window.brojPacijenata.setText("Broj pacijenata kod svih doktora:")
                        for i in range(len(lista_doktora)):
                            self.window.brojPacijenata.append(lista_doktora_sa_imenima[i] + ":" + lista_termina[i])

                        for line in fajl_doktori:
                            id_doktora, ime, sifra, prazan = line.split(":", 3)
                            self.window.pacijentCombo.addItem(id_doktora + ":" + ime)

                        #self.window.
                        self.window.imePacijenta.setText(pacijent_id + ":" + ime)

                        pacijent.close()
                        termini.close()
                        fajl_doktori.close()
                        self.close()
                        break

            else:
                self.pacijent_login_greska.setText("Niste registrovani")
    
    def pacijent_registrovanje(self):
        self.window = UI_pacijent_registracija()
        self.close()
    
#pacijentovo registrovanje
class UI_pacijent_registracija(QMainWindow):
    
    def __init__(self):
        super(UI_pacijent_registracija, self).__init__()
    
        loadUi("Interfejs/pacRegistracija.ui", self)

        self.pacijent_registruj.clicked.connect(self.pacijent_registrovan)
        self.pacijentRegistracijaNazad.clicked.connect(self.nazad)
        #skrivenasifra
        self.sifra_pacijent_reg.setEchoMode(QtWidgets.QLineEdit.Password)

        self.show()
    
    def nazad(self):
        self.window = UI_pacijent_login()
        self.close()

    def pacijent_registrovan(self):
        termini = open("termini.txt", "r", encoding="utf-8")

        slova = ["a", "b", "v", "g", "d", "đ", "e", "ž", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "ć", "u", "f", "h", "c", "š", "A", "B", "V", "G", "D", "Đ", "E", "Ž", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "Ć", "U", "F", "H", "C", "Š", ":"]
        dvotacka = [":"]
        brojevi = ["0", "1", "2", "3","4","5","6","7","8","9"]
        
        pacijent_ime = self.ime_pacijent_reg.text()
        pacijent_sifra = self.sifra_pacijent_reg.text()
        pacijent_id = self.id_pacijent_reg.text()
            
        if len(pacijent_ime) == 0 or len(pacijent_sifra) == 0 or len(pacijent_id) == 0:
            self.pacijent_greska_reg.setText("Popunite sva polja")

        elif any(element in pacijent_id for element in dvotacka) or any(element in pacijent_sifra for element in dvotacka) or any(element in pacijent_ime for element in dvotacka):
            self.pacijent_greska_reg.setText("Ne mozete upotrebiti:" + " :")

        elif len(pacijent_id) >6:
            self.pacijent_greska_reg.setText("Uneli ste previse karaktera za ID (>6)")  
        
        elif any(element in pacijent_id for element in slova):
            self.pacijent_greska_reg.setText("Ne mozete upotrebiti:" + " :")  

        elif any(element in pacijent_ime for element in brojevi):
            self.pacijent_greska_reg.setText("Ne mozete koristiti brojeve u imenu.")  
                
        else:
            pacijent = open("pacijenti.txt", "r", encoding="utf-8")
          
            pacijent_provera_lista = []
            for line in pacijent:
                pacijentov_id, ostalo = line.split(":", 1)
                pacijent_provera_lista.append(pacijentov_id)

            if pacijent_id in pacijent_provera_lista:
                self.pacijent_greska_reg.setText("Ovaj ID je već registrovan")
                
            else:
                pacijent.close()
                pacijent = open("pacijenti.txt", "a", encoding="utf-8")
                pacijent.write(pacijent_id +":" + pacijent_ime + ":" + pacijent_sifra + ":" +"\n")
                pacijent.close()

                
                fajl_doktori = open("doktori.txt", "r", encoding="utf-8")
                lista_doktora = []
                lista_doktora_sa_imenima = []
                niz_termina = array("i", [])

                for line in fajl_doktori:
                    id_doktora, ime_doktora, sifra_doktora, prazan = line.split(":", 3)
                    lista_doktora.append(id_doktora)
                    lista_doktora_sa_imenima.append(id_doktora + "," + ime_doktora)

                fajl_doktori.seek(0,0)

                for line in fajl_doktori:
                    niz_termina.append(int(0))       

                test = termini.read()
                if test != "":
                    termini.seek(0,0)
                    for line in termini:
                        id_pacijenta, id_dok, mesec, termin = line.split(":", 3)
                        niz_termina[lista_doktora.index(id_dok)] += 1

                lista_termina = []
                for i in range(len(niz_termina)):
                    lista_termina.append(str(niz_termina[i]))

               # self.window.
                fajl_doktori.seek(0,0)
                self.window = UI_pacijent()
                
                for i in range(len(lista_doktora)):
                    self.window.brojPacijenata.append(lista_doktora_sa_imenima[i] + ":" + lista_termina[i])


                for line in fajl_doktori:
                    id_doktora, ime, sifra, prazan = line.split(":", 3)
                    self.window.pacijentCombo.addItem(id_doktora + ":" + ime)

                self.window.imePacijenta.setText(pacijent_id + ":" + pacijent_ime)

                termini.close()
                fajl_doktori.close()
                self.close()
        
#pacijentov interfejs
class UI_pacijent(QMainWindow):
    
    def __init__(self):
        super(UI_pacijent, self).__init__()
        
        loadUi("Interfejs/pacijent.ui", self)

        self.pacijent_pogresan = self.findChild(QLabel, "pacijent_greska")

        self.pacijentZakazi.clicked.connect(self.zakazi)

        self.pacijent_pocetni.clicked.connect(self.povratak_pacijent)
        
        self.pacijentPrikazi.clicked.connect(self.prikaziGrafik)

        self.prikazOsvezi.clicked.connect(self.osvezi)

        self.pacijentTermini.clicked.connect(self.termin)

        self.pacijentPodaci.clicked.connect(self.podaci)

        self.show()
        
    def povratak_pacijent(self):
        self.window = UI_login()
        self.close()

    def zakazi(self):
        termini = open("termini.txt", "r", encoding="utf-8")
        
        mesec = self.zakazivanje_mesec.currentText()
        dan = self.zakazivanje_dan.currentText()
        sat = self.zakazivanje_sat.currentText()

        labela_ime_pacijenta = self.imePacijenta.text()
        id_pacijenta, ime_pacijenta = labela_ime_pacijenta.split(":", 1)

        zakazan = mesec + ":" + dan + ":" + sat + ":"

        doktor = self.pacijentCombo.currentText()
        id_doktora, ime_doktora = doktor.split(":", 1)

        trideset = ["APRIL", "JUN", "SEPTEMBAR", "NOVEMBAR"]
        trideset_jedan = ["JANUAR", "MART", "MAJ", "JUL", "AVGUST", "OKTOBAR", "DECEMBAR"]

        if mesec == "FEBRUAR" and dan > "28": 
            self.pacijent_pogresan.setText("Termin ne postoji")


        elif mesec in trideset and dan == "31":
            self.pacijent_pogresan.setText("Termin ne postoji")

        else:
            lista_termina = []

            test = termini.read()
            if test != "":
                termini.seek(0,0)
                for line in termini:
                    pacijent_id, doktor_id, mesec, dan, sat, minut, ostatak  = line.split(":", 6)
                    lista_termina.append(doktor_id +":"+ mesec +":"+ dan + ":" + sat + ":" + minut + ":")
                
            provera = id_doktora + ":" + zakazan
            
            if provera in lista_termina:
                termini.close()
                self.pacijent_pogresan.setText("Termin je zauzet.")

            else:
                termini.close()
                termini = open("termini.txt", "a", encoding="utf-8")
                termini.write(id_pacijenta + ":" + id_doktora + ":" + zakazan + "\n")
                termini.close()
                self.pacijent_pogresan.setText("Zakazali ste termin")

    def osvezi(self):
        fajl_doktori = open("doktori.txt", "r", encoding="utf-8")
        lista_doktora = []
        lista_doktora_sa_imenima = []
        niz_termina = array("i", [])

        for line in fajl_doktori:
            id_doktora, ime_doktora, sifra_doktora, prazan = line.split(":", 3)
            lista_doktora.append(id_doktora)
            lista_doktora_sa_imenima.append(id_doktora + "," + ime_doktora)

        fajl_doktori.seek(0,0)
        for line in fajl_doktori:
            niz_termina.append(int(0))

        termini = open("termini.txt", "r", encoding="utf-8")

        for line in termini:
            id_pacijenta, id_dok, mesec, termin = line.split(":", 3)
            niz_termina[lista_doktora.index(id_dok)] += 1

        lista_termina = []
        for i in range(len(niz_termina)):
            lista_termina.append(str(niz_termina[i]))

        self.brojPacijenata.setText("Broj pacijenata kod svih doktora.")
        for i in range(len(lista_doktora)):
            self.brojPacijenata.append(lista_doktora_sa_imenima[i] + ":" + lista_termina[i])

        termini.close()
        fajl_doktori.close()

    def prikaziGrafik(self):
        termini = open("termini.txt", "r", encoding="utf-8")
        fajl_doktori = open("doktori.txt", "r", encoding="utf-8")
        lista_doktora = []
        lista_doktora_sa_imenima = []
        niz_termina = array("i", [])
        
        for line in fajl_doktori:
            id_doktora, ime_doktora, sifra_doktora, prazan = line.split(":", 3)
            lista_doktora.append(id_doktora)
            lista_doktora_sa_imenima.append(id_doktora + "," + ime_doktora)

        fajl_doktori.seek(0,0)
        for line in fajl_doktori:
            niz_termina.append(int(0))       
       
        test = termini.read()
        if test != "":
            termini.seek(0,0)
            for line in termini:
                id_pacijenta, id_dok, mesec, termin = line.split(":", 3)
                niz_termina[lista_doktora.index(id_dok)] += 1

        lista_termina = []
        for i in range(len(niz_termina)):
            lista_termina.append(str(niz_termina[i]))

        self.brojPacijenata.setText("Broj pacijenata kod svih doktora:")
        for i in range(len(lista_doktora)):
            self.brojPacijenata.append(lista_doktora_sa_imenima[i] + ":" + lista_termina[i])      
        
        plt.bar(lista_doktora, niz_termina)
        plt.xlabel("Doktori")
        plt.xticks(rotation = 90)
        plt.ylabel("Broj pacijenata")
        plt.ylim(ymin = 0, ymax = max(niz_termina))
        plt.tight_layout()
        plt.show()
        termini.close()
        fajl_doktori.close()

    def termin(self):

        termini = open("termini.txt", "r", encoding="utf-8")
        
        lista_termina = []

        pacijent = self.imePacijenta.text()

        pacijent_id, pacijent_ime = pacijent.split(":", 1)


        self.brojPacijenata.setText("Vaši zakazani termini:")
        
        test = termini.read()
        if test != "":
            termini.seek(0,0)
            for line in termini:
                id_pacijent, id_doktor, zakazan_termin = line.split(":", 2)

                if pacijent_id == id_pacijent:
                    lista_termina.append(pacijent_id)
                    self.brojPacijenata.append(zakazan_termin + " kod doktora:" + id_doktor  + "\n")

            if lista_termina == []:
                self.brojPacijenata.append("Nemate zakazan termin.")

            termini.close()

    def podaci(self):
        labela = self.imePacijenta.text()
        pacijent_id, pacijent_ime = labela.split(":", 1)

        fajl = "pacijent/" + pacijent_id + ".txt"
        try:
            fajl_pacijenta = open(fajl, "x", encoding="utf-8")
            self.brojPacijenata.setText("")
            self.brojPacijenata.setText("Nema unetih podataka")
            fajl_pacijenta.close()

        except:
            fajl_pacijenta = open(fajl, "r", encoding="utf-8")
            ispis = fajl_pacijenta.read()
            self.brojPacijenata.setText("")
            self.brojPacijenata.append(ispis)
            fajl_pacijenta.close()

#inicijalizacija aplikacije
app = QApplication(sys.argv)
UIWindow = UI_login()
app.exec_()