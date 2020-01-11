from login import hoofdMenu
import os
from PyQt5.QtCore  import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMessageBox,\
                QComboBox, QPushButton

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Printen diverse formulieren')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
 
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
        
def printFile(filename, m_email, path):
    from sys import platform
    if platform == 'win32':
        os.startfile(path+filename, "print")
    else:
        os.system("lpr "+path+filename)
    printing()
    fileList(m_email, path)

def fileList(m_email, path):
    filelist = os.listdir(path)
    class combo(QDialog):
      def __init__(self, parent=None):
          super(combo, self).__init__(parent)
          self.setWindowTitle("Printen van lijsten")
          self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
          self.setFont(QFont("Arial", 10))
          grid = QGridLayout()
          grid.setSpacing(20)
        
          logo = QLabel()
          pixmap = QPixmap('./images/logos/logo.jpg')
          logo.setPixmap(pixmap)
          grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
          
          plbl = QLabel()
          plbl = QLabel('Printen\nLijsten')
          plbl.setStyleSheet("color:rgba(45, 83, 115, 255); font: 20pt Comic Sans MS")
          grid.addWidget(plbl, 0, 1)
                
          lbl = QLabel()
          pixmap = QPixmap('./images/logos/verbinding.jpg')
          lbl.setPixmap(pixmap)
          grid.addWidget(lbl, 0, 0)
                    
          self.cb = QComboBox()
          self.cb.setFixedWidth(430)
          self.Keuze = QLabel()
          
          self.cb.addItem('                               Kies bestand')
          grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignCenter)
          x = 0
          for item in filelist:
              self.cb.addItem(filelist[x])
              grid.addWidget(self.cb, 1, 0, 1, 3, Qt.AlignCenter)
              x += 1
          self.cb.activated[str].connect(self.cbChanged)
          self.cb.setStyleSheet("font: 10pt Comic Sans MS; color: black ; background-color: #D9E1DF") 
              
          cancelBtn = QPushButton('Sluiten')
          cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))  
            
          grid.addWidget(cancelBtn, 3, 1, 1, 1, Qt.AlignRight)
          cancelBtn.setFont(QFont("Arial",10))
          cancelBtn.setFixedWidth(90)
          cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")    
          
          printBtn = QPushButton('Printen')
          printBtn.clicked.connect(self.accept)  
            
          grid.addWidget(printBtn,  3, 2)
          printBtn.setFont(QFont("Arial",10))
          printBtn.setFixedWidth(90)
          printBtn.setStyleSheet("color: black;  background-color: gainsboro")    
              
          grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 3, Qt.AlignCenter)
            
          self.setLayout(grid)
          self.setGeometry(550, 300, 150, 150)
          
      def cbChanged(self, text):
         self.Keuze.setText(text)
        
      def returncb(self):
         return self.Keuze.text()
    
      @staticmethod
      def getData(parent=None):
         dialog = combo(parent)
         dialog.exec_()
         return [dialog.returncb()]
       
    win = combo()
    data = win.getData()
    
    if data[0] == '' or data[0][0] == ' ':
        fileList(m_email, path)
    elif data[0]:
        filename = data[0]
        printFile(filename, m_email, path)
    else:
        fileList(m_email, path)