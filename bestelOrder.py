﻿from login import hoofdMenu
import sys, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp, QSize
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator, QColor, QImage
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout, QPushButton, QLineEdit,\
     QWidget, QMessageBox, QTableView, QVBoxLayout, QComboBox, QStyledItemDelegate,\
     QSpinBox, QCheckBox
from sqlalchemy import (Table, Column, Integer, String, MetaData, create_engine,\
                        Float, Boolean, ForeignKey, select, insert, update, delete, and_, func)
from sqlalchemy.exc import IntegrityError

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)

def bestGelukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Betaling heeft plaatsgevonden\nBestelling wordt in behandeling genomen!')
    msg.setWindowTitle('Bestellingen')               
    msg.exec_()
    
def betMislukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Betaling is niet gelukt\nbetaling opnieuw uitvoeren!')
    msg.setWindowTitle('Betalingen')               
    msg.exec_()
    
def betGelukt():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Betaling is geslaagd!')
    msg.setWindowTitle('Betalingen')               
    msg.exec_()
  
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren a.u.b.!')
    msg.setWindowTitle('Artikelen opvragen')               
    msg.exec_()
    
def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie a.u.b.!')
    msg.setWindowTitle('Artikelen opvragen')               
    msg.exec_() 
    
def geenRegels():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Nog geen lopende bestelling aanwezig\neerst bestellen a.u.b.!')
    msg.setWindowTitle('Bestellen')               
    msg.exec_()
    
def foutPostcode():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Onjuiste postcode en / of huisnummer ingebracht\nof onjuiste combinatie van postcode en huisnummer!')
    msg.setWindowTitle('Postcode')               
    msg.exec_()
    return(False)
   
def negVoorraad(maant):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('Niet voldoende voorraad\ner is/zijn nog maar '+str(int(maant))+' st. beschikbaar\nde boeking is niet uitgevoerd!')
    msg.setWindowTitle('Voorraad onvoldoende')
    msg.exec_()
    
def foutAlert(e):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Critical)
    msg.setText('\n\nEr heeft zich een fout voorgedaan.\nGeef foutmelding door aan Systeembeheer.\nDruk op OK om programma af te sluiten!\n\nFoutmelding: '+str(e))
    msg.setWindowTitle('Systeemfout')
    msg.exec_()
    
