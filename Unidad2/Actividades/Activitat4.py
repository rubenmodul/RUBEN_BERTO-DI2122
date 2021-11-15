from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6.QtCore import QSize

from Act4_config import ample,llarg

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.setFixedSize(QSize(ample, llarg))
        self.setWindowTitle("Exemple signals-slots 1")

        self.pybutton = QPushButton('Minimitza', self)
        self.pybutton2 = QPushButton('Normalitza', self)
        self.pybutton3 = QPushButton('Maximitza', self)


        #Connectem la senyal clicked a la ranura button_pressed
        self.pybutton.clicked.connect(self.min1) 
        self.pybutton2.clicked.connect(self.nor1) 
        self.pybutton3.clicked.connect(self.max1) 


        self.pybutton.resize(75, 50)
        self.pybutton.move(20, 125)

        self.pybutton2.resize(75, 50)
        self.pybutton2.move(115, 125)

        self.pybutton3.resize(75, 50)
        self.pybutton3.move(205, 125)


    def min1(self):

            self.setFixedSize(QSize(ample/2+75,llarg/2-100))
            self.setWindowTitle("Minimitza") 

            self.pybutton.move(0, 0)
            self.pybutton2.move(75, 0)
            self.pybutton3.move(150, 0)

            self.pybutton.setEnabled(False)
            self.pybutton2.setEnabled(True)
            self.pybutton3.setEnabled(True)

    def nor1(self):

        self.setFixedSize(QSize(ample,llarg))
        self.setWindowTitle("Normalitza")

        self.pybutton.move(20, 125)
        self.pybutton2.move(115, 125)
        self.pybutton3.move(205, 125)

        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(False)
        self.pybutton3.setEnabled(True)

    def max1(self):

        self.setFixedSize(QSize(ample*2,llarg*2))
        self.setWindowTitle("Maximitza")

        self.pybutton.move(65, 125*2)
        self.pybutton2.move(265, 125*2)
        self.pybutton3.move(465, 125*2)

        self.pybutton.setEnabled(True)
        self.pybutton2.setEnabled(True)
        self.pybutton3.setEnabled(False)

if __name__ == "__main__":
    app = QApplication([])
    mainWin = MainWindow()
    mainWin.show()
    app.exec()
