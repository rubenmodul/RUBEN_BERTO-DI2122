import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLineEdit
)

class Admin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin")
        self.label = QLabel("Has entrat com a administrador")
        self.setCentralWidget(self.label)

        volver_a = QAction("&Log out", self)
        volver_a.setStatusTip("Log out")
        volver_a.triggered.connect(self.volver_p)

        salir_a = QAction("&Salir", self)
        salir_a.setStatusTip("Salir")
        salir_a.triggered.connect(self.exit)

        menu = self.menuBar()

        menu_principal = menu.addMenu("&Menu")
        menu_principal.addAction(volver_a)
        menu_principal.addAction(salir_a)

    #  Volver a la pantalla de Login
    def volver_p(self):
        self.hide()
        if __name__ == '__main__':
            self = MainWindow()
            if __name__ == '__main__':
                w.show()

    #  Salir
    def exit(self):
        app.closeAllWindows()

class User(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Usuari")
        self.label = QLabel("Has entrat com a usuari", self)
        self.setCentralWidget(self.label)

        volver_u = QAction("&Log out", self)
        volver_u.setStatusTip("Log out")
        volver_u.triggered.connect(self.volver_p)

        salir_u = QAction("&Salir", self)
        salir_u.setStatusTip("Salir")
        salir_u.triggered.connect(self.exit)

        menu = self.menuBar()

        menu_principal = menu.addMenu("&Menu")
        menu_principal.addAction(volver_u)
        menu_principal.addAction(salir_u)

    #  Volver a la pantalla de Login
    def volver_p(self):
        self.hide()
        if __name__ == '__main__':
            self = MainWindow()
            if __name__ == '__main__':
                w.show()

    #  Salir
    def exit(self):
            app.closeAllWindows()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")

        self.user = User()
        self.admin = Admin()

        layout = QVBoxLayout()

        self.label = QLabel("", self)

        # Añadim la casella del'usuari'
        self.usuari = QLineEdit()
        self.usuari.setPlaceholderText("Usuario")
        layout.addWidget(self.usuari)

        # Añadim la casella de 'contraseña'
        self.con = QLineEdit()
        self.con.setPlaceholderText("Contraseña")
        layout.addWidget(self.con)

        # Añadimos el boton
        button1 = QPushButton("Login")
        button1.clicked.connect(self.comprobar)
        layout.addWidget(button1)

        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    # Comprobamos si queremos entrar como administrador o usuario
    def comprobar(self):
        if self.usuari.text() == "admin" and self.con.text() == "1234":
            self.admin.show()
        elif self.usuari.text() == "user" and self.con.text() == "1234":
            self.user.show()
        else:
            self.label.setText("Datos incorrectos")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()