def info():
    class Widget(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            self.setWindowTitle("Informatie bestelprocedure")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setFont(QFont("Arial", 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 3, 1, 1, Qt.AlignRight)
            
            lblinfo = QLabel('Uitleg over bestellingen')
            grid.addWidget(lblinfo, 0, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("color:rgb(45, 83, 115); font: 25pt Comic Sans MS")
        
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 0, 0)
            lblinfo = QLabel(
        '''
        Kies op het artikelscherm de rij met het gewenste artikel. 
        Klik vervolgens met de muis op het eerste veld. 
        Deze actie opent een bestelscherm.
        Op dit bestelscherm zijn de gegevens van het gekozen produkt te zien,
        zoals prijs en omschrijving en tevens een verkleinde afbeelding.
        Tevens zijn een 3 tal knoppen zichtbaar. Foto, Bestellen en Winkelwagen.
        Met Foto wordt een vergrote afbeelding van het produkt getoond.
        Voor bestellen het bestelaantal invullen en met knop "Bestellen" wordt
        het produkt aan de winkelwagen toegevoegd. De inhoud van de winkelwagen 
        is altijd met de knop winkelwagen op te vragen.
        Tevens kun je hier de aantallen nog wijzigen, met op 0 stellen wordt het
        desbetreffende produkt verwijderd. Klikken op eerste veld van betreffend
        produkt, aantal wijzigen en de knop "Aanpassen" klikken.
        Indien de selektie akkoord is, kun je onder in het scherm eventueel een 
        alternatief verzendadres opgeven. Geef hier naam, postcode en huisnummer in. 
        De straat- en plaatsnaam wordt door het systeem ingevuld.
        Indien verzendadres niet wordt ingevuld worden de goederen naar het
        factuuradres verzonden.
        
        Vervolgens druk je op de knop "Bereken gegevens".
        Hierna worden alle bedragen en overige gegevens weergegeven.
        Na het plaatsen van het vinkje voor het accepteren van de algemene
        voorwaarden wordt de betaalknop aktief en kun je verder naar afrekenen.
        De volgorde van Berekening gegevens en Akkoord algemene voorwaarden is belangrijk.\t
        Zolang betaling niet daadwerkelijk heeft plaatsgevonden, kunnen nog aanpassingen
        worden uitgevoerd. Sluit en heropen hiertoe het bestelscherm.
        De volgende betaalmethoden zijn mogelijk:
        iDeal via alle banken in Nederland.
        Creditcard via Visa, American Express of Maestro/Mastercard.
        Tevens kan voor PayPal worden gekozen of voor Afterpay. Voor Afterpay wordt
        echter een extra vergoeding berekend van Euro 2,50 voor verzekering en kosten.
        Na gelukte betaling wordt de bestelling in behandeling genomen.
        ''')
                
            grid.addWidget(lblinfo, 1, 0, 1, 4, Qt.AlignCenter)
            lblinfo.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF") 
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)  
            
            grid.addWidget(cancelBtn,  3, 0, 1, 4, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(90)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 3, 0, 1, 4, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setMinimumWidth(650)
            self.setGeometry(550, 50, 900, 150)
            
    window = Widget()
    window.exec_()
    
def refresh(m_email, self, btnStatus, e1, e2, e3, e4, e5, e6, klmail):
    metadata = MetaData() 
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float),
        Column('subtotaal', Float),
        Column('btw', Float),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    btwsel = select([params]).where(params.c.paramID == 1)
    rpbtw = con.execute(btwsel).first()
    btwperc = rpbtw[1]
    selweb = select([webbestellingen]).where(webbestellingen.c.email == m_email).order_by(webbestellingen.c.artikelID)
    rpweb = con.execute(selweb)
    subtot = 0
    btwsub = 0
    for row in rpweb:
        subtot = subtot+row[3]*row[4]
        btwsub = (subtot*btwperc)/(1+btwperc)
        updw = update(webbestellingen).where(and_(webbestellingen.c.email == m_email,\
             webbestellingen.c.artikelID == row[1])).values(subtotaal = subtot, btw = btwsub,\
             voornaam=e1, tussenvoegsel=e2, achternaam=e3, postcode=e4, huisnummer=e5,\
             toevoeging=e6)
        con.execute(updw)
    btnStatus = True
    self.close()
    showBasket(m_email,  self, btnStatus, klmail, subtot, btwsub)
    
def writeVal(valint , rpweb, self):
    metadata = MetaData()
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('reserveringsaldo', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if valint == 0:
        delart = delete(webbestellingen).where(webbestellingen.c.webID == rpweb[6])
        con.execute(delart)
    else:
        updbest = update(webbestellingen).where(webbestellingen.c.webID == rpweb[6]).\
            values(aantal = valint)
        con.execute(updbest)
    updart = update(artikelen).where(artikelen.c.artikelID == rpweb[7]).\
            values(reserveringsaldo = artikelen.c.reserveringsaldo + valint - rpweb[9])
    con.execute(updart)
    self.close()
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Bestelaantal aangepast!')
    msg.setWindowTitle('Bestelaantal')
    msg.exec_()
    
def invoerOK(mbedrag, mrek, martnr, mhoev, movbestnr, m_email, klmail):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    mdag =  str(datetime.datetime.now())[0:10]
    if mbedrag < 0:
        msg.setText('Creditrecord aangemaakt voor klant!\n'+klmail+' € '+str(round(mbedrag,2)))
        metadata = MetaData()              
        webretouren = Table('webretouren', metadata,
            Column('retourID', Integer(), primary_key=True),
            Column('e_mail', String),
            Column('bedrag', Float),
            Column('rekening', String),
            Column('artikelID', Integer),
            Column('aantal', Float),
            Column('ordernummer', Integer),
            Column('boeking', String))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        retournr=(con.execute(select([func.max(webretouren.c.retourID,\
                            type_=Integer).label('retournr')])).scalar())
        retournr += 1
        insret = insert(webretouren).values(retourID = retournr, e_mail = klmail,\
              bedrag = mbedrag, rekening = mrek, artikelID = martnr, aantal = mhoev,\
              ordernummer = movbestnr, boeking = mdag)
        con.execute(insret)
    msg.setWindowTitle('Retourboeking maken')
    msg.exec_()
    
def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr
    
def showFoto(fotopad):
      class Widget(QDialog):
          def __init__(self, parent=None):
              super(Widget, self).__init__(parent)
              self.setWindowTitle("Afbeelding Webartikel")
              self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
              self.setFont(QFont('Arial', 10))
              pixmap = QPixmap(fotopad)
              lbl21 = QLabel()
              lbl21.setPixmap(pixmap)
              grid = QGridLayout()
              grid.setSpacing(20)
              grid.addWidget(lbl21 , 0, 1)
              self.setLayout(grid)
              self.setGeometry(300, 200, 150, 150)
      win = Widget()
      win.exec_()
        
def invoerBasket(martnr, martomschr, mhoev, verkprijs):
    if mhoev == 1:
        ww = ' is '
    else:
        ww = ' zijn '
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Er'+ww+str(int(mhoev))+' st. '+martomschr+'\nartikelnummer: '+str(martnr)+'\nin de winkelwagen geplaatst!')
    msg.setWindowTitle('Inhoud winkelwagen')
    msg.exec_() 
           
def verwerkArtikel(martnr,retstat, m_email, mhoev, self, klmail):
    if not mhoev or not mhoev.text():
        return
    elif retstat:
        mhoev = float(str(mhoev.text()))
        mhoev = -mhoev
    else:
        mhoev = float(str(mhoev))
    mjaar = int(str(datetime.datetime.now())[0:4])
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('mutatiedatum', String),
        Column('jaarverbruik_1', Float),
        Column('jaarverbruik_2', Float),
        Column('reserveringsaldo', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer(), primary_key=True),
        Column('email', String, nullable=False))
    klanten = Table('klanten', metadata,
        Column('klantID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('rekening', String))
    orders_verkoop = Table('orders_verkoop', metadata,
        Column('ovbestelID', Integer, primary_key=True),
        Column('klantID', None, ForeignKey('klanten.klantID')),
        Column('ovbesteldatum', String),
        Column('datum_betaald', String),
        Column('bedrag', Float))
    orders_verkoop_artikelen = Table('orders_verkoop_artikelen', metadata,
        Column('ovaID', Integer, primary_key=True),
        Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('ovaantal', Integer),
        Column('ovleverdatum', String),
        Column('verkoopprijs', Float),
        Column('regel', Integer),
        Column('retour', Float))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('lock', Boolean),
        Column('ondergrens', Float),
        Column('bovengrens', Float))
    afdrachten = Table('afdrachten', metadata,
        Column('afdrachtID', Integer(), primary_key=True),
        Column('soort', String),
        Column('bedrag', Float),
        Column('boekdatum', String),
        Column('betaaldatum', String),
        Column('instantie', String),
        Column('werknemerID', Integer),
        Column('werknummerID', Integer),
        Column('werkorderID', Integer),
        Column('rekeningnummer', String),
        Column('periode', String),
        Column('ovbestelID', Integer))
    artikelmutaties = Table('artikelmutaties', metadata,
       Column('mutatieID', Integer, primary_key=True),
       Column('artikelID', None, ForeignKey('artikelen.artikelID')),
       Column('ovbestelID', None, ForeignKey('orders_verkoop.ovbestelID')),
       Column('hoeveelheid', Float),
       Column('boekdatum', String),
       Column('tot_mag_prijs', Float),
       Column('btw_hoog', Float),
       Column('regel', Integer))
                                       
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
                                
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    transaction = con.begin()
    try:
        if retstat:
            selpers = select([artikelen, accounts, klanten]).\
                where(and_(artikelen.c.artikelID == martnr, accounts.c.email\
                == klmail, klanten.c.accountID == accounts.c.accountID))
            rppers = con.execute(selpers).first()
        else:
            selpers = select([artikelen, accounts, klanten]).\
                where(and_(artikelen.c.artikelID == martnr, accounts.c.email\
                == m_email, klanten.c.accountID == accounts.c.accountID))
            rppers = con.execute(selpers).first()
        selmov = select([orders_verkoop]).where(and_(orders_verkoop.\
            c.ovbesteldatum == str(datetime.datetime.now())[0:10],\
            orders_verkoop.c.klantID == rppers[10]))
        rpmov = con.execute(selmov).first()
        
        if rpmov:
            movbestnr = rpmov[0]
            selao = select([orders_verkoop_artikelen]).where(and_(\
                  orders_verkoop_artikelen.c.artikelID == martnr,\
                  orders_verkoop_artikelen.c.ovbestelID == movbestnr))
            rpao = con.execute(selao).first()
        
        mboekd = movlev = str(datetime.datetime.now())[0:10]
        movlev = str(datetime.datetime.now()+datetime.timedelta(days=7))[0:10]
        
        if rpmov and not rpao:
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
             (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
             orders_verkoop.c.klantID == rppers[10],\
             orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            if retstat == 0:
                mregel = rpreg[6]+1
                movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                    .c.ovaID, type_=Integer).label('movanr')])).scalar())
                movanr += 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], ovaantal =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            elif retstat == 1:
                mregel = rpreg[6]+1
                movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                    .c.ovaID, type_=Integer).label('movanr')])).scalar())
                movanr += 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], retour = mhoev,\
                 verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            if mjaar%2 == 0:    
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                    reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                    reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        elif rpmov and rpao:
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
              (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
              orders_verkoop.c.klantID == rppers[10],\
              orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            mregel = rpreg[6]
            selreg = select([orders_verkoop_artikelen, orders_verkoop]).where(and_\
             (orders_verkoop_artikelen.c.ovbestelID == orders_verkoop.c.ovbestelID,\
             orders_verkoop.c.klantID == rppers[10],\
             orders_verkoop.c.ovbesteldatum == str(datetime.datetime.now())[0:10]))\
              .order_by(orders_verkoop_artikelen.c.regel.desc())
            rpreg = con.execute(selreg).first()
            if retstat == 0:
                mregel = rpreg[6]
                movanr= rpao[0]
                updova = update(orders_verkoop_artikelen).where(and_\
                 (orders_verkoop_artikelen.c.artikelID == martnr,\
                   orders_verkoop_artikelen.c.ovaID == movanr)).\
                   values(ovaantal=orders_verkoop_artikelen.c.ovaantal+mhoev)
                con.execute(updova)
            elif retstat == 1:
                mregel = rpreg[6]
                movanr= rpao[0]
                updova = update(orders_verkoop_artikelen).where(and_\
                 (orders_verkoop_artikelen.c.artikelID == martnr,\
                   orders_verkoop_artikelen.c.ovaID == movanr)).\
                   values(retour=orders_verkoop_artikelen.c.retour+mhoev)
                con.execute(updova)
            if mjaar%2 == 0:    
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                 reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                     reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                   mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        else:
            movbestnr=(con.execute(select([func.max(orders_verkoop.c.ovbestelID, type_=Integer)\
                       .label('movbestnr')])).scalar())
            movbestnr = int(maak11proef(movbestnr))
            insov = insert(orders_verkoop).values(ovbestelID=movbestnr,\
              klantID=rppers[10], ovbesteldatum=str(datetime.datetime.now())[0:10],\
              datum_betaald = str(datetime.datetime.now())[0:10])
            con.execute(insov)
            if retstat == 0:
                mregel = 1
                movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                    .c.ovaID, type_=Integer).label('movanr')])).scalar())
                movanr += 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], ovaantal =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            elif retstat == 1:
                mregel = 1
                movanr=(con.execute(select([func.max(orders_verkoop_artikelen\
                    .c.ovaID, type_=Integer).label('movanr')])).scalar())
                movanr += 1
                insova = insert(orders_verkoop_artikelen).values(ovaID = movanr,\
                 ovbestelID = movbestnr, artikelID = rppers[0], retour =\
                 mhoev, verkoopprijs = round(rppers[2]*(1+rppar[0][1])*(1+rppar[3][1]),2),\
                 regel = mregel, ovleverdatum = movlev)
                con.execute(insova)
            if mjaar%2 == 0:           
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                   reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                  mutatiedatum = mboekd, jaarverbruik_1 = artikelen.c.jaarverbruik_1 + mhoev)
                con.execute(ua)
            elif mjaar%2 == 1:                     
                ua = update(artikelen).where(artikelen.c.artikelID == martnr)\
                 .values(art_voorraad  = artikelen.c.art_voorraad - mhoev,\
                   reserveringsaldo = artikelen.c.reserveringsaldo - mhoev,\
                  mutatiedatum = mboekd, jaarverbruik_2 = artikelen.c.jaarverbruik_2 + mhoev)
                con.execute(ua)
        uov = update(orders_verkoop).where(and_(orders_verkoop.c.\
         ovbestelID == movbestnr, orders_verkoop_artikelen.c.ovbestelID == movbestnr,\
         orders_verkoop_artikelen.c.regel == mregel)).values(\
         bedrag = orders_verkoop.c.bedrag+\
         orders_verkoop_artikelen.c.verkoopprijs*mhoev+orders_verkoop_artikelen.c.verkoopprijs\
         *orders_verkoop_artikelen.c.retour)
        con.execute(uov)
        mafdrachtnr =(con.execute(select([func.max(afdrachten.c.afdrachtID,\
            type_=Integer).label('mafdrachtnr')])).scalar())
        mafdrachtnr += 1
        iafdr = insert(afdrachten).values(afdrachtID=mafdrachtnr,\
         soort = 'BTW afdracht 21%', instantie = 'Belastingdienst',\
         rekeningnummer = 'NL10 ABNA 9999999977', boekdatum = mboekd,\
         bedrag = mhoev*rppers[2]*(1+rppar[3][1])*(rppar[0][1]),\
         periode = mboekd[0:7], ovbestelID = movbestnr)
        con.execute(iafdr)
        mutatienr=(con.execute(select([func.max(artikelmutaties.c.mutatieID,\
            type_=Integer).label('mutatienr')])).scalar())
        mutatienr += 1
        insmut = insert(artikelmutaties).values(mutatieID=mutatienr,\
         artikelID=martnr,ovbestelID=movbestnr, hoeveelheid = -mhoev,\
         boekdatum=mboekd, tot_mag_prijs=rppers[2]*-mhoev,\
         btw_hoog = -mhoev*(rppers[2])*(1+rppar[3][1])*(rppar[0][1]),\
         regel = mregel)  
        con.execute(insmut) 
        mbedrag = mhoev*rppers[2]*(1+rppar[3][1])*(1+rppar[0][1]) 
        mrek = rppers[12]                           
        transaction.commit()
        if retstat and mhoev != 0:
            invoerOK(mbedrag, mrek, martnr, mhoev, movbestnr, m_email, klmail)
            self.close()
    except IntegrityError as e:
        transaction.rollback()
        foutAlert(e)
        sys.exit()
        
