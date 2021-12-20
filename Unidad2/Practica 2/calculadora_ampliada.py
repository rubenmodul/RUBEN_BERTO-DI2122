import os
import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import *

class calculadora_ampliada(QMainWindow):
    def __init__(self):
        super(calculadora_ampliada, self).__init__()
        self.setWindowTitle("Calculadora_ampliada")

        # Creem el widget principal
        self.principal_w = QWidget()
        self.setCentralWidget(self.principal_w)

        # Creem el stacked_layout y el añadim al widget principal
        self.stacked_layout = QStackedLayout(self.principal_w)

        # Calculadora Estandar
        self.calculadora_e = QWidget()
        self.layout_e = QVBoxLayout(self.calculadora_e)
        self.calculadora_e.setLayout(self.layout_e)
        self.stacked_layout.addWidget(self.calculadora_e)

        # Calculadora Cientifica
        self.calculadora_ci = QWidget()
        self.layout_c = QVBoxLayout(self.calculadora_ci)
        self.calculadora_ci.setLayout(self.layout_c)
        self.stacked_layout.addWidget(self.calculadora_ci)

        self.cuadro_t_c = QLineEdit()  # Creamos nuestro cuadro de texto 'cuadro_t_c'
        self.cuadro_t_c.setReadOnly(True)  # Solo leer
        self.layout_c.addWidget(self.cuadro_t_c)  # Añadimos el cuadro de texto a nuestro layout cientifico

        self.cuadro_t_e = QLineEdit()  # Creamos nuestro cuadro de texto 'cuadro_t_e'
        self.cuadro_t_e.setReadOnly(True)  # Solo leer
        self.layout_e.addWidget(self.cuadro_t_e)  # Añadimos el cuadro de texto a nuestro layout estandar


        # Creamos el 'toolbar' paa la parte del menu
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # Añadimos los botones
        calcu_cien = QAction("&Calculadora Cientifica", self)
        calcu_cien.setStatusTip("Calculadora Cientifica")
        calcu_cien.triggered.connect(self.modo_c)

        toolbar.addSeparator()

        calcu_nor = QAction("Calculadora Estandar", self)
        calcu_nor.setStatusTip("Calculadora Estandar")
        calcu_nor.triggered.connect(self.modo_n)

        self.guardar_d = QAction("Guardar", self)
        self.guardar_d.setStatusTip("Guardar")
        self.guardar_d.triggered.connect(self.guardar_datos)
        self.guardar_d.setShortcut(QKeySequence("CTRL+S"))
        self.guardar_d.setCheckable(True)

        salir = QAction("Salir", self)
        salir.setStatusTip("Salir")
        salir.triggered.connect(self.salir)
        salir.setShortcut(QKeySequence("CTRL+Q"))

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        menu = self.menuBar()

        file_menu = menu.addMenu("&Menu")
        file_submenu = file_menu.addMenu("Modo")
        file_submenu.addAction(calcu_cien)
        file_submenu.addSeparator()
        file_submenu.addAction(calcu_nor)
        file_menu.addAction(self.guardar_d)
        file_menu.addAction(salir)

        # Variable
        self.guardar = ""  # Guardar botones pulsados

        self.botones_n = {}  # Lista para los botones de la estandard
        self.botones_cienti = {}  # Lista para los botones de la cientifica

        #  Añadimos cada signo en su boton para la calculadora cientifica
        self.botones_cienti = {
            '√': (0, 0), 'π': (0, 1), '^': (0, 2), '❗': (0, 3), 'Hyp': (0, 4), 'Mod': (0, 5),
            'C': (1, 0), '(': (1, 1), ')': (1, 2), '/': (1, 3), '%': (1, 4), '1/x': (1, 5),
            '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3), 'Cos': (2, 4), 'x!': (2, 5),
            '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3), 'Tan': (3, 4), 'x^2': (3, 5),
            '1': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3), 'Log': (4, 4), 'x^y': (4, 5),
            '.': (5, 0), '0': (5, 1), '⬅': (5, 2), '=': (5, 3), 'Ln': (5, 4), 'x^3': (5, 5),
        }

        #  Añadimos cada signo en su boton para la calculadora normal
        self.botones_n = {
            '√': (0, 0), 'π': (0, 1), '^': (0, 2), '/': (0, 3),
            'C': (1, 0), '(': (1, 1), ')': (1, 2), '%': (1, 3),
            '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3),
            '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3),
            '1': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3),
            '.': (5, 0), '0': (5, 1), '⬅': (5, 2), '=': (5, 3),
        }

        # Creamos los botones de la calculadora normal cogiendo la lista de botones creada anteriormente

        self.gridlayout_e =QGridLayout()

        for boton in self.botones_n.keys():
            b = QPushButton(boton)
            b.setFixedSize(50, 25)
            #  Añadimos los botones a la calculadora
            self.gridlayout_e.addWidget(b, self.botones_n[boton][0]
                                    , self.botones_n[boton][1])

            b.setStatusTip(boton)  # Cuando pasemos el raton por encima nos dira que signo es


            b.setShortcut(
                QKeySequence(boton))  # Hacer que la calculadora funcione por teclado

            if boton == "⬅":
                b.setShortcut(QKeySequence("delete"))  # Hacer que borre por teclado

            if boton == "=":
                b.setShortcut(QKeySequence("enter"))  # Hacer que funcione el enter

            b.clicked.connect(
                self.operaciones)  # Cuando clickemos nos mandara a operaciones

        self.layout_e.addLayout(self.gridlayout_e)  # Añadimos al layout principal el layout de botones

        # Creamos los botones de la calculadora cientifica cogiendo la lista de botones creada anteriormente

        self.gridlayout_c =QGridLayout()

        for boton in self.botones_cienti.keys():
            b = QPushButton(boton)
            b.setFixedSize(50, 25)
            #  Añadimos los botones a la calculadora
            self.gridlayout_c.addWidget(b, self.botones_cienti[boton][0]
                                    , self.botones_cienti[boton][1])

            b.setStatusTip(boton)  # Cuando pasemos el raton por encima nos dira que signo es

            b.setShortcut(
                QKeySequence(boton))  # Hacer que la claculaddora funcione por teclado

            if boton == "⬅":
                b.setShortcut(QKeySequence("delete"))  # Hacer que borre por teclado

            if boton == "=":
                b.setShortcut(QKeySequence("enter"))  # Hacer que funcione el enter

            b.clicked.connect(
                self.operaciones)  # Cuando clickemos nos mandara a operaciones

        self.layout_c.addLayout(self.gridlayout_c)  # Añadimos al layout principal el layout de botones

    # Funciones:
    def operaciones(self):
        if (self.sender().text() == "="):
            self.resultado()
        elif (self.sender().text() == "C"):  # Vaciamos el texto
            self.borrar_t()
        elif (self.sender().text() == "π"):  # Le pasamos el numero PI
            self.guardar += "3.14159"
            self.actualizar_t(self.guardar)
        elif (self.sender().text() == "⬅"):  # Ens borra el ultim numero o operador
            self.guardar = self.guardar[:-1]
            self.actualizar_t(self.guardar)
        elif (self.sender().text() == "x"):  # Ens cambia la 'x' per la '*' per a que el eval l'agafe
            self.guardar += "*"
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
        self.cuadro_t_c.setText(text)
        self.cuadro_t_e.setText(text)

    # Calcula la operacion guardada en 'guardar' con el metodo eval
    def resultado(self):
        self.actualizar_t(str(eval(self.guardar)))
        if self.guardar_d.isChecked():
            self.guardar_datos()

    # Guardamos los datos en un txt
    def guardar_datos(self):
        #  Para que nos salga la ventan de donde guardarlo
        '''
        g = QFileDialog(self)
        self.archiu, var = g.getOpenFileName()
        :return: con esto queriamos que nos mostrara por pantalla donde
        quieres guardarlo pero como e lo preguntaba varias veces
        lo comento
        '''

        operaciones = os.path.join(os.path.dirname(__file__), "guardar_o.txt")

        with open(operaciones, 'a') as op:
            if(self.cuadro_t_c == ""):
                op.write(self.guardar + " = " + self.cuadro_t_e.text() + "\n")
            else:
                op.write(self.guardar + " = " + self.cuadro_t_c.text() + "\n")

    #  Modo estandar
    def modo_n(self):
        self.statusBar.showMessage("Calculadora Estandar")
        self.stacked_layout.setCurrentIndex(0)

    #  Modo cientifica
    def modo_c(self):
        self.statusBar.showMessage("Calculadora Cientifica")
        self.stacked_layout.setCurrentIndex(1)

    # Para salir de la calculadora
    def salir(self):

        salir = QMessageBox(self)
        salir.setWindowTitle("Salir")
        salir.setText("Estas seguro que deseas salir ?")
        button = salir.exec()

        if button == QMessageBox.Ok:
            exit()

app = QApplication(sys.argv)
window = calculadora_ampliada()
window.show()
app.exec()
