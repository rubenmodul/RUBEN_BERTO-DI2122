import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QGridLayout, QVBoxLayout,
    QLineEdit, QPushButton)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora")  # Añadimos titulo de la ventana

        self.widget = QWidget()
        self.layout_p = QVBoxLayout(self.widget)  # Variable 'layout_p' que sera nuestro (layout principal)
        self.setCentralWidget(self.widget)
        self.widget.setLayout(self.layout_p)

        # Variables
        self.guardar = ""  # Guardar botones pulsados
        self.comprovar_p = True  # Lo utilizaremos para los parentesis
        layout_b = QGridLayout()  # Layout para los botones

        self.cuadro_t = QLineEdit()  # Creamos nuestro cuadro de texto 'cuadro_t'
        self.cuadro_t.setReadOnly(True)  # Solo leer
        self.layout_p.addWidget(self.cuadro_t)  # Añadimos el cuadro de texto a nuestro layout principal

        self.botones = {}  # Lista para los botones

        #  Añadimos cada signo en su boton 
        botones = {
                    '√': (0, 0), 'π': (0, 1), '^': (0, 2), '❗': (0, 3),
                    'C': (1, 0), '()': (1, 1), '%': (1, 2), '/': (1, 3),
                    '7': (2, 0), '8': (2, 1), '9': (2, 2), 'x': (2, 3),
                    '4': (3, 0), '5': (3, 1), '6': (3, 2), '+': (3, 3),
                    '1️': (4, 0), '2': (4, 1), '3': (4, 2), '-': (4, 3),
                    '.': (5, 0), '0': (5, 1), '⬅': (5, 2), '=': (5, 3),
                  }

        # Creamos los botones de la calculadora cogiendo la lista de botones creada anteriormente
        for boton, pos in botones.items():
            self.botones[boton] = QPushButton(boton)
            self.botones[boton].setFixedSize(50, 25)
            #  Añadimos los botones a la calculadora
            layout_b.addWidget(self.botones[boton], pos[0], pos[1])

            self.botones[boton].clicked.connect(self.operaciones)  # Cuando clickemos nos mandara a operaciones

        self.layout_p.addLayout(layout_b)  # Añadimos al layout principal el layout de botones
        self.botones['='].clicked.connect(self.resultado)  # Si pulsamos en '=' llama a la funcion 'resultado'

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

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()