def vulBasket(martnr, m_email, mhoev, verkprijs, self):
    mhoev = str(mhoev.text())
    if mhoev > '0':
        mhoev = float(mhoev)
        metadata = MetaData()              
        artikelen = Table('artikelen', metadata,
            Column('artikelID', Integer, primary_key=True),
            Column('artikelomschrijving', String),
            Column('reserveringsaldo', Float),
            Column('artikelprijs', Float),
            Column('art_voorraad', Float))
        webbestellingen = Table('webbestellingen', metadata,
            Column('webID', Integer, primary_key=True),
            Column('artikelID', ForeignKey('artikelen.artikelID')),
            Column('email', String),
            Column('aantal', Float),
            Column('stukprijs', Float))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        sel = select([artikelen]).where(artikelen.c.artikelID == martnr)
        rpart = con.execute(sel).first()
          
        if rpart[4] - rpart[2] >= mhoev:
            selw = select([webbestellingen]).where(and_(webbestellingen.c.artikelID == martnr,\
                        webbestellingen.c.email == m_email))
            rpw = con.execute(selw).first()
            if rpw:
                updweb = update(webbestellingen).where(and_(webbestellingen.c.artikelID == martnr,\
                               webbestellingen.c.email == m_email)).\
                  values(aantal = webbestellingen.c.aantal + mhoev)
                con.execute(updweb)                
            else:
                webnr=con.execute(select([func.max(webbestellingen.c.webID,\
                                        type_=Integer).label('webnr')])).scalar()
                webnr += 1 
                insw = insert(webbestellingen).values(webID = webnr, artikelID = martnr, email = m_email,\
                               aantal = mhoev, stukprijs = verkprijs)
                con.execute(insw)
            selart = select([artikelen, webbestellingen]).where(and_(artikelen.c.artikelID == martnr, webbestellingen.c.email == m_email))
            rpart = con.execute(selart).first()
            updart = update(artikelen).where(artikelen.c.artikelID == martnr).values(reserveringsaldo = artikelen.c.reserveringsaldo + mhoev)
            con.execute(updart)
            martomschr = rpart[1]
            invoerBasket(martnr, martomschr, mhoev, verkprijs)
            self.close()
        else:
            negVoorraad(rpart[4]-rpart[2])
         
