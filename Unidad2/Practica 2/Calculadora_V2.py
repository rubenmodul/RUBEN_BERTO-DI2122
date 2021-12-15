import os
import sys

from PySide6 import QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QKeySequence, QAction
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QVBoxLayout,
    QLineEdit, QPushButton, QToolBar, QLabel,
    QCheckBox, QStatusBar, QStackedLayout, QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")  # Añadimos titulo de la ventana

        self.widget = QWidget()
        self.layout_p = QVBoxLayout(self.widget)  # Variable 'layout_p' que sera nuestro (layout principal)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout_p)

        #Para la cientifica
        self.layout_h = QHBoxLayout(self.widget)

        # Creamos el 'toolbar' paa la parte del menu
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Añadimos los botones
        button_action = QAction("&Calculadora Cientifica", self)
        button_action.setStatusTip("Calculadora Cientifica")
        button_action.triggered.connect(self.calculadora_c)
        button_action.setCheckable(True)

        toolbar.addSeparator()

        calcu_nor = QAction("Calculadora Normal", self)
        calcu_nor.setStatusTip("Calculadora Normal")
        calcu_nor.triggered.connect(self.calculadora_n)
        calcu_nor.setCheckable(True)

        self.guardar_d = QAction("Guardar", self)
        self.guardar_d.setStatusTip("Guardar")
        self.guardar_d.triggered.connect(self.onMyToolBarButtonClick)
        self.guardar_d.setCheckable(True)

        salir = QAction("Salir", self)
        salir.setStatusTip("Salir")
        salir.triggered.connect(self.salir)
        salir.setShortcut(QKeySequence("CTRL+Q"))

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&Menu")
        file_submenu = file_menu.addMenu("Modo")
        file_submenu.addAction(button_action)
        file_submenu.addSeparator()
        file_submenu.addAction(calcu_nor)
        file_menu.addAction(self.guardar_d)
        file_menu.addAction(salir)

        # Variables
        self.guardar = ""  # Guardar botones pulsados
        self.comprovar_p = True  # Lo utilizaremos para los parentesis
        self.layout_b = QGridLayout()  # Layout para los botones

        self.cuadro_t = QLineEdit()  # Creamos nuestro cuadro de texto 'cuadro_t'
        self.cuadro_t.setReadOnly(True)  # Solo leer
        self.layout_p.addWidget(self.cuadro_t)  # Añadimos el cuadro de texto a nuestro layout principal

        self.botones_normal = {}  # Lista para los botones
        self.botones_cienti = {}

        #  Añadimos cada signo en su boton para la calculadora cientifica
        self.botones_cienti = {
                    '√': (0, 0), 'π': (0, 1), '^': (0, 2), '❗': (0, 3), 'Hyp': (0, 4), 'Mod': (0, 5),
                    'C': (1, 0), '()': (1, 1), '%': (1, 2), '/': (1, 3), 'Sin': (1, 4), '1/x': (1, 5),
                    '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3), 'Cos': (2, 4), 'x!': (2, 5),
                    '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3), 'Tan': (3, 4), 'x^2': (3, 5),
                    '1': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3), 'Log': (4, 4), 'x^y': (4, 5),
                    '.': (5, 0), '0': (5, 1), '⬅': (5, 2), '=': (5, 3), 'Ln': (5, 4), 'x^3': (5, 5),
        }

        #  Añadimos cada signo en su boton para la calculadora normal
        self.botones_n = {
                    '√': (0, 0), 'π': (0, 1), '^': (0, 2), '❗': (0, 3),
                    'C': (1, 0), '()': (1, 1), '%': (1, 2), '/': (1, 3),
                    '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3),
                    '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3),
                    '1': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3),
                    '.': (5, 0), '0': (5, 1), '⬅': (5, 2), '=': (5, 3),
                  }

    # Creamos los botones de la calculadora normal cogiendo la lista de botones creada anteriormente
    def calculadora_n(self):
        for boton, pos in self.botones_n.items():
            self.botones_normal[boton] = QPushButton(boton)
            self.botones_normal[boton].setFixedSize(50, 25)
            #  Añadimos los botones a la calculadora
            self.layout_b.addWidget(self.botones_normal[boton], pos[0], pos[1])

            self.botones_normal[boton].setShortcut(
                QKeySequence(boton))  # Hacer que la claculaddora funcione por teclado

            if boton == "⬅":
                self.botones_normal[boton].setShortcut(QKeySequence("DELETE"))  # Hacer que borre por teclado

            if boton == "=":
                self.botones_normal[boton].setShortcut(QKeySequence("enter"))  # Hacer que funcione el enter

            self.botones_normal[boton].clicked.connect(
                self.operaciones)  # Cuando clickemos nos mandara a operaciones

        self.layout_p.addLayout(self.layout_b)  # Añadimos al layout principal el layout de botones
        self.botones_normal['='].clicked.connect(
            self.resultado)  # Si pulsamos en '=' llama a la funcion 'resultado'

    # Creamos los botones de la calculadora cientifica cogiendo la lista de botones creada anteriormente
    def calculadora_c(self):
        for boton, pos in self.botones_cienti.items():
            self.botones_cienti[boton] = QPushButton(boton)
            self.botones_cienti[boton].setFixedSize(50, 25)
            #  Añadimos los botones a la calculadora
            self.layout_b.addWidget(self.botones_cienti[boton], pos[0], pos[1])

            self.botones_cienti[boton].setShortcut(
                QKeySequence(boton))  # Hacer que la claculaddora funcione por teclado

            if boton == "⬅":
                self.botones_cienti[boton].setShortcut(QKeySequence("delete"))  # Hacer que borre por teclado

            if boton == "=":
                self.botones_cienti[boton].setShortcut(QKeySequence("enter"))  # Hacer que funcione el enter

            self.botones_cienti[boton].clicked.connect(
                self.operaciones)  # Cuando clickemos nos mandara a operaciones

        self.layout_p.addLayout(self.layout_b)  # Añadimos al layout principal el layout de botones
        self.botones_cienti['='].clicked.connect(
            self.resultado)  # Si pulsamos en '=' llama a la funcion 'resultado'

    # Funciones:
    def operaciones(self):
        if (self.sender().text() == "="):
            pass
        elif (self.sender().text() == "C"):  # Vaciamos el texto
            self.borrar_t()
        elif(self.sender().text()=="π"):  # Le pasamos el numero PI
            self.guardar += "3.14159"
            self.actualizar_t(self.guardar)
        elif (self.sender().text() == "⬅"):  # Ens borra el ultim numero o operador
            self.guardar = self.guardar[:-1]
            self.actualizar_t(self.guardar)
        elif (self.sender().text() == "x"):  # Ens cambia la 'x' per la '*' per a que el eval l'agafe
            self.guardar += "*"
            self.actualizar_t(self.guardar)
        elif (self.sender().text() == "()"):  # Añadim el parentesis
            if(self.comprovar_p):  # Añadimos la primer parte del parentesis '('
                self.guardar += "("
                self.comprovar_p = False
                self.actualizar_t(self.guardar)
            elif(not self.comprovar_p):  # Si ya tenemos la primera parte, añadimos la segunda ')'
                self.guardar += ")"
                self.comprovar_p = True
                self.actualizar_t(self.guardar)
        else:  # Si no hemos pulsado ninguna operacion de antes, nos añade lo pulsado
            self.guardar += self.sender().text()
            self.actualizar_t(self.guardar)

    # Borra el texto del cuadro_t
    def borrar_t(self):
        self.actualizar_t("")
        self.guardar = ""

    # Actualizamos la operacion
    def actualizar_t(self, text):
        self.cuadro_t.setText(text)

    # Calcula la operacion guardada en 'guardar' con el metodo eval
    def resultado(self):
        self.actualizar_t(str(eval(self.guardar)))
        if self.guardar_d.isChecked():
            self.guardar_datos()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    # Guardamos los datos en un txt
    def guardar_datos(self):
        operaciones = os.path.join(os.path.dirname(__file__), "guardar_o.txt")
        with open(operaciones, 'a') as op:
            op.write(self.guardar + " = " + self.cuadro_t.text() + "\n")

    # Para salir de la calculadora
    def salir(self):
        quit()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
