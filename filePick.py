from login import hoofdMenu
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QTextEdit

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Printen diverse formulieren')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
 
def ongDir(m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Directory niet toegestaan!')
    msg.setWindowTitle('Geen bevoegdheid')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
    hoofdMenu(m_email)
    
def printFile(filename):
    from sys import platform
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
    
def fileList(m_email, path):
    class bestandLijst(QDialog):
       def __init__(self, parent = None):
          super(bestandLijst, self).__init__(parent)
          self.getfile()
                 
       def getfile(self):
          fname = QFileDialog.getOpenFileName(self, 'Herprinten bestanden', path)

          if fname[0].find(path[1:]) == -1:  
              ongDir(m_email)
              #if specified path differs from the actual path deny printing
              #not secure enough, looking for enother solution
          else:
              printFile(fname[0])

    bestandLijst()
    hoofdMenu(m_email)