def showBasket(m_email, self, btnStatus, klmail, subtot, btwsub):
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer, primary_key=True),
        Column('artikelomschrijving', String),
        Column('thumb_artikel', String),
        Column('foto_artikel', String),
        Column('artikelprijs', Float),
        Column('art_eenheid', String(20)))
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float),
        Column('stukprijs', Float),
        Column('subtotaal', Float),
        Column('btw', Float),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String),
        Column('voornaam', String),
        Column('tussenvoegsel', String),
        Column('achternaam', String))
    accounts = Table('accounts', metadata,
         Column('accountID', Integer(), primary_key=True),
         Column('email', String),
         Column('voornaam', String), 
         Column('tussenvoegsel', String),
         Column('achternaam', String),
         Column('postcode', String),
         Column('huisnummer', String),
         Column('toevoeging', String))
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selbest = select([artikelen, webbestellingen]).where(and_(webbestellingen.c.email == m_email,\
                    webbestellingen.c.artikelID == artikelen.c.artikelID)).order_by(webbestellingen.c.artikelID)
    rps = con.execute(selbest).fetchone()
    selw = select([webbestellingen, accounts]).where(and_(webbestellingen.c.email == m_email,\
                 webbestellingen.c.email == accounts.c.email))
    rpw = con.execute(selw).first()
    postsel = select([params]).where(params.c.paramID == 102)
    rppost = con.execute(postsel).first()
    if rps:
        rpsel = con.execute(selbest)
        class MyWindow(QDialog):
            def __init__(self, data_list, header):
                QDialog.__init__(self)
                self.setWindowTitle('Inhoud winkelwagen')
                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                  Qt.WindowMinMaxButtonsHint)
                self.setFont(QFont('Arial', 10))
                
                grid = QGridLayout()
                grid.setSpacing(20)
                
                table_model = MyTableModel(self, data_list, header)
                table_view = QTableView()
                table_view.setModel(table_model)
                font = QFont("Arial", 10)
                table_view.setFont(font)
                table_view.resizeColumnsToContents()
                table_view.setSelectionBehavior(QTableView.SelectRows)
                table_view.setColumnWidth(2, 100)
                table_view.verticalHeader().setDefaultSectionSize(75)
                table_view.setItemDelegateForColumn(2, showImage(self))
                table_view.setColumnHidden(3,True)
                table_view.setColumnHidden(4,True)
                table_view.setColumnHidden(6,True)             
                table_view.setColumnHidden(7,True)
                table_view.setColumnHidden(8,True)
                table_view.setColumnHidden(13,True)
                table_view.setColumnHidden(14,True)
                table_view.setColumnHidden(15,True)
                table_view.setColumnHidden(16,True)
                table_view.setColumnHidden(17,True)
                table_view.setColumnHidden(18,True)
                table_view.clicked.connect(showSpinBox)
                
                grid.addWidget(table_view, 0, 0, 1, 6)
                               
                grid.addWidget(QLabel('Bezorgadres:      (wijzigen indien gewenst)'), 1, 0, 1 ,2)
                
                if rpw[7] == '':
                    e1 = QLineEdit(rpw[15])
                else:
                    e1 = QLineEdit(rpw[10])
                e1.setFixedWidth(220)
                e1.setFont(QFont("Arial",10))
                def textchange():
                    e1.setText(e1.text())
                e1.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,30}$")
                input_validator = QRegExpValidator(reg_ex, e1)
                e1.setValidator(input_validator)
                grid.addWidget(QLabel('Voornaam'), 2, 0)
                grid.addWidget(e1, 2, 1)
                 
                if rpw[7] == '':
                    e2 = QLineEdit(rpw[16])
                else:
                    e2 = QLineEdit(rpw[11])
                e2.setFixedWidth(80)
                e2.setFont(QFont("Arial",10))
                def textchange():
                    e2.setText(e2.text())
                e2.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,10}$")
                input_validator = QRegExpValidator(reg_ex, e2)
                e2.setValidator(input_validator)
                grid.addWidget(QLabel('Tussenvoegsel'), 2, 2)
                grid.addWidget(e2, 2, 3)
                
                if rpw[7] == '':
                    e3 = QLineEdit(rpw[17])
                else:
                    e3 = QLineEdit(rpw[12])               
                e3.setFixedWidth(250)
                e3.setFont(QFont("Arial",10))
                def textchange():
                    e3.setText(e3.text())
                e3.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{1,50}$")
                input_validator = QRegExpValidator(reg_ex, e3)
                e3.setValidator(input_validator)
                grid.addWidget(QLabel('Achternaam'), 2, 4)
                grid.addWidget(e3, 2, 5)
                
                if rpw[7] == '':
                    e4 = QLineEdit(rpw[18])
                else:
                    e4 = QLineEdit(rpw[7])
                e4.setFixedWidth(80)
                e4.setFont(QFont("Arial",10))
                def textchange():
                    e4.setText(e4.text().upper())
                e4.textChanged.connect(textchange)
                reg_ex = QRegExp("^[0-9]{4}[A-Za-z]{2}$")
                input_validator = QRegExpValidator(reg_ex, e4)
                e4.setValidator(input_validator)
                grid.addWidget(QLabel('Postcode'), 3, 2)
                grid.addWidget(e4, 3, 3) 
        
                if rpw[7] == '':
                    e5 = QLineEdit(rpw[19])
                else:
                    e5 = QLineEdit(rpw[8])
                e5.setFixedWidth(80)
                e5.setFont(QFont("Arial",10))
                def textchange():
                    e5.setText(e5.text())
                e5.textChanged.connect(textchange)
                reg_ex = QRegExp("^[0-9]{1,5}$")
                input_validator = QRegExpValidator(reg_ex, e5)
                e5.setValidator(input_validator)
                grid.addWidget(e5, 3, 1)  #huisnummer
                grid.addWidget(QLabel('Toev.'), 3, 1, 1, 1, Qt.AlignCenter)
                
                if rpw[7] == '':
                    e6 = QLineEdit(rpw[20])
                else:
                    e6 = QLineEdit(rpw[9])
                e6.setFixedWidth(80)
                e6.setFont(QFont("Arial",10))
                def textchange():
                    e6.setText(e6.text())
                e6.textChanged.connect(textchange)
                reg_ex = QRegExp("^.{0,8}")
                input_validator = QRegExpValidator(reg_ex, e6)
                e6.setValidator(input_validator)
                grid.addWidget(e6, 3, 1, 1, 1, Qt.AlignRight)   #Toevoeging huisnummer
                              
                from postcode import checkpostcode
                postcStatus = True
                if rpw[7] == '':
                    mstrtpls = checkpostcode(rpw[18], int(rpw[19]))
                    if mstrtpls[0] == '':
                        postcStatus=foutPostcode()
                else:
                    mstrtpls = checkpostcode(rpw[7], int(rpw[8]))
                    if mstrtpls[0] == '':
                        postcStatus=foutPostcode()   
                            
                mfactsp = checkpostcode(rpw[18], int(rpw[19]))
                grid.addWidget(QLabel('Factuuradres: '+rpw[15]+' '+rpw[16]+' '+rpw[17]+',  '+mfactsp[0]+' '+rpw[19]+', '+rpw[18]+' '+mfactsp[1]+'.'), 4, 0, 1 ,4)
 
                freshBtn = QPushButton('Berekening\ngegevens')
                freshBtn.clicked.connect(lambda: refresh(m_email, self,\
                   btnStatus, e1.text(), e2.text(), e3.text(), e4.text(), e5.text(), e6.text(), klmail))

                freshBtn.setFont(QFont("Arial",10))
                freshBtn.setFixedWidth(140) 
                freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
                grid.addWidget(freshBtn, 6, 5, 2, 1, Qt.AlignRight | Qt.AlignBottom)
                
                betaalBtn = QPushButton()
                betaalBtn.setIcon(QIcon('./images/logos/Betaal/afrekenen.png'))
                betaalBtn.setIconSize(QSize(90, 60))
                
                betaalBtn.setFixedWidth(100) 
                betaalBtn.setStyleSheet("color: black;  background-color: gainsboro")
                betaalBtn.clicked.connect(lambda: betaalBasket(m_email, klmail, factbedrag))
              
                grid.addWidget(betaalBtn, 6, 5, 2, 1, Qt.AlignLeft | Qt.AlignTop)
  
                sluitBtn = QPushButton('Sluiten')
                sluitBtn.clicked.connect(self.close)

                sluitBtn.setFont(QFont("Arial",10))
                sluitBtn.setFixedWidth(100) 
                sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(sluitBtn, 7, 4, 1, 1, Qt.AlignRight)
                
                helpBtn = QPushButton('Informatie')
                helpBtn.clicked.connect(lambda: help())

                helpBtn.setFont(QFont("Arial",10))
                helpBtn.setFixedWidth(100) 
                helpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(helpBtn, 7, 3, 1, 1, Qt.AlignRight)
                
                helpBtn = QPushButton('Informatie')
                helpBtn.clicked.connect(lambda: info())

                helpBtn.setFont(QFont("Arial",10))
                helpBtn.setFixedWidth(100) 
                helpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                grid.addWidget(helpBtn, 7, 3, 1, 1, Qt.AlignRight)
                
                betaalBtn.setEnabled(False)
                cBox = QCheckBox('Akkoord algemene voorwaarden')
                def cboxChange():
                    cBox = self.sender()
                    if (cBox.isChecked() and postcStatus and  btnStatus):
                        betaalBtn.setEnabled(True)
                        cBox.setChecked(True)
                                                               
                cBox.toggled.connect(cboxChange)
   
                grid.addWidget(cBox, 4, 4, 1, 2)
                             
                grid.addWidget(QLabel(mstrtpls[0]), 3, 0)
                grid.addWidget(QLabel(mstrtpls[1]), 3, 4)
                
                postnl = rppost[1]
                factbedrag = round(subtot+postnl, 2)
                              
                grid.addWidget(QLabel('Som subtotalen:  '), 5, 0)
                grid.addWidget(QLabel(str(round(subtot,2))), 5, 1, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('Bedrag BTW 21%: '), 5 ,2, 1, 2)
                grid.addWidget(QLabel(str(round(btwsub,2))), 5, 3, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('Bezorgkosten PostNL: '), 6, 0)
                grid.addWidget(QLabel(str(postnl)), 6, 1, 1, 1, Qt.AlignRight)
                grid.addWidget(QLabel('Totaal factuurbedrag: '), 7, 0)
                grid.addWidget(QLabel(str(factbedrag)), 7, 1, 1, 1, Qt.AlignRight)
     
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 6, Qt.AlignCenter)
                
                self.setLayout(grid)
                self.setGeometry(250, 50, 600, 900)
                                              
        class MyTableModel(QAbstractTableModel):
            def __init__(self, parent, mylist, header, *args):
                QAbstractTableModel.__init__(self, parent, *args)
                self.mylist = mylist
                self.header = header
            def rowCount(self, parent):
                return len(self.mylist)
            def columnCount(self, parent):
                return len(self.mylist[0])
            def data(self, index, role):
                if not index.isValid():
                    return None
                elif role != Qt.DisplayRole:
                    return None
                return str(self.mylist[index.row()][index.column()])
            def headerData(self, col, orientation, role):
                if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                    return self.header[col]
                return None
            
        class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap))
 
        header = ['Artikelnr','Omschrijving', 'Thumb','Foto','ArtikelPrijs', 'Eenheid',\
                  'WebID','Artikelnr', 'email','Aantal','Stukprijs', 'Subtotaal', 'BTW',\
                  '','','','','','']
                          
        data_list=[]
        for row in rpsel:
            data_list += [(row)]
                          
        def showSpinBox(idx):
            artnr = idx.data()
            if idx.column() == 0 and not btnStatus:
               engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
               con = engine.connect()
               selweb = select([artikelen, webbestellingen]).where(and_(webbestellingen.c.artikelID == artnr,\
               webbestellingen.c.artikelID == artikelen.c.artikelID, webbestellingen.c.email == m_email))
               rpweb = con.execute(selweb).first()
               class MainWindow(QDialog):
                   def __init__(self):
                        QDialog.__init__(self)
                                                         
                        self.setWindowTitle("Aantal wijzigen")
                        self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                        self.setFont(QFont('Arial', 10))
                        
                        grid = QGridLayout()
                        grid.setSpacing(20)
                        
                        lbl = QLabel()
                        pixmap = QPixmap('./images/logos/verbinding.jpg')
                        lbl.setPixmap(pixmap)
                        grid.addWidget(lbl , 0, 0, 1, 2)
            
                        logo = QLabel()
                        pixmap = QPixmap('./images/logos/logo.jpg')
                        logo.setPixmap(pixmap)
                        grid.addWidget(logo , 0, 0, 1, 2, Qt.AlignRight)
                        
                        self.qspin = QSpinBox()
                        self.qspin.setRange(0, 100)
                        self.qspin.setFrame(True)
                        self.qspin.setFont(QFont('Arial', 10))
                        self.qspin.setValue(int(rpweb[9]))
                        self.qspin.setFixedSize(40, 30)
                        self.qspin.setStyleSheet("color: black; font: bold;  background-color: gainsboro")
                        
                        def valuechange():
                           self.qspin.setValue(self.qspin.value())
                                                                         
                        self.qspin.valueChanged.connect(valuechange)
                                                                 
                        grid.addWidget(QLabel('Wijzig bestelaantal van artikel\n'+str(rpweb[0])+' '+rpweb[1]), 2, 0, 1, 2)
                        
                        grid.addWidget(QLabel('Bestelaantal'), 3, 0, 1, 2, Qt.AlignCenter)
                        grid.addWidget(self.qspin, 3, 1)
                        
                        lblpic = QLabel()
                        pixmap = QPixmap(rpweb[2])
                        lblpic.setPixmap(pixmap)
                        grid.addWidget(lblpic , 3, 0, 2, 1)
                        
                        closeBtn = QPushButton('Sluiten')
                        closeBtn.clicked.connect(self.close)
                       
                        grid.addWidget(closeBtn, 4, 0, 1, 1, Qt.AlignRight)
                        closeBtn.setFont(QFont("Arial",10))
                        closeBtn.setFixedWidth(100) 
                        closeBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                                                                                   
                        aanpBtn = QPushButton('Aanpassen')
                        aanpBtn.clicked.connect(lambda: writeVal(self.qspin.value(), rpweb, self))
                       
                        grid.addWidget(aanpBtn, 4, 1, 1, 1, Qt.AlignRight)
                        aanpBtn.setFont(QFont("Arial",10))
                        aanpBtn.setFixedWidth(100) 
                        aanpBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                                                                          
                        grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 5, 0, 1, 2, Qt.AlignCenter)
                        
                        self.setLayout(grid)
                        self.setGeometry(900, 200, 100, 100)
                        self.setLayout(grid)
                                                
               mainWin = MainWindow()
               mainWin.exec_()
                  
        win = MyWindow(data_list, header)
        win.exec_()
    else:
        geenRegels()
         
def betaalBasket(m_email, klmail, factbedrag):
    metadata = MetaData()              
    webbestellingen = Table('webbestellingen', metadata,
        Column('webID', Integer, primary_key=True),
        Column('artikelID', ForeignKey('artikelen.artikelID')),
        Column('email', String),
        Column('aantal', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selbest = select([webbestellingen]).where(webbestellingen.c.email == m_email)
    rps = con.execute(selbest).fetchone()
    if rps:
        class Widget(QDialog):
            def __init__(self, parent=None):
                super(Widget, self).__init__(parent)
                self.setWindowTitle("Winkelwagen en betalen")
                self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                self.setFont(QFont('Arial', 10))
                grid = QGridLayout()
                grid.setSpacing(20)
                self.setLayout(grid)
                self.setGeometry(400, 100, 250, 150)
                lbl = QLabel()
                pixmap = QPixmap('./images/logos/verbinding.jpg')
                lbl.setPixmap(pixmap)
                grid.addWidget(lbl , 0, 0, 1, 2)
                
                lblinfo = QLabel('Afrekenen\n€ '+str(factbedrag))
                grid.addWidget(lblinfo, 0, 2, 1, 2, Qt.AlignCenter)
                lblinfo.setStyleSheet("color: rgb(45, 83, 115); font: 18pt Comic Sans MS")
                
                logo = QLabel()
                pixmap = QPixmap('./images/logos/logo.jpg')
                logo.setPixmap(pixmap)
                grid.addWidget(logo , 0, 4, 1, 1, Qt.AlignRight)
             
                ideal = QPushButton()
                grid.addWidget(ideal, 1, 0, 1, 5, Qt.AlignCenter)
                ideal.setIcon(QIcon('./images/logos/Betaal/iDEAL.png'))
                ideal.setIconSize(QSize(120, 120))
                ideal.setFlat(True)
                               
                ABNamroBtn = QPushButton()
                ABNamroBtn.clicked.connect(lambda: handler(m_email, self))
                ABNamroBtn.setCheckable(True)
                grid.addWidget(ABNamroBtn, 2, 0)
                ABNamroBtn.setIcon(QIcon('./images/logos/Betaal/ABNAmro.png'))
                ABNamroBtn.setIconSize(QSize(90, 60))
                ABNamroBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                ASNBankBtn = QPushButton()
                ASNBankBtn.clicked.connect(lambda: handler(m_email, self))
                ASNBankBtn.setCheckable(True)
                grid.addWidget(ASNBankBtn, 2, 1)
                ASNBankBtn.setIcon(QIcon('./images/logos/Betaal/ASNBank.png'))
                ASNBankBtn.setIconSize(QSize(90, 60))
                ASNBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                INGBtn = QPushButton()
                INGBtn.clicked.connect(lambda: handler(m_email, self))
                INGBtn.setCheckable(True)
                grid.addWidget(INGBtn, 2, 2)
                INGBtn.setIcon(QIcon('./images/logos/Betaal/ING.png'))
                INGBtn.setIconSize(QSize(90, 60))
                INGBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                KnabBtn = QPushButton()
                KnabBtn.clicked.connect(lambda: handler(m_email, self))
                KnabBtn.setCheckable(True)
                grid.addWidget(KnabBtn, 2, 3)
                KnabBtn.setIcon(QIcon('./images/logos/Betaal/Knab.png'))
                KnabBtn.setIconSize(QSize(90, 60))
                KnabBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                RabobankBtn = QPushButton()
                RabobankBtn.clicked.connect(lambda: handler(m_email, self))
                RabobankBtn.setCheckable(True)
                grid.addWidget(RabobankBtn, 2, 4)
                RabobankBtn.setIcon(QIcon('./images/logos/Betaal/Rabobank.png'))
                RabobankBtn.setIconSize(QSize(90, 60))
                RabobankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                RegioBankBtn = QPushButton()
                RegioBankBtn.clicked.connect(lambda: handler(m_email, self))
                RegioBankBtn.setCheckable(True)
                grid.addWidget(RegioBankBtn, 3, 0)
                RegioBankBtn.setIcon(QIcon('./images/logos/Betaal/RegioBank.png'))
                RegioBankBtn.setIconSize(QSize(90, 60))
                RegioBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                SNSBankBtn = QPushButton()
                SNSBankBtn.clicked.connect(lambda: handler(m_email, self))
                SNSBankBtn.setCheckable(True)
                grid.addWidget(SNSBankBtn, 3, 1)
                SNSBankBtn.setIcon(QIcon('./images/logos/Betaal/SNSBank.png'))
                SNSBankBtn.setIconSize(QSize(90, 60))
                SNSBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                TriodosBankBtn = QPushButton()
                TriodosBankBtn.clicked.connect(lambda: handler(m_email, self))
                TriodosBankBtn.setCheckable(True)
                grid.addWidget(TriodosBankBtn, 3, 2)
                TriodosBankBtn.setIcon(QIcon('./images/logos/Betaal/TriodosBank.png'))
                TriodosBankBtn.setIconSize(QSize(90, 60))
                TriodosBankBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                VanLanschotBtn = QPushButton()
                VanLanschotBtn.clicked.connect(lambda: handler(m_email, self))
                VanLanschotBtn.setCheckable(True)
                grid.addWidget(VanLanschotBtn, 3, 3)
                VanLanschotBtn.setIcon(QIcon('./images/logos/Betaal/VanLanschot.png'))
                VanLanschotBtn.setIconSize(QSize(90, 60))
                VanLanschotBtn.setStyleSheet("color: black;  background-color: gainsboro") 
                
                credit = QPushButton()
                grid.addWidget(credit, 4, 0, 1, 5, Qt.AlignCenter)
                credit.setIcon(QIcon('./images/logos/Betaal/creditcard.jpg'))
                credit.setIconSize(QSize(120, 120))
                credit.setFlat(True)

                VisaBtn = QPushButton()
                VisaBtn.clicked.connect(lambda: handler(m_email, self))
                VisaBtn.setCheckable(True)
                grid.addWidget(VisaBtn, 5, 1)
                VisaBtn.setIcon(QIcon('./images/logos/Betaal/Visa.png'))
                VisaBtn.setIconSize(QSize(90, 60))
                VisaBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                
                MasterCardBtn = QPushButton()
                MasterCardBtn.clicked.connect(lambda: handler(m_email, self))
                MasterCardBtn.setCheckable(True)
                grid.addWidget(MasterCardBtn, 5, 2)
                MasterCardBtn.setIcon(QIcon('./images/logos/Betaal/MasterCard.png'))
                MasterCardBtn.setIconSize(QSize(90, 60))
                MasterCardBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                AmericanExpressBtn = QPushButton()
                AmericanExpressBtn.clicked.connect(lambda: handler(m_email, self))
                AmericanExpressBtn.setCheckable(True)
                grid.addWidget(AmericanExpressBtn, 5, 3)
                AmericanExpressBtn.setIcon(QIcon('./images/logos/Betaal/AmericanExpress.png'))
                AmericanExpressBtn.setIconSize(QSize(90, 60))
                AmericanExpressBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                PayPalBtn = QPushButton()
                PayPalBtn.clicked.connect(lambda: handler(m_email, self))
                PayPalBtn.setCheckable(True)
                grid.addWidget(PayPalBtn, 6, 0)
                PayPalBtn.setIcon(QIcon('./images/logos/Betaal/PayPal.png'))
                PayPalBtn.setIconSize(QSize(90, 60))
                PayPalBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                        
                afterPayBtn = QPushButton()
                afterPayBtn.clicked.connect(lambda: handler(m_email, self))
                afterPayBtn.setCheckable(True)
                grid.addWidget(afterPayBtn, 6, 4)
                afterPayBtn.setIcon(QIcon('./images/logos/Betaal/afterpay.png'))
                afterPayBtn.setIconSize(QSize(90, 60))
                afterPayBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
                sluitenBtn = QPushButton('Sluiten')
                sluitenBtn.clicked.connect(self.accept)
                
                grid.addWidget(sluitenBtn, 7, 4)
                sluitenBtn.setFont(QFont("Arial",10))
                sluitenBtn.setFixedWidth(100) 
                sluitenBtn.setStyleSheet("color: black;  background-color: gainsboro")
                
                grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 8, 0, 1, 6, Qt.AlignCenter)
                                
                def handler(m_email, self):
                    if PayPalBtn.isChecked() or ABNamroBtn.isChecked() or afterPayBtn.isChecked()\
                        or ASNBankBtn.isChecked() or INGBtn.isChecked() or KnabBtn.isChecked()\
                        or RabobankBtn.isChecked() or RegioBankBtn.isChecked() or\
                        SNSBankBtn.isChecked() or TriodosBankBtn.isChecked() or\
                        VanLanschotBtn.isChecked() or AmericanExpressBtn.isChecked() or\
                        MasterCardBtn.isChecked() or VisaBtn.isChecked():
                    
                        #indien produktie doorgeven bedrag en naam Pandora BV Vianen
                        #en klant e-mail bij terugontvangst akoord onderstaand uitvoeren
                        #anders melding om opnieuw betaling uit te voeren!
                        rpsel = con.execute(selbest)
                        for row in rpsel:
                            verwerkArtikel(row[1], 0, m_email, row[3], self, klmail)
                            delsel = delete(webbestellingen).where(webbestellingen.c.email == m_email)
                            con.execute(delsel)
                        bestGelukt()
                        self.close()
                    else:
                        betMislukt()
                        self.close()
                               
        win = Widget()
        win.exec_()
    else:
        geenRegels()
 
def artKeuze(m_email, retstat, klmail):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen / Bestellen Webartikelen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(220)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: gainsboro")
            k0Edit.addItem(' Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Gesorteerd op artikelnr')
            k0Edit.addItem('2. Gesorteerd op voorraad')
            k0Edit.addItem('3. Gefilterd omschrijving')
            k0Edit.addItem('4. Gefilterd artikelgroep.')
            k0Edit.addItem('5. Gefilterd opslaglocatie.')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(220)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 1, 0, 1 ,2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 1, 1, 2, Qt.AlignRight)
                                  
            grid.addWidget(k0Edit, 2, 1)
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 3, 0)
            grid.addWidget(zktermEdit, 3, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 6, 0, 1, 3)
        
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
      
            grid.addWidget(applyBtn, 5, 1, 1, 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            closeBtn = QPushButton('Sluiten')
            closeBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(closeBtn, 5, 1, 1, 1)
            closeBtn.setFont(QFont("Arial",10))
            closeBtn.setFixedWidth(100)
            closeBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk0(self):
            return self.Keuze.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzkterm()] 
        
    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    toonArtikellijst(m_email, retstat, keuze, zoekterm, klmail)
                   
def toonArtikellijst(m_email, retstat, keuze, zoekterm, klmail):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Materiaallijst')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setColumnWidth(2, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.setItemDelegateForColumn(2, showImage(self))
            table_view.clicked.connect(showSelart)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            if not index.isValid():
                return None
            elif role != Qt.DisplayRole:
                return None
            return str(self.mylist[index.row()][index.column()])
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
        
    class showImage(QStyledItemDelegate):  
       def __init__(self, parent):
           QStyledItemDelegate.__init__(self, parent)
       def paint(self, painter, option, index):        
            painter.fillRect(option.rect,QColor(255,255,255))
            image = QImage(index.data())
            pixmap = QPixmap(image)
            pixmap.scaled(256,256) 
            return(painter.drawPixmap(option.rect, pixmap))
   
    header = ['Artikelnr','Omschrijving', 'Thumb','ArtikelPrijs', 'Voorraad',\
              'Eenheid','Minimum Voorraad','Bestelgrootte', 'Locatie',\
              'Artikelgroep', 'Categorie', 'Afmeting']
    
    metadata = MetaData()              
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('thumb_artikel', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String(20)),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float),
        Column('locatie_magazijn', String(10)),
        Column('artikelgroep', String),
        Column('categorie', String(10)),
        Column('afmeting', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    if keuze == 1:
        sel = select([artikelen]).order_by(artikelen.c.artikelID)
    elif keuze == 2:
        sel = select([artikelen]).order_by(artikelen.c.art_voorraad)
    elif keuze == 3:
        sel = select([artikelen]).where(artikelen.c.artikelomschrijving.ilike\
           ('%'+zoekterm+'%')).order_by(artikelen.c.artikelID) 
    elif keuze == 4:
        sel = select([artikelen]).where(artikelen.c.artikelgroep.ilike\
            ('%'+zoekterm+'%')).order_by(artikelen.c.artikelgroep)
    elif keuze == 5:
        sel = select([artikelen]).where(artikelen.c.locatie_magazijn.\
        ilike('%'+zoekterm+'%')).order_by(artikelen.c.locatie_magazijn)
    else:
        ongInvoer()
        artKeuze(m_email, retstat, klmail)

    if con.execute(sel).fetchone():
        rpartikelen = con.execute(sel)
    else:
        geenRecord()
        artKeuze(m_email,retstat,klmail)
     
    data_list=[]
    for row in rpartikelen:
        data_list += [(row)]
        
    def showSelart(idx):
        martnr = idx.data()
        if idx.column() == 0:
            header = ['Artikelnr','Omschrijving','ArtikelPrijs', 'Voorraad',\
              'Eenheid','Minimum Voorraad','Bestelgrootte', 'Locatie',\
              'Artikelgroep', 'Categorie', 'Afmeting', 'Afbeelding']
        
            metadata = MetaData()              
            artikelen = Table('artikelen', metadata,
                Column('artikelID', Integer(), primary_key=True),
                Column('artikelomschrijving', String),
                Column('artikelprijs', Float),
                Column('art_voorraad', Float),
                Column('art_eenheid', String(20)),
                Column('art_min_voorraad', Float),
                Column('art_bestelgrootte', Float),
                Column('locatie_magazijn', String(10)),
                Column('artikelgroep', String),
                Column('categorie', String(10)),
                Column('afmeting', String),
                Column('thumb_artikel', String),
                Column('foto_artikel', String))
            params = Table('params', metadata,
                Column('paramID', Integer, primary_key=True),
                Column('tarief', Float))
             
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
      
            sel = select([artikelen]).where(artikelen.c.artikelID == martnr)
            rpartikelen = con.execute(sel).first()
     
            selpar = select([params]).order_by(params.c.paramID)
            rppar = con.execute(selpar).fetchall()
            verkprijs = rpartikelen[2]*(1+rppar[3][1])*(1+rppar[0][1])
                                 
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                                
                    self.setWindowTitle("Bestellingen Webartikelen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Bestellingen Webartikelen'),0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)                
                    index = 1
                    for item in header:
                        self.lbl = QLabel('{:15}'.format(header[index-1]))
                        self.Gegevens = QLabel()
                        if index == 2:
                            q1Edit = QLineEdit('{:40}'.format(str(rpartikelen[index-1])))
                            q1Edit.setFixedWidth(400)
                        elif index == 3:
                            q1Edit = QLineEdit('{:10}'.format(str(round(rpartikelen[index-1]*(1+rppar[3][1])*(1+rppar[0][1]),2))))
                            q1Edit.setFixedWidth(100)
                        elif index == 12:
                            pixmap = QPixmap(rpartikelen[11])
                            lbl21 = QLabel(self)
                            lbl21.setPixmap(pixmap)
                            grid.addWidget(lbl21 , index, 1, 3, 1)
                        else:
                            q1Edit = QLineEdit('{:10}'.format(str(rpartikelen[index-1])))
                            q1Edit.setFixedWidth(100)
                        q1Edit.setDisabled(True)
                        grid.addWidget(self.lbl, index, 0)
                        if index != 12 and index != 13:
                            grid.addWidget(q1Edit, index, 1, 1, 2)
          
                        index +=1
                    
                    self.Bestelaantal = QLabel(self)
                    if retstat == 0:
                        self.Bestelaantal.setText('                     Bestelaantal ')
                    else:
                        self.Bestelaantal.setText('                          Retouraantal')
                    self.best = QLineEdit(self)
                    self.best.setFixedWidth(50)
                    
                    if retstat == 1:
                        reg_ex = QRegExp('^[0-9]{0,10}[.]{1}[0-9]{0,10}$')
                    else:
                        reg_ex = QRegExp('^[0-9]{0,10}[.]{1}[0-9]{0,10}$')
                    input_validator = QRegExpValidator(reg_ex, self.best)
                    self.best.setValidator(input_validator)
                    
                    grid.addWidget(self.Bestelaantal, index-1, 1)
                    grid.addWidget(self.best, index-1, 1, 1, 1, Qt.AlignRight)
                    
                    subtot = 0
                    btwsub = 0
                    basket = QPushButton()
                    grid.addWidget(basket, index-5, 2, 2, 1, Qt.AlignLeft)
                    btnStatus = False
                    basket.setIcon(QIcon('./images/logos/basket.jpg'))
                    basket.setIconSize(QSize(90, 90))
                    basket.setStyleSheet("color: black;  background-color: gainsboro")
                    basket.clicked.connect(lambda: showBasket(m_email, self, btnStatus, klmail, subtot,btwsub))
                                      
                    fotoBtn = QPushButton('Foto groot')
                    fotoBtn.clicked.connect(lambda: showFoto(rpartikelen[12]))
            
                    grid.addWidget(fotoBtn, index-3, 2, 1, 1, Qt.AlignTop)
                    fotoBtn.setFont(QFont("Arial",10))
                    fotoBtn.setFixedWidth(100) 
                    fotoBtn.setStyleSheet("color: black;  background-color: gainsboro")
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, index-2, 2)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100) 
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    mhoev = self.best
                    if retstat == 1:
                        basket.setDisabled(True)
                        bestelBtn = QPushButton('Retour')
                        bestelBtn.clicked.connect(lambda: verwerkArtikel(martnr,retstat, m_email, mhoev, self, klmail))
                    else:
                        basket.setDisabled(False)
                        bestelBtn = QPushButton('Bestellen')
                        bestelBtn.clicked.connect(lambda: vulBasket(martnr, m_email, mhoev, verkprijs, self))
                     
                    grid.addWidget(bestelBtn, index-1, 2)
                    bestelBtn.setFont(QFont("Arial",10))
                    bestelBtn.setFixedWidth(100) 
                    bestelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                 
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+4, 0, 1, 3, Qt.AlignCenter)
                                                                               
                    self.setLayout(grid)
                    self.setGeometry(300, 150, 150, 150)
                                                               
            mainWin = MainWindow()
            mainWin.exec_()
                      
    win = MyWindow(data_list, header)
    win.exec_()
    artKeuze(m_email, retstat, klmail